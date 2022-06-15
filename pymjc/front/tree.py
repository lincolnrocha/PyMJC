from __future__ import annotations
from abc import ABC, abstractmethod
import sys

from pymjc.front.temp import DefaultMap, Label, LabelList, Temp, TempMap


class Exp(ABC):

    @abstractmethod
    def kids(self) -> ExpList:
        pass

    @abstractmethod
    def build(self, kids: ExpList) -> Exp:
        pass

class ExpList():
    def __init__(self, head: Exp = None, tail: ExpList = None):
        self.head: Exp = head
        self.tail: ExpList = tail

    def add_head(self, element: Exp):
        self.tail = ExpList(self.head, self.tail)
        self.head = element
    
    def add_tail(self, element: Exp):
        if self.head is None:
            self.head = element
        else:
            last: ExpList = self.tail
            while last is not None:
                last = last.tail
            last.tail = ExpList(element, None)

class BINOP(Exp):
    PLUS = 0
    MINUS = 1
    MUL = 2
    DIV = 3
    AND = 4
    OR = 5
    LSHIFT = 6
    RSHIFT = 7
    ARSHIFT = 8
    XOR = 9

    def __init__(self, op: int, left_exp: Exp, right_exp: Exp):
        self.op: int = op
        self.left_exp: Exp = left_exp
        self.right_exp: Exp = right_exp

    def kids(self) -> ExpList:
        return ExpList(self.left_exp, ExpList(self.right_exp, None))

    def build(self, kids: ExpList) -> Exp:
        return BINOP(self.op, kids.head, kids.tail.head)


class CALL(Exp):
    def __init__(self, func_exp: Exp, arg_exp_list: ExpList):
        self.func_exp: Exp = func_exp
        self.arg_exp_list: ExpList = arg_exp_list

    def kids(self) -> ExpList:
        return ExpList(self.func_exp, self.arg_exp_list)

    def build(self, kids: ExpList) -> Exp:
        return CALL(kids.head, kids.tail.head)


class CONST(Exp):
    def __init__(self, value: int):
        self.value: int = value

    def kids(self) -> ExpList:
        return None

    def build(self, kids: ExpList) -> Exp:
        return self


class ESEQ(Exp):
    def __init__(self, stm: Stm, exp: Exp):
        self.stm: Stm = stm
        self.exp: Exp = exp

    def kids(self) -> ExpList:
        raise RuntimeError("kids() not applicable to ESEQ")

    def build(self, kids: ExpList) -> Exp:
        raise RuntimeError("build() not applicable to ESEQ")


class MEM(Exp):
    def __init__(self, exp: Exp):
        self.exp: Exp = exp

    def kids(self) -> ExpList:
        return ExpList(self.exp, None)

    def build(self, kids: ExpList) -> Exp:
        return MEM(kids.head)


class NAME(Exp):
    def __init__(self, label: Label):
        self.label: Label = label

    def kids(self) -> ExpList:
        return None

    def build(self, kids: ExpList) -> Exp:
        return self


class TEMP(Exp):
    def __init__(self, temp: Temp):
        self.temp: Temp = temp

    def kids(self) -> ExpList:
        return None

    def build(self, kids: ExpList) -> Exp:
        return self




class Stm(ABC):

    @abstractmethod
    def kids(self) -> ExpList:
        pass

    @abstractmethod
    def build(self, kids: ExpList) -> Stm:
        pass


class StmList():
    def __init__(self, head: Stm, tail: StmList):
        self.head: Stm = head
        self.tail: StmList = tail


class LABEL(Stm):
    def __init__(self, label: Label):
        self.label: Label = label

    def kids(self) -> ExpList:
        return None

    def build(self, kids: ExpList) -> Stm:
        return self


class SEQ(Stm):
    def __init__(self, left_stm: Stm, right_stm: Stm):
        self.left_stm: Stm = left_stm
        self.right_stm: Stm = right_stm

    def kids(self) -> ExpList:
        raise RuntimeError("kids() not applicable to SEQ")

    def build(self, kids: ExpList) -> Stm:
        raise RuntimeError("build() not applicable to SEQ")


class EXP(Stm):
    def __init__(self, exp: Exp):
        self.exp: Exp = exp

    def kids(self) -> ExpList:
        return ExpList(self.exp, None)

    def build(self, kids: ExpList) -> Stm:
        return EXP(kids.head)


class MOVE(Stm):
    def __init__(self, dest: Exp, src: Exp):
        self.dest: Exp = dest
        self.src: Exp = src

    def kids(self) -> ExpList:
        if isinstance(self.dest, MEM):
            return ExpList(self.dest.exp, ExpList(self.src, None))
        else:
            return ExpList(self.src, None)

    def build(self, kids: ExpList) -> Stm:
        if isinstance(self.dest, MEM):
            return MOVE(MEM(kids.head), kids.tail.head)
        else:
            return MOVE(self.dest, kids.head)


class JUMP(Stm):
    def __init__(self, target: Label=None, exp: Exp=None, targets: LabelList=None):
        if target is not None:
            self.exp: Exp = NAME(target)
            self.targets: LabelList = LabelList(target, None)
        else:
            self.exp: Exp = exp
            self.targets: LabelList = targets

    def kids(self) -> ExpList:
        return ExpList(self.exp,None)


    def build(self, kids: ExpList) -> Stm:
        return JUMP(kids.head, self.targets)


class CJUMP(Stm):
    EQ = 0
    NE = 1
    LT = 2
    GT = 3
    LE = 4
    GE = 5
    ULT = 6
    ULE = 7
    UGT = 8
    UGE = 9

    def __init__(self, rel_op: int, left_exp: Exp, right_exp: Exp, if_true: Label, if_false: Label):
        self.rel_op: int = rel_op 
        self.left_exp: Exp = left_exp 
        self.right_exp: Exp = right_exp 
        self.if_true: Label = if_true
        self.if_false: Label = if_false

    def kids(self) -> ExpList:
        return ExpList(self.left_exp, ExpList(self.right_exp, None))


    def build(self, kids: ExpList) -> Stm:
        return CJUMP(self.rel_op, kids.head, kids.tail.head, self.if_true, self.if_false)
    
    def not_rel(rel_op: int) -> int:
        match rel_op:
            case CJUMP.EQ:
                return CJUMP.NE
            case CJUMP.NE:
                return CJUMP.EQ
            case CJUMP.LT:
                return CJUMP.GE
            case CJUMP.GE:
                return CJUMP.LT
            case CJUMP.GT:
                return CJUMP.LE
            case CJUMP.LE:
                return CJUMP.GT
            case CJUMP.ULT:
                return CJUMP.UGE
            case CJUMP.UGE:
                return CJUMP.ULT
            case CJUMP.UGT:
                return CJUMP.ULE
            case CJUMP.ULE:
                return CJUMP.UGT
            case _:
                raise RuntimeError("bad relop in CJUMP.not_rel()")



class Print():
    #sys.stdout
    def __init__(self, out_path: str = None, temp_map: TempMap = None):
        if out_path is not None:
            sys.stdout = open(out_path, 'w')
        
        if temp_map is None:
            self.temp_map = DefaultMap()
        else:
            self.temp_map = temp_map


    def indent(self, d: int):
        #for index in range(d):
        print(d * ' ',  end='')

    def say(self, string: str):
         print(string)

    def say(self, string: str):
         print(string, end='')

    def sayln(self, string: str):
         self.say(string)
         self.say('\n')


    def print_stm(self, stmt : Stm, d: int):
        if stmt is None:
            self.indent(d)
            return None

        if isinstance(stmt, SEQ):
            self.print_seq(stmt, d)

        elif isinstance(stmt, LABEL):
            self.print_label(stmt, d)

        elif isinstance(stmt, JUMP):
            self.print_jump(stmt, d)

        elif isinstance(stmt, CJUMP):
            self.print_cjump(stmt, d)

        elif isinstance(stmt, MOVE):
            self.print_move(stmt, d)

        elif isinstance(stmt, EXP):
            self.print_sexp(stmt, d)

        else:
            raise RuntimeError("Print.print_stm()")


    def print_seq(self, stmt : SEQ, d: int):
        self.indent(d)
        self.sayln("SEQ(")
        self.print_stm(stmt.left, d + 1)
        self.sayln(",")
        self.print_stm(stmt.right, d + 1)
        self.say(")")


    def print_label(self, stmt: LABEL, d: int):
        self.indent(d)
        self.say("LABEL ")
        self.say(stmt.label.to_string())


    def print_jump(self, stmt: JUMP, d: int):
        self.indent(d)
        self.sayln("JUMP(")
        self.print_exp(stmt.exp, d + 1)
        self.say(")")


    def print_cjump(self, stmt: CJUMP, d: int):
        self.indent(d)
        self.say("CJUMP(")

        match(stmt.rel_op):
            case CJUMP.EQ:
                self.say("EQ")

            case CJUMP.NE:
                self.say("NE")

            case CJUMP.LT:
                self.say("LT")

            case CJUMP.GT:
                self.say("GT")

            case CJUMP.LE:
                self.say("LE")

            case CJUMP.GE:
                self.say("GE")

            case CJUMP.ULT:
                self.say("ULT")

            case CJUMP.ULE:
                self.say("ULE")

            case CJUMP.UGT:
                self.say("UGT")

            case CJUMP.UGE:
                self.say("UGE")

            case _:
                raise RuntimeError("Print.print_cjump()")
        
        self.sayln(",")
        self.print_exp(stmt.left_exp, d + 1)
        self.sayln(",")
        self.print_exp(stmt.right_exp, d + 1)
        self.sayln(",")
        self.indent(d + 1)
        self.say(stmt.if_true.to_string())
        self.say(",")
        self.say(stmt.if_false.to_string())
        self.say(")")


    def print_move(self, stmt: MOVE, d: int):
        self.indent(d)
        self.sayln("MOVE(")
        self.print_exp(stmt.dest, d + 1)
        self.sayln(",")
        self.print_exp(stmt.src, d + 1)
        self.say(")")


    def print_sexp(self, stmt: EXP, d: int):
        self.indent(d)
        self.sayln("EXP(")
        self.print_exp(stmt.exp, d + 1)
        self.say(")")


    def print_exp(self, exp : Exp, d: int):
        if exp is None:
            self.indent(d)
            return None

        if isinstance(exp, BINOP):
            self.print_binop(exp, d)

        elif isinstance(exp, MEM):
            self.print_mem(exp, d)

        elif isinstance(exp, TEMP):
            self.print_temp(exp, d)

        elif isinstance(exp, ESEQ):
            self.print_eseq(exp, d)

        elif isinstance(exp, NAME):
            self.print_name(exp, d)

        elif isinstance(exp, CONST):
            self.print_const(exp, d)

        elif isinstance(exp, CALL):
            self.print_call(exp, d)

        else:
            raise RuntimeError("Print.print_exp()")


    def print_binop(self, exp: BINOP, d: int):
        self.indent(d)
        self.say("BINOP(")

        match(exp.binop):
            case BINOP.PLUS:
                self.say("PLUS")

            case BINOP.MINUS:
                self.say("MINUS")

            case BINOP.MUL:
                self.say("MUL")

            case BINOP.DIV:
                self.say("DIV")

            case BINOP.AND:
                self.say("AND")
            
            case BINOP.OR:
                self.say("OR")

            case BINOP.LSHIFT:
                self.say("LSHIFT")

            case BINOP.RSHIFT:
                self.say("RSHIFT")

            case BINOP.ARSHIFT:
                self.say("ARSHIFT")

            case BINOP.XOR:
                self.say("XOR")

            case _:
                raise RuntimeError("Print.print_binop()")
      
        self.sayln(",")
        self.print_exp(exp.left_exp, d + 1)
        self.sayln(",")
        self.print_exp(exp.right_exp, d + 1)
        self.say(")")


    def print_mem(self, exp: MEM, d: int):
        self.indent(d)
        self.sayln("MEM(")
        self.print_exp(exp.exp, d + 1)
        self.say(")")

    def print_temp(self, exp: TEMP, d: int):
        self.indent(d)
        self.say("TEMP ")
        self.say(self.temp_map.temp_map(exp.temp))

    def print_eseq(self, exp: ESEQ, d: int):
        self.indent(d)
        self.sayln("ESEQ(")
        self.print_stm(exp.stm, d + 1)
        self.sayln(",")
        self.print_exp(exp.exp, d + 1)
        self.say(")")

    def print_name(self, exp: NAME, d: int):
        self.indent(d)
        self.say("NAME ")
        self.say(exp.label.to_string())

    def print_const(self, exp: CONST, d: int):
        self.indent(d)
        self.say("CONST ")
        self.say(str(exp.value))

    def print_call(self, exp: CALL, d: int):
        self.indent(d)
        self.sayln("CALL(")
        self.print_exp(exp.func_exp, d + 1)
        
        exp_list: ExpList = exp.arg_exp_list
        
        while exp_list is not None:
            self.sayln(",")
            self.print_exp(exp_list.head, d + 2)
            exp_list = exp_list.tail

        self.say(")")

    def print_only_stm(self, stmt: Stm):
        self.print_stm(stmt, 0)
        self.say("\n")

    def print_only_exp(self, exp: Exp):
        self.print_exp(exp, 0)
        self.say("\n")