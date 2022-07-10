from __future__ import annotations
from abc import ABC, abstractmethod

from pymjc.front import tree

class CodegenVisitor(ABC):

    @abstractmethod
    def visit_binop(self, element: tree.BINOP) -> str:
        pass

    @abstractmethod
    def visit_call(self, element: tree.CALL) -> str:
        pass

    @abstractmethod
    def visit_cjump(self, element: tree.CJUMP) -> str:
        pass

    @abstractmethod
    def visit_const(self, element: tree.CONST) -> str:
        pass
    
    @abstractmethod
    def visit_eseq(self, element: tree.ESEQ) -> str:
        pass

    @abstractmethod
    def visit_exp(self, element: tree.EXP) -> str:
        pass

    @abstractmethod
    def visit_jump(self, element: tree.JUMP) -> str:
        pass

    @abstractmethod
    def visit_label(self, element: tree.LABEL) -> str:
        pass

    @abstractmethod
    def visit_mem(self, element: tree.MEM) -> str:
        pass

    @abstractmethod
    def visit_move(self, element: tree.MOVE) -> str:
        pass

    @abstractmethod
    def visit_name(self, element: tree.NAME) -> str:
        pass

    @abstractmethod
    def visit_print(self, element: tree.Print) -> str:
        pass

    @abstractmethod
    def visit_seq(self, element: tree.SEQ) -> str:
        pass

    @abstractmethod
    def visit_temp(self, element: tree.TEMP) -> str:
        pass