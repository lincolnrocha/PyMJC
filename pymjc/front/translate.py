from __future__ import annotations

from pymjc.front import frame
from pymjc.front import tree


class Exp():
    def __init__(self, exp: tree.Exp):
        self.exp: tree.Exp = exp

    def un_ex(self) -> tree.Exp:
        return self.exp

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