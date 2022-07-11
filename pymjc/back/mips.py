from contextlib import nullcontext
import itertools
from typing import List
from pymjc.back import assem
from pymjc.front import frame, temp, tree
from pymjc.front.symbol import Symbol
from pymjc.util import BoolList

class InFrame(frame.Access):

    def __init__(self, offset: int):
        self.offset: int = offset

    def exp(self, fp: tree.Exp) -> tree.Exp:
        return tree.MEM(tree.BINOP(tree.BINOP.PLUS, fp, tree.CONST(self.offset)))

    def to_string(self) -> str:
        return str(self.offset)


class InReg(frame.Access):

    def __init__(self, temp: temp.Temp):
        self.temp = temp

    def exp(self, fp: tree.Exp) -> tree.Exp:
        return tree.TEMP(self.temp)

    def to_string(self) -> str:
        return self.temp.to_string()

class Codegen():

    def __init__(self, frame: frame.Frame):
        self.frame = frame
        self.instr_list = None
        self.last = None

    def emit(self, instr: assem.Instr) -> None:
        if (self.last is None):
            self.instr_list = assem.InstrList(instr, None)
            self.last = assem.InstrList(instr, None)
        else:
            self.instr_list.tail = assem.InstrList(instr, None)
            self.last = self.instr_list.tail


    def munch_stm(self, stmt: tree.Stm) -> None:
        if isinstance(stmt, tree.SEQ):
            self.munch_stm(stmt.left_stm)
            self.munch_stm(stmt.right_stm)

        elif isinstance(stmt, tree.LABEL):
            self.emit(assem.LABEL(stmt.label.to_string() + ":\n", stmt.label.to_string()))

        elif isinstance(stmt, tree.MOVE):
            self.munch_move(stmt.dest, stmt.src)

        elif  isinstance(stmt, tree.JUMP):
            self.munch_jump(stmt)

        elif isinstance(stmt, tree.CJUMP):
            self.munch_cjump(stmt)

        elif  isinstance(stmt, tree.EXP) and isinstance(stmt.exp, tree.CALL):
            r: temp.Temp  = self.munch_exp(stmt.exp.func_exp)
            l: temp.TempList = self.munch_args(0, stmt.exp.arg_exp_list)
            if isinstance(stmt.exp.func_exp, tree.NAME):
                temp_list = temp.TempList()
                for element in MipsFrame.call_defs:
                    temp_list.add_tail(element)
                self.emit(assem.OPER("jal " + stmt.exp.func_exp.label.to_string() + "\n", temp_list, temp.TempList(r, l)))

    def munch_exp(self, exp: tree.Exp) -> temp.Temp:
        if isinstance(exp, tree.MEM):
            return self.munch_mem(exp)

        elif isinstance(exp, tree.BINOP):
            return self.munch_binop(exp)
        
        elif isinstance(exp, tree.CONST):
            r = temp.Temp()
            self.emit(assem.OPER("li `d0,"+ str(exp.value) + "\n", temp.TempList(r, None), None))
            return r
        
        elif isinstance(exp, tree.TEMP):
            return exp.temp
        
        elif isinstance(exp, tree.NAME):
            return temp.Temp()

        return None

    def munch_args(self, i: int, args: tree.ExpList) -> temp.TempList:
        tmp: tree.ExpList  = args
        out = temp.TempList()

        while tmp is not None:
            out.add_tail(self.munch_exp(tmp.head))
            tmp = tmp.tail
        
        return out


    def munch_move(self, dst: tree.Exp, src: tree.Exp):
        if isinstance(dst, tree.MEM):
            self.munch_move_mem(dst, src)

        elif isinstance(dst, tree.TEMP) and isinstance(src, tree.CALL):
            r: temp.Temp = self.munch_exp(src.func_exp)
            l: temp.TempList = self.munch_args(0, src.arg_exp_list)
            if isinstance(src.func_exp, tree.NAME):
                self.emit(assem.OPER("jal " + src.func_exp.label.to_string() + "\n", temp.TempList(r, None), l))

        elif isinstance(dst, tree.TEMP):
            self.munch_move_temp(dst, src)

    def munch_move_mem(self, dst: tree.MEM, src: tree.Exp) -> None:
        srcTemps: temp.TempList 
        dstTemps: temp.TempList

        if isinstance(dst.exp, tree.BINOP):
            if dst.exp.op == tree.BINOP.PLUS and isinstance(dst.exp.right_exp, tree.CONST):
                dstTemps = temp.TempList(self.munch_exp(dst.exp.left_exp), None)
                srcTemps = temp.TempList(self.munch_exp(src), None)
                self.emit(assem.OPER("sw `s0," + str(dst.exp.right_exp.value) + "(`d0)\n", dstTemps, srcTemps))
            elif dst.exp.op == tree.BINOP.PLUS and isinstance(dst.exp.left_exp, tree.CONST):
                dstTemps = temp.TempList(self.munch_exp(dst.exp.right_exp), None)
                srcTemps = temp.TempList(self.munch_exp(src), None)
                self.emit(assem.OPER("sw `s0," + str(dst.exp.left_exp.value) + "(`d0)\n", dstTemps, srcTemps))

        elif isinstance(src, tree.MEM):
            dstTemps = temp.TempList(self.munch_exp(dst.exp), None)
            srcTemps = temp.TempList(self.munch_exp(src.exp), None)
            self.emit(assem.OPER("move `d0, `s0\n", dstTemps, srcTemps))
        
        elif isinstance(dst.exp, tree.CONST):
            srcTemps = temp.TempList(self.munch_exp(src), None)
            dstTemps = temp.TempList(self.munch_exp(dst.exp), None)
            self.emit(assem.OPER("sw `s0,"+ str(dst.exp.value) +"(`d0)\n", dstTemps, srcTemps))
        
        else:
            dstTemps = temp.TempList(self.munch_exp(dst.exp), None);
            srcTemps = temp.TempList(self.munch_exp(src), None);
            self.emit(assem.OPER("sw `s0, 0(`d0)\n", dstTemps, srcTemps))

    def munch_move_temp(self, dst: tree.TEMP, src: tree.Exp) -> None:
        tmp: temp.Temp = self.munch_exp(src)
        self.emit(assem.MOVE("move `s0,`d0\n", dst.temp, tmp))



    def munch_cjump(self, stmt: tree.CJUMP) -> None:
        r: temp.Temp = self.munch_exp(tree.BINOP(tree.BINOP.MINUS, stmt.left_exp, stmt.right_exp))
        if (stmt.rel_op == tree.CJUMP.EQ):
            self.emit(assem.OPER("beq `s0,$zero,`j0\n", None, temp.TempList(r, None), temp.LabelList(stmt.if_true, None)))
        
        elif (stmt.rel_op == tree.CJUMP.GE):
            self.emit(assem.OPER("bge `s0,$zero,`j0\n", None, temp.TempList(r, None),temp.LabelList(stmt.if_true, None)))
        
        elif (stmt.rel_op == tree.CJUMP.LT):
            self.emit(assem.OPER("blt `s0,$zero,`j0\n", None, 
                    temp.TempList(r, None), temp.LabelList(stmt.if_true, None)))
        
        elif (stmt.rel_op == tree.CJUMP.NE):
            self.emit(assem.OPER("bne `s0,$zero,`j0\n", None, temp.TempList(r, None), temp.LabelList(stmt.if_true, None)))
        
        elif (stmt.rel_op == tree.CJUMP.GT):
            self.emit(assem.OPER("bgt `s0,$zero,`j0\n", None, temp.TempList(r, None), temp.LabelList(stmt.if_true, None)))
        
        else:
            self.emit(assem.OPER("j `j0\n", None, None, temp.LabelList(stmt.if_false, None)))


    def munch_jump(self, stmt: tree.JUMP) -> None:
        self.emit(assem.OPER("j `j0\n", None, None, temp.LabelList(stmt.exp.label, None)))



    def munch_mem(self, mem: tree.MEM) -> temp.Temp:
        if isinstance(mem.exp, tree.BINOP):
            if (mem.exp.op == tree.BINOP.PLUS) and isinstance(mem.exp.right_exp, tree.CONST):
                r = temp.Temp()
                self.emit(assem.OPER("lw `d0," + str(mem.exp.right_exp.value) +"(`s0)\n",
                          temp.TempList(r, None),
                          temp.TempList(self.munch_exp(mem.exp.left_exp), None)))
                return r

            elif (mem.exp.op == tree.BINOP.PLUS) and isinstance(mem.exp.left_exp, tree.CONST):
                r = temp.Temp()
                self.emit(assem.OPER("lw `d0," + str(mem.exp.left_exp.value) +"(`s0)\n",
                          temp.TempList(r, None),
                          temp.TempList(self.munch_exp(mem.exp.right_exp), None)))
                return r

        elif isinstance(mem.exp, tree.CONST):
            r = temp.Temp()
            self.emit(assem.OPER("lw `d0," + str(mem.exp.value) +"($zero)\n", temp.TempList(r, None), None))
            return r

        r = temp.Temp()
        self.emit(assem.OPER("lw `d0,`s0\n", temp.TempList(r, None), temp.TempList(self.munch_exp(mem.exp), None)))
        return r


    def munch_binop(self, stmt: tree.BINOP) -> temp.Temp:
        r = temp.Temp()
        
        # munch_exp(BINOP(PLUS,e1,CONST (i)))
        if (stmt.op == tree.BINOP.PLUS) and isinstance(stmt.right_exp, tree.CONST):
            src = temp.TempList(self.munch_exp(stmt.left_exp), None)
            self.emit(assem.OPER("addi `d0,`s0," + str(stmt.right_exp.value) + "\n",temp.TempList(r, None), src))
            return r

        # munch_exp(BINOP(PLUS,CONST (i),e1))
        if (stmt.op == tree.BINOP.PLUS) and isinstance(stmt.left_exp, tree.CONST):            
            src = temp.TempList(self.munch_exp(stmt.right_exp), None)
            self.emit(assem.OPER("addi `d0,`s0," + str(stmt.left_exp.value) + "\n",temp.TempList(r, None), src))
            return r            


        # munch_exp(BINOP(PLUS,e1,e2))
        if (stmt.op == tree.BINOP.PLUS):
            src = temp.TempList(self.munch_exp(stmt.left_exp), temp.TempList(self.munch_exp(stmt.right_exp), None))
            self.emit(assem.OPER("add `d0,`s0,`s1\n", temp.TempList(r, None), src))
            return r

        # munch_exp(BINOP(MUL,e1,e2))
        if (stmt.op == tree.BINOP.MUL):
            src = temp.TempList(self.munch_exp(stmt.left), temp.TempList(self.munch_exp(stmt.right), None))
            self.emit(assem.OPER("mul `d0,`s0,`s1\n",temp.TempList(r, None), src))
            return r

        # munch_exp(BINOP(DIV,e1,e2))
        if (stmt.op == tree.BINOP.DIV):
            src = temp.TempList(self.munch_exp(stmt.left_exp), temp.TempList(self.munch_exp(stmt.right_exp), None))
            self.emit(assem.OPER("div `s0,`s1\nmflo `d0\n", temp.TempList(r, None), src))
            return r

        # munch_exp(BINOP(SUB,e1,CONST(i)))
        if (stmt.op == tree.BINOP.MINUS) and isinstance(stmt.right_exp, tree.CONST):
            src = temp.TempList(self.munch_exp(stmt.left_exp), temp.TempList(self.munch_exp(stmt.right_exp), None))
            self.emit(assem.OPER("sub `d0,`s0,`s1\n", temp.TempList(r, None), src))
            return r

        # munch_exp(BINOP(SUB,e1,e2))
        if (stmt.op == tree.BINOP.MINUS):
            src = temp.TempList(self.munch_exp(stmt.left_exp), temp.TempList(self.munch_exp(stmt.right_exp), None))
            self.emit(assem.OPER("sub `d0,`s0, `s1\n", temp.TempList(r, None), src))
            return r

        # munch_exp(BINOP(AND,e1,e2))
        if (stmt.binop == tree.BINOP.AND):
            src = temp.TempList(self.munch_exp(stmt.left_exp), temp.TempList(self.munch_exp(stmt.right_exp), None))
            self.emit(assem.OPER("and `d0,`s0, `s1\n", temp.TempList(r, None), src))
            return r
        
        # munch_exp(BINOP(OR,e1,e2))
        if (stmt.op == tree.BINOP.OR):
            src = temp.TempList(self.munch_exp(stmt.left_exp), temp.TempList(self.munch_exp(stmt.right_exp), None))
            self.emit(assem.OPER("or `d0,`s0, `s1\n", temp.TempList(r, None), src))
            return r
        
        return None


    def codegen(self, stmt: tree.Stm) -> assem.InstrList:
        l: assem.InstrList
        self.munch_stm(stmt)
        l = self.instr_list
        self.instr_list = self.last = None
        return l










class MipsFrame(frame.Frame):
    ZERO = temp.Temp() # zero reg
    AT = temp.Temp()   # reserved for assembler
    V0 = temp.Temp()   # function result
    V1 = temp.Temp()   # second function result
    A0 = temp.Temp()   # argument1
    A1 = temp.Temp()   # argument2
    A2 = temp.Temp()   # argument3
    A3 = temp.Temp()   # argument4
    T0 = temp.Temp()   # caller-saved
    T1 = temp.Temp()
    T2 = temp.Temp()
    T3 = temp.Temp()
    T4 = temp.Temp()
    T5 = temp.Temp()
    T6 = temp.Temp()
    T7 = temp.Temp()
    S0 = temp.Temp()   # callee-saved
    S1 = temp.Temp()
    S2 = temp.Temp()
    S3 = temp.Temp()
    S4 = temp.Temp()
    S5 = temp.Temp()
    S6 = temp.Temp()
    S7 = temp.Temp()
    T8 = temp.Temp()   # caller-saved
    T9 = temp.Temp()
    K0 = temp.Temp()   #  reserved for OS kernel
    K1 = temp.Temp()   #  reserved for OS kernel
    GP = temp.Temp()   # pointer to global area
    SP = temp.Temp()   # stack pointer
    S8 = temp.Temp()   # callee-save (frame pointer)
    RA = temp.Temp()   # return address

    # registers dedicated to special purposes
    special_regs = [ZERO, AT, K0, K1, GP, SP]
    
    # registers to pass outgoing arguments
    arg_regs =[A0, A1, A2, A3]


    # registers that a callee must preserve for its caller
    callee_saves = [RA, S0, S1, S2, S3, S4, S5, S6, S7, S8]

    # registers that a callee may use without preserving
    caller_saves = [T0, T1, T2, T3, T4, T5, T6, T7, T8, T9, V0, V1]

    FP = temp.Temp() # virtual frame pointer (eliminated)

    bad_ptr: temp.Label  = temp.Label("BADPTR")

    bad_sub: temp.Label  = temp.Label("BADSUB")

    tmp_map = {ZERO: "$0",
                AT: "$at",
                V0: "$v0",
                V1: "$v1",
                A0: "$a0",
                A1: "$a1",
                A2: "$a2",
                A3: "$a3",
                T0: "$t0",
                T1: "$t1",
                T2: "$t2",
                T3: "$t3",
                T4: "$t4",
                T5: "$t5",
                T6: "$t6",
                T7: "$t7",
                S0: "$s0",
                S1: "$s1",
                S2: "$s2",
                S3: "$s3",
                S4: "$s4",
                S5: "$s5",
                S6: "$s6",
                S7: "$s7",
                T8: "$t8",
                T9: "$t9",
                K0: "$k0",
                K1: "$k1",
                GP: "$gp",
                SP: "$sp",
                S8: "$fp",
                RA: "$ra"}


    # registers live on return
    return_sink = [V0] + special_regs + callee_saves

    # registers defined by a call
    call_defs = [RA] + arg_regs + caller_saves

    registers =  caller_saves + callee_saves + arg_regs + special_regs

    spilling: bool = True

    functions = {}

    labels = {}

    word_size = 4

    def __init__(self, symbol: Symbol = None, formal_list: BoolList = None):
        self.offset :int = 0
        self.max_arg_offset :int = 0
        if (symbol is not None) and (formal_list is not None):
            count = MipsFrame.functions.get(symbol.to_string())

            if count is None:
                count = 0
                self.name = temp.Label(symbol)
            else:
                count += 1 
                self.name = temp.Label(symbol.to_string() + "." + str(count))
            
            MipsFrame.functions[symbol.to_string()] = count
            self.actuals = List[frame.Access]
            self.formals = List[frame.Access]

            offset :int = 0
            if len(formal_list.list) == 0:
                return None
            
            escapes = iter(formal_list.list)
            escape = next(escapes)
            self.formals.append(self.alloc_local(escape))
            self.actuals.append(InReg(MipsFrame.V0))

            for i in range(len(self.arg_regs)):
                try:
                    escape = next(escapes)
                except StopIteration:
                    break
            
            offset += self.word_size
            self.actuals.append(InReg(self.arg_regs[i]))

            if escape:
                self.formals.append(InFrame(offset))
            else:
                self.formals.append(InReg(temp.Temp()))
            
            try:
                while True:
                    escape = next(escapes)
                    offset += MipsFrame.word_size
                    actual = InFrame(offset)
                    self.actuals.append(actual)
                    if escape:
                        self.formals.append(actual)
                    else:
                        self.formals.append(InReg(temp.Temp()))                    
            except StopIteration:
                return None

    def new_frame(self, symbol: Symbol, formal_list: BoolList) -> frame.Frame:
        if (self.name is not None):
            symbol = Symbol.symbol(self.name.to_string() + "." + symbol.to_string())

        return MipsFrame(symbol, formal_list)


    def alloc_local(self, escape: bool) -> frame.Access:
        if escape:
            result = InFrame(self.offset)
            self.offset -= MipsFrame.word_size
            return result
        else:
            return InReg(temp.Temp())

    def FP(self) -> temp.Temp:
        return MipsFrame.FP

    def  word_size(self) -> int:
        return MipsFrame.word_size

    def external_call(self, func:str, args: List[tree.Exp]) -> tree.Exp:
        label: temp.Label = self.labels.get(func)
        if label is None:
            label = temp.Label("_" + func)
            self.labels[func] = label
        args.insert(0, tree.CONST(0))

        exp_list = tree.ExpList()
        for arg in args:
            exp_list.add_tail(arg)

        return tree.CALL(tree.NAME(label), exp_list)

    def RV(self) -> temp.Temp:
        return MipsFrame.V0

    def string(self, label: temp.Label, str_value: str) -> str:
        length = len(str_value)
        lit: str = ""
        for i in range(length):
            c = str_value[i]
            match c:
                case '\b':
                    lit += "\\b"

                case '\t':
                    lit += "\\t"

                case '\n':
                    lit += "\\n"

                case '\f':
                    lit += "\\f"

                case '\r':
                    lit += "\\r"
                
                case '\"':
                    lit += "\\\""

                case '\\':
                    lit += "\\\\"

                case __:
                    if (c < ' ' or c > '~'):
                        v: int = ord(c)
                        lit += "\\" + ((v >> 6) & 7) + ((v >> 3) & 7) + (v & 7)
                    else:
                        lit += c
        return "\t.data\n\t.word " + str(length) + "\n" + label.to_string() + ":\t.asciiz\t\"" + lit + "\""

    def bad_ptr(self) -> temp.Label:
        MipsFrame.bad_ptr

    def bad_sub(self) -> temp.Label:
        MipsFrame.bad_sub

    def temp_map(self, temp: temp.Temp) -> str:
        MipsFrame.tmp_map.get(temp)

    def codegen(self, stmts: List[tree.Stm]) -> List[assem.Instr]:
        code_gen = Codegen(self)
        frame_assem_list = List[assem.Instr]
        instr_list: assem.InstrList = None
        
        for stmt in stmts:
            instr_list = code_gen.codegen(stmt)
            for instr in instr_list.to_list():
                frame_assem_list.append(instr)

        return frame_assem_list

    def SEQ(left: tree.Stm, right:tree.Stm) -> tree.Stm:
        if (left is None):
            return right
        
        if (right is None):
            return left
        return tree.SEQ(left, right)
	

    def proc_entry_exit1(self, body: List[tree.Stm]) -> None:
        index = 0        
        #assign formals
        for (formal, actual) in zip(self.formals, self.actuals):
            body.insert(index, tree.MOVE(formal.exp(tree.TEMP(MipsFrame.FP)), actual.exp(tree.TEMP(MipsFrame.FP))))
            index += 1

        #assign callees
        for i in range(len(MipsFrame.callee_saves)):
            access: frame.Access = self.alloc_local(not MipsFrame.spilling) 
            body.insert(i, tree.MOVE(access.exp(tree.TEMP(MipsFrame.FP)), tree.TEMP(MipsFrame.callee_saves[i])))
            body.append(tree.MOVE(access.exp(tree.TEMP(MipsFrame.callee_saves[i])), tree.TEMP(MipsFrame.FP)))


    def OPER(assem: str, dest: List[temp.Temp], src: List[temp.Temp]) -> assem.Instr:
        dest_list = temp.TempList()
        for d in dest:
            dest_list.add_tail(d)

        src_list = temp.TempList()
        for s in src:
            src_list.add_tail(s)

        return tree.OPER(assem, dest_list, src_list)

    def proc_entry_exit2(self, body: List[assem.Instr]) -> None:
        body.append(MipsFrame.OPER("#\treturn", None, MipsFrame.return_sink))

    def proc_entry_exit3(self, body: List[assem.Instr]) -> None:
        frame_size = self.max_arg_offset - self.offset
        index = 0
        body.insert(index, MipsFrame.OPER("\t.text", None, None))
        index +=1
        body.insert(index, MipsFrame.OPER(self.name.to_string() + ":", None, None))
        index +=1
        body.insert(index, MipsFrame.OPER(self.name.to_string() + "_framesize=" + str(frame_size), None, None))
        index +=1
        if (frame_size != 0):
            body.insert(index, MipsFrame.OPER("\tsubu $sp " + self.name.to_string() + "_framesize", [MipsFrame.SP], [MipsFrame.SP]))
            index +=1
            body.insert(index, MipsFrame.OPER("\taddu $sp " + self.name.to_string() + "_framesize", [MipsFrame.SP], [MipsFrame.SP]))
            index +=1
        body.add(index, MipsFrame.OPER("\tj $ra", None, [MipsFrame.RA]))

    def registers(self) -> List[temp.Temp]:
        return MipsFrame.caller_saves + MipsFrame.callee_saves + MipsFrame.arg_regs + MipsFrame.special_regs

    def spill(self, insns: List[assem.Instr], spills: List[temp.Temp]) -> None:
        pass

    def program_tail(self) -> str:
        tail_list = ["         .text            ", "         .globl _halloc   ", "_halloc:                  ",
                     "         li $v0, 9        ", "         syscall          ", "         j $ra            ",
                     "                          ", "         .text            ", "         .globl _printint ",
                     "_printint:                ", "         li $v0, 1        ", "         syscall          ",
                     "         la $a0, newl     ", "         li $v0, 4        ", "         syscall          ",
                     "         j $ra            ", "                          ", "         .data            ",
                     "         .align   0       ", "newl:    .asciiz \"\\n\"  ", "         .data            ",
                     "         .align   0       ", "str_er:  .asciiz \" ERROR: abnormal termination\\n\" "   , #verificar
                     "                          ", "         .text            ", "         .globl _error    ",
                     "_error:                   ", "         li $v0, 4        ", "         la $a0, str_er   ",
                     "         syscall          ", "         li $v0, 10       ", "         syscall          "]
        return '\n'.join(tail_list) + "\n"