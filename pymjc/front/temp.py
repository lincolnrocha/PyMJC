from __future__ import annotations
from abc import ABC, abstractmethod

from pymjc.front.symbol import Symbol

class Temp():
    count: int = 0

    def __init__(self):
        self.number = Temp.count
        Temp.count += 1

    def to_string(self) -> str:
        return "t" + str(self.number)


class TempList():
    
    def __init__(self, head: Temp = None, tail: TempList = None):
        self.head: Temp = head
        self.tail: TempList = tail
    
    def add_head(self, element: Temp):
        self.tail = TempList(self.head, self.tail)
        self.head = element
    
    def add_tail(self, element: Temp):
        if self.head is None:
            self.head = element
        else:
            last: TempList = self.tail
            while last is not None:
                last = last.tail
            last.tail = TempList(element, None)

        


class TempMap(ABC):

    @abstractmethod
    def temp_map(self, temp: Temp) -> str:
        pass

class DefaultMap(TempMap):

    def temp_map(self, temp: Temp) -> str:
        return temp.to_string()


class CombineMap(TempMap):

    def __init__(self, temp_map1: TempMap, temp_map2: TempMap):
        self.temp_map1 = temp_map1
        self.temp_map2 = temp_map2
        
    def temp_map(self, temp: Temp) -> str:
        mapping = self.temp_map1.temp_map(temp)
        
        if(mapping is not None):
            return mapping
        
        return self.temp_map2.temp_map(temp)


class Label():

    count: int = 0

    def __init__(self, name: str = None, symbol: Symbol = None):
        if name is not None:
            self.name = name
        elif symbol is not None:
            self.name = symbol.to_string()
        else:
            self.name = "L" + str(Label.count)
            Label.count += 1
    
    def to_string(self) -> str:
        return self.name 


class LabelList():

    def __init__(self, head: Label, tail: LabelList):
        self.head: Label = head
        self.tail: LabelList = tail    