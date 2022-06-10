from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
from pymjc.back.assem import Instr
from pymjc.front.symbol import Symbol

from pymjc.front.temp import Label, Temp, TempMap
from pymjc.front.tree import Exp, Stm
from pymjc.util import BoolList

class Access(ABC):

    @abstractmethod
    def to_string(self) -> str:
        pass

    @abstractmethod
    def exp(self, exp: Exp) -> Exp:
        pass

class Frame(TempMap):

    @abstractmethod
    def new_frame(self, symbol: Symbol, formal_list: BoolList) -> Frame:
        pass

    @abstractmethod
    def alloc_local(self, escape: bool) -> Access:
        pass

    @abstractmethod
    def FP(self) -> Temp:
        pass

    @abstractmethod
    def  word_size(self) -> int:
        pass

    @abstractmethod
    def external_call(self, func:str, args: List[Exp]) -> Exp:
        pass

    @abstractmethod
    def RV(self) -> Temp:
        pass

    @abstractmethod
    def string(self, label: Label, value: str) -> str:
        pass

    @abstractmethod
    def bad_ptr(self) -> Label:
        pass

    @abstractmethod
    def bad_sub(self) -> Label:
        pass

    @abstractmethod
    def temp_map(self, temp: Temp) -> str:
        pass

    @abstractmethod
    def codegen(self, stmts: List[Stm]) -> List[Instr]:
        pass

    @abstractmethod
    def proc_entry_exit1(self, body: List[Stm]) -> None:
        pass

    @abstractmethod
    def proc_entry_exit2(self, body: List[Instr]) -> None:
        pass

    @abstractmethod
    def proc_entry_exit3(self, body: List[Instr]) -> None:
        pass

    @abstractmethod
    def registers(self) -> List[Temp]:
        pass

    @abstractmethod
    def spill(self, insns: List[Instr], spills: List[Temp]) -> None:
        pass

    @abstractmethod
    def program_tail(self) -> str:
        pass