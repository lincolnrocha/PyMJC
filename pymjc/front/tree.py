from __future__ import annotations
from abc import ABC, abstractmethod

from pymjc.front.temp import Label, LabelList, Temp


class Exp(ABC):

    @abstractmethod
    def kids(self) -> ExpList:
        pass

    @abstractmethod
    def build(self, kids: ExpList) -> Exp:
        pass

class ExpList():
    def __init__(self, head: Exp, tail: ExpList):
        self.head: Exp = head
        self.tail: ExpList = tail

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
    def __init__(self, func_exp: Exp, args_exp: ExpList):
        self.func_exp: Exp = func_exp
        self.args_exp: ExpList = args_exp

    def kids(self) -> ExpList:
        return ExpList(self.func_exp, self.args_exp)

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



