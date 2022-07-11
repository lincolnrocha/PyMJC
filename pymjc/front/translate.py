from __future__ import annotations
from abc import ABC, abstractmethod

from pymjc.front import frame, temp, tree


class Exp(ABC):

    @abstractmethod
    def un_ex(self) -> tree.Exp:
        pass

    @abstractmethod
    def un_nx(self) -> tree.Stm:
        pass

    @abstractmethod
    def un_cx(self, true_label: temp.Label, false_label: temp.Label) -> tree.Stm:
        pass

class Ex(Exp):
    def __init__(self, exp: tree.Exp):
        self.exp: tree.Exp = exp

    def un_ex(self) -> tree.Exp:
        return self.exp
     
    def un_nx(self) -> tree.Stm:
        return tree.EXP(self.exp)

    def un_cx(self, true_label: temp.Label, false_label: temp.Label) -> tree.Stm:
        # if the exp is a constant, emit JUMP statement.
        if (isinstance(self.exp, tree.CONST)):
            if (self.exp.value == 0):
                return tree.JUMP(false_label)
            else:
                return tree.JUMP(true_label)
        return tree.CJUMP(tree.CJUMP.NE, self.exp, tree.CONST(0), true_label, false_label)        

class Cx(Exp):
    def un_ex(self) -> tree.Exp:
        register: temp.Temp = temp.Temp()
        true_label: temp.Label = temp.Label()
        false_label: temp.Label = temp.Label()
        
        return tree.ESEQ(
            tree.SEQ (
                tree.MOVE(
                    tree.TEMP(register), 
                    tree.CONST(1)), 
                    tree.SEQ(
                        self.un_cx(true_label, false_label),
                        tree.SEQ(
                            tree.LABEL(false_label),
                            tree.SEQ(
                                tree.MOVE(
                                    tree.TEMP(register), 
                                    tree.CONST(0)), 
                                    tree.LABEL(true_label))))),
                                    tree.TEMP(register))
    

    def un_nx(self) -> tree.Stm:
        join: temp.Label = temp.Label()
        return tree.SEQ(self.un_cx(join, join), tree.LABEL(join))

    @abstractmethod
    def un_cx(self, true_label: temp.Label, false_label: temp.Label) -> tree.Stm:
        pass

class RelCx(Cx):
    def __init__(self, opration: int, left: tree.Exp, right: tree.Exp):
        self.opration: int = opration
        self.left_side: tree.Exp = left
        self.rigth_side: tree.Exp = right

    def un_cx(self, true_label: temp.Label, false_label: temp.Label) -> tree.Stm:
        return tree.CJUMP(self.opration, self.left_side, self.rigth_side, true_label, false_label)


class Nx(Exp):
    def __init__(self, stm: tree.Stm):
        self.stm: tree.Stm = stm

    def un_ex(self) -> tree.Exp:
        return None
     
    def un_nx(self) -> tree.Stm:
        return self.stm

    def un_cx(self, true_label: temp.Label, false_label: temp.Label) -> tree.Stm:
        return None


class IfThenElseExp(Exp):
    def __init__(self, condition: Exp, if_expression: Exp, else_expression: Exp):
        self.condition: Exp = condition
        self.if_expression: Exp = if_expression
        self.else_expression: Exp = else_expression
        self.true_label = temp.Label()
        self.false_label = temp.Label()
        self.join_label = temp.Label()

    def __SEQ(left: tree.Stm , right: tree.Stm ) -> tree.Stm :
        if (left is None):
            return right
        if (right is None):
            return left

        return tree.SEQ(left, right)
    
    def __LABEL(label: temp.Label) -> tree.LABEL: 
        return tree.LABEL(label)

    def __ESEQ(stm: tree.Stm , exp: tree.Exp) -> tree.Exp:
        if (stm is None): 
            return exp
        
        return tree.ESEQ(stm, exp)

    def __MOVE(dst: tree.Exp, src: tree.Exp) -> tree.Stm:
        return tree.MOVE(dst, src)
    
    def __JUMP(label: temp.Label)  -> tree.Stm: 
        return tree.JUMP(label)
    
    def __TEMP(temp: temp.Temp)  -> tree.Exp: 
        return tree.TEMP(temp)


    def un_cx(self, t_label: temp.Label, f_label: temp.Label) -> tree.Stm:
        if_stm: tree.Stm  = self.if_expression.un_cx(t_label, f_label)
        
        if (isinstance(if_stm, tree.JUMP)):
            if(isinstance(if_stm.exp, tree.NAME)):
                self.true_label = if_stm.exp.label
                if_stm = None

        else_stm: tree.Stm  = self.else_expression.un_cx(t_label, f_label)
        
        if (isinstance(else_stm, tree.JUMP)):
            if(isinstance(else_stm.exp, tree.NAME)):
                self.false_label = else_stm.exp.label
                else_stm = None
        

        cond_stm: tree.Stm = self.condition.un_cx(self.true_label, self.false_label)

        if (if_stm is None and else_stm is None):
            return cond_stm
        
        if (if_stm is None):
            return IfThenElseExp.__SEQ(cond_stm, IfThenElseExp.__SEQ(IfThenElseExp.__LABEL(self.false_label), else_stm))

        if(else_stm is None):
            return IfThenElseExp.__SEQ(cond_stm, IfThenElseExp.__SEQ(IfThenElseExp.__LABEL(self.true_label), if_stm))

             
        return IfThenElseExp.__SEQ(cond_stm, 
                    IfThenElseExp.__SEQ(
                        IfThenElseExp.__SEQ(
                            IfThenElseExp.__LABEL(self.true_label), if_stm), 
                        IfThenElseExp.__SEQ(
                            IfThenElseExp.__LABEL(self.true_label), else_stm)))


    def un_ex(self) -> tree.Exp:
        if_exp: tree.Exp  = self.if_expression.un_ex()
        if if_exp is None:
            return None


        else_exp: tree.Exp  = self.else_expression.un_ex()
        if else_exp is None:
            return None

        register: temp.Temp = temp.Temp()


        return IfThenElseExp.__ESEQ(IfThenElseExp.__SEQ(IfThenElseExp.__SEQ(self.condition.un_cx(self.true_label, self.false_label),
                    IfThenElseExp.__SEQ(IfThenElseExp.__SEQ(IfThenElseExp.__LABEL(self.true_label),
                        IfThenElseExp.__SEQ(IfThenElseExp.__MOVE(IfThenElseExp.__TEMP(register), if_exp),
                        IfThenElseExp.__JUMP(self.join_label))),
                    IfThenElseExp.__SEQ(IfThenElseExp.__LABEL(self.false_label),
                        IfThenElseExp.__SEQ(IfThenElseExp.__MOVE(IfThenElseExp.__TEMP(register), else_exp),
                        IfThenElseExp.__JUMP(self.join_label))))),
                IfThenElseExp.__LABEL(self.join_label)),
                IfThenElseExp.__TEMP(register))
    
    
    def un_nx(self) -> tree.Stm:
        if_stm = self.if_expression.un_nx()
        if (if_stm is None):
            self.true_label = self.join_label
        else:
            if_stm = IfThenElseExp.__SEQ(IfThenElseExp.__SEQ(IfThenElseExp.__LABEL(self.true_label), if_stm), IfThenElseExp.__JUMP(self.join_label))

        else_stm = self.else_expression.un_nx()
        if (if_stm is None):
            self.false_label = self.join_label
        else:
            else_stm = IfThenElseExp.__SEQ(IfThenElseExp.__SEQ(IfThenElseExp.__LABEL(self.false_label), else_stm), IfThenElseExp.__JUMP(self.join_label))

        if (if_stm is None and else_stm is None):
            return self.condition.un_nx()

        cond_stm: tree.Stm = self.condition.un_cx(self.true_label, self.false_label)

        if (if_stm is None):
            return IfThenElseExp.__SEQ(IfThenElseExp.__SEQ(cond_stm, else_stm), IfThenElseExp.__LABEL(self.join_label))

        if (else_stm is None):
            return IfThenElseExp.__SEQ(IfThenElseExp.__SEQ(cond_stm, if_stm), IfThenElseExp.__LABEL(self.join_label))

        return IfThenElseExp.__SEQ(IfThenElseExp.__SEQ(cond_stm, IfThenElseExp.__SEQ(if_stm, else_stm)), IfThenElseExp.__LABEL(self.join_label))
    

class Frag():
    def __init__(self, frag: Frag = None):
        self.nex: Frag = frag

    def add_next(self, next: Frag) -> None:
        self.next = next

    def get_next(self) -> Frag:
        return self.next


class ProcFrag (Frag):

    def __init__(self, stmt: tree.Stm, frame: frame.Frame):
        self.body: tree.Stm = stmt
        self.frame: frame.Frame = frame

class DataFrag (Frag):

    def __init__(self, data: str):
        self.data: str = data
    
    def to_string(self) -> str:
        return self.data