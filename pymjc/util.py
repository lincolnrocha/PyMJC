from typing import List
from pymjc.front import tree

class BoolList():
    def __init__(self):
        self.list: list = []
    
    def add_bool(self, value: bool):
        self.list.append(value)

    def get_list(self) -> list:
        return self.list

class Converter():

    def to_SEQ(list: List[tree.Stm])-> tree.Stm:
        seq = tree.SEQ(list[0], list[1])
        for i in range(2, len(list)):
            seq = tree.SEQ(list.get(i), seq)
        return seq

    def to_ExpList(list: List[tree.Exp])-> tree.ExpList:
        exp_list: tree.ExpList = None
        for i in range(len(list)):
            exp_list = tree.ExpList(list.get(i), exp_list)
        return exp_list