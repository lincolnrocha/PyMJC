from __future__ import annotations
from turtle import st

from pymjc.front.frame import Frame
from pymjc.front.tree import Exp, Stm


class ExpT():
    def __init__(self, exp: Exp):
        self.exp: Exp = exp

    def un_ex(self) -> Exp:
        return self.exp

class Frag():
    def __init__(self, frag: Frag = None):
        self.nex: Frag = frag

    def add_next(self, next: Frag) -> None:
        self.next = next

    def get_next(self) -> Frag:
        return self.next

class ProcFrag (Frag):

    def __init__(self, stmt: Stm, frame: Frame):
        self.body: Stm = stmt
        self.frame: Frame = frame

class DataFrag (Frag):

    def __init__(self, data: str):
        self.data: str = data
    
    def to_string(self) -> str:
        return self.data