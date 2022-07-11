from __future__ import annotations
from pymjc.front import temp, tree

class StmListList():

    def __init__(self, head: tree.StmList, tail: StmListList):
        self.head: tree.StmList = head
        self.tail: StmListList = tail


class BasicBlocks():

    def __init__(self, stms: tree.StmList):
        self.done: temp.Label = temp.Label()
        self.mk_blocks(stms)
        self.blocks: StmListList = None
        self.last_block: StmListList = None
        self.last_stm: tree.StmList = None

    def add_stm(self, stm: tree.Stm) -> None:
        self.last_stm = self.last_stm.tail = tree.StmList(stm, None)

    def do_stms(self, stm_list: tree.StmList) -> None:
        if (stm_list is None):
            self.do_stms(tree.StmList(tree.JUMP(self.done), None))
        elif (isinstance(stm_list.head, tree.JUMP) or isinstance(stm_list.head, tree.CJUMP)):
            self.add_stm(stm_list.head)
            self.mk_blocks(stm_list.tail)
        elif (isinstance(stm_list.head, tree.LABEL)):
            self.do_stms(tree.StmList(tree.JUMP(stm_list.head.label), stm_list))
        else:
            self.add_stm(stm_list.head)
            self.do_stms(stm_list.tail)


    def mk_blocks(self, stm_list: tree.StmList) -> None:
        if (stm_list is None):
            return None
        elif (isinstance(stm_list.head, tree.LABEL)):
            self.last_stm = tree.StmList(stm_list.head, None)
            if (self.last_block is None):
                self.last_block = self.blocks = StmListList(self.last_stm, None)
            else:
                self.last_block = self.last_block.tail = StmListList(self.last_stm, None)
            self.do_stms(stm_list.tail)
        else:
            self.mk_blocks(tree.StmList(tree.LABEL(temp.Label()), stm_list))




class MoveCall(tree.Stm):

    def __init__(self, dst: tree.TEMP, src: tree.CALL):
        self.dst: tree.TEMP = dst
        self.src: tree.CALL = src

    def kids(self) -> tree.ExpList:
        return self.src.kids()

    def build(self, kids: tree.ExpList) -> tree.Stm:
        return tree.MOVE(self.dst, self.src.build(kids))


class ExpCall (tree.Stm):
    def __init__(self, call: tree.CALL):
        self.call: tree.CALL = call

    def kids(self) -> tree.ExpList:
        return self.call.kids()

    def build(self, kids: tree.ExpList) -> tree.Stm:
        return tree.EXP(self.call.build(kids))
    

class StmExpList ():

    def __init__(self, stm: tree.Stm, exps: tree.ExpList):
        self.stm: tree.Stm = stm
        self.exps: tree.ExpList = exps
    

class Canon():

    def is_nop(a: tree.Stm) -> bool:
        return isinstance(a, tree.EXP) and isinstance(a.exp, tree.CONST)

    def seq(a: tree.Stm, b: tree.Stm) -> tree.Stm:
        if (Canon.is_nop(a)):
            return b
        elif (Canon.is_nop(b)):
            return a
        else:
            return tree.SEQ(a, b)

    def commute(a: tree.Stm, b: tree.Exp) -> bool:
        return Canon.is_nop(a) or isinstance(b,tree.NAME) or isinstance(b, tree.CONST)

    def do_stm(s: tree.Stm) -> tree.Stm:
        if (isinstance(s, tree.SEQ)):
            return Canon.do_stm_seq(s)
        elif (isinstance(s, tree.MOVE)):
            return Canon.do_stm_move(s)
        elif (isinstance(s, tree.EXP)):
            return Canon.do_stm_exp(s)
        else:
            return Canon.reorder_stm(s)


    def do_stm_seq(s: tree.SEQ) -> tree.Stm:
        return Canon.seq(Canon.do_stm(s.left), Canon.do_stm(s.right))

    def do_stm_move(s: tree.MOVE) -> tree.Stm:
        if (isinstance(s.dst, tree.TEMP) and isinstance(s.src, tree.CALL)):
            return Canon.reorder_stm(MoveCall(s.dst, s.src))
        elif (isinstance(s.dst, tree.ESEQ)):
            return Canon.do_stm(tree.SEQ(s.dst.stm, tree.MOVE(s.dst.exp, s.src)))
        else:
            return Canon.reorder_stm(s)

    def do_stm_exp(s: tree.EXP) -> tree.Stm:
        if (isinstance(s.exp, tree.CALL)):
            return Canon.reorder_stm(ExpCall(s.exp))
        else:
            return Canon.reorder_stm(s)



    def reorder_stm(s: tree.Stm) -> tree.Stm:
        x: StmExpList = Canon.reorder(s.kids())
        return Canon.seq(x.stm, s.build(x.exps))

    def do_exp(e: tree.Exp) -> tree.ESEQ:
        if (isinstance(e, tree.ESEQ)):
            return Canon.do_exp_eseq(e)
        else:
            return Canon.reorder_exp(e)

    def do_exp_eseq(e: tree.ESEQ) -> tree.ESEQ:
        stms: tree.Stm = Canon.do_stm(e.stm)
        b: tree.ESEQ = Canon.do_exp(e.exp)
        return tree.ESEQ(Canon.seq(stms, b.stm), b.exp)


    def reorder_exp(e: tree.Exp) -> tree.ESEQ:
        x: StmExpList  = Canon.reorder(e.kids())
        return tree.ESEQ(x.stm, e.build(x.exps))

    nop_null: StmExpList = StmExpList(tree.EXP(tree.CONST(0)), None)

    def reorder(exps: tree.ExpList) -> StmExpList:
        if (exps is None):
            return Canon.nop_null
        else:
            a: tree.Exp = exps.head
            if (isinstance(a, tree.CALL)):
                t: temp.Temp = temp.Temp()
                e: tree.Exp = tree.ESEQ(tree.MOVE(tree.TEMP(t), a), tree.TEMP(t))
                return Canon.reorder(tree.ExpList(e, exps.tail))
            else:
                aa: tree.ESEQ = Canon.do_exp(a)
                bb: StmExpList  = Canon.reorder(exps.tail)
                if (Canon.commute(bb.stm, aa.exp)):
                    return StmExpList(Canon.seq(aa.stm, bb.stm), tree.ExpList(aa.exp, bb.exps))
                else:
                    t: temp.Temp = temp.Temp()
                    return StmExpList(Canon.seq(aa.stm, Canon.seq(tree.MOVE(tree.TEMP(t), aa.exp), bb.stm)), tree.ExpList(tree.TEMP(t), bb.exps))


    def linear(s: tree.Stm, l: tree.StmList) -> tree.StmList:
        if (isinstance(s, tree.SEQ)):
            return Canon.linear_seq(s, l)
        else:
            return tree.StmList(s, l)

    def linear_seq(s: tree.SEQ, l: tree.StmList) -> tree.StmList:
        return Canon.linear(s.left, Canon.linear(s.right, l))


    def linearize(s: tree.Stm) -> tree.StmList:
        return Canon.linear(Canon.do_stm(s), None)



class TraceSchedule():

    def __init__(self, the_blocks: BasicBlocks):
        self.stms: tree.StmList = None
        self.the_blocks: BasicBlocks = the_blocks
        self.table = {}
        stm_list: StmListList = the_blocks.blocks 
        
        while(stm_list is not None):
            if(isinstance(stm_list.head.head, tree.LABEL)):
                self.table[stm_list.head.head.label.to_string()] = stm_list.head
        
        self.stms = self.get_next()
        self.table = None
        


    def get_last(self, block: tree.StmList) -> tree.StmList:
        l: tree.StmList = block
        while (l.tail.tail is not None):
            l = l.tail
        return l

    def trace(self, l: tree.StmList) -> None:
        while True:
            lab: tree.LABEL = l.head
            self.table.pop(lab.label)
            last: tree.StmList = self.get_last(l)
            s: tree.Stm = last.tail.head
            if (isinstance(s, tree.JUMP)):
                target: tree.StmList = self.table.get(s.targets.head)
                if (s.targets.tail is None and target is not None):
                    last.tail = target
                    l = target
                else:
                    last.tail.tail = self.get_next()
                    return None

            elif (isinstance(s, tree.CJUMP)):
                t: tree.StmList = self.table.get(s.if_true)
                f: tree.StmList = self.table.get(s.if_false)
                if (f is not None):
                    last.tail.tail = f
                    l = f
                elif (t is not None):
                    last.tail.head = tree.CJUMP(tree.CJUMP.not_rel(s.rel_op), s.left_exp, s.right_exp, s.if_false, s.if_true)
                    last.tail.tail = t
                    l = t
                else:
                    ff: temp.Label = temp.Label()
                    last.tail.head = tree.CJUMP(s.rel_op, s.left_exp, s.right_exp, s.if_true, ff)
                    last.tail.tail = tree.StmList(tree.LABEL(ff), tree.StmList(tree.JUMP(s.if_false), self.get_next()))
                    return None
            else:
                raise RuntimeError("Bad basic block in TraceSchedule")


    def get_next(self) -> tree.StmList:
        if (self.the_blocks.blocks is None):
            return tree.StmList(tree.LABEL(self.the_blocks.done), None)
        else:
            s: tree.StmList = self.the_blocks.blocks.head
            lab: tree.LABEL = s.head
            if (self.table.get(lab.label) is not None):
                self.trace(s)
                return s
            else:
                self.the_blocks.blocks = self.the_blocks.blocks.tail
                return self.get_next()