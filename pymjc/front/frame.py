from __future__ import annotations
from abc import ABC, abstractmethod
from pymjc.front.symbol import Symbol

from pymjc.front.temp import Label, TempMap
from pymjc.front.tree import Exp
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
    def new_frame(self, symbols: Symbol, formal_list: BoolList) -> Frame:
        pass