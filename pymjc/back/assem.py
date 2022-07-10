from __future__ import annotations
from abc import ABC, abstractmethod
from ast import match_case
from io import StringIO
from typing import List


from pymjc.front import temp


class Targets():

  def __init__(self, labels: temp.LabelList):
    self.labels = labels

class Instr(ABC):

    @abstractmethod
    def use(self) -> temp.TempList:
        pass

    @abstractmethod
    def deff(self) -> temp.TempList:
        pass

    @abstractmethod
    def jumps(self) -> Targets:
        pass

    def nth_temp(self, temp_list: temp.TempList, i: int) -> temp.Temp:
        if i == 0:
            return temp_list.head
        else:
            return self.nth_temp(temp_list.tail, i - 1)
  

    def nth_label(self, label_list: temp.LabelList, i: int) -> temp.Label:
        if i == 0:
            return label_list.head
        else:
            return self.nth_label(label_list.tail, i - 1)


    def format(self, temp_map: temp.TempMap) -> str:
        dest: temp.TempList = self.deff()
        src: temp.TempList = self.use()
        j: Targets = self.jumps()
        jump: temp.LabelList = None
        if j is not None:
            jump = j.labels

        s: StringIO = StringIO()
        length: int = len(self.assem)
        t: temp.Temp

        for i in len(self.assem):
            if (self.assem[i] == '`'):
                i += 1
                match(self.assem[i]):
                    case 's':
                        i += 1
                        n: int = int(self.assem[i], 10)
                        t = self.nth_temp(src, n)
                        result = temp_map.temp_map(t)
                        if result is not None:
                            s.write(temp_map.temp_map(t))
                        else:
                            s.write(t)

                    case 'd':
                        i += 1
                        n: int = int(self.assem[i], 10)
                        t = self.nth_temp(dest, n)
                        result = temp_map.temp_map(t)
                        if result is not None:
                            s.write(temp_map.temp_map(t))
                        else:
                            s.write(t)

                    case 'j':
                        i += 1
                        n: int = int(self.assem[i], 10)
                        s.write(self.nth_label(jump, t).to_string())

                    case '`':
                        s.write('`')

                    case _:
                        raise RuntimeError("bad Assem format")
            else:
                s.write(self.assem[i])

        return s.getvalue()



class InstrList():
    def __init__(self, head: Instr, tail: InstrList):
        self.head: Instr = head
        self.tail: InstrList = tail
    
    def to_list(self) -> List[Instr]:
        instr_list = List[Instr]
        current_head = self.head
        current_tail = self.tail
        while current_head is not None:
            instr_list.append(current_head)
            if current_tail is not None:
                current_head = current_tail.head
                current_tail = current_tail.tail
            else:
                current_head = None
        return instr_list


class LABEL(Instr):
   def __init__(self, assem: str, label: temp.Label):
      self.assem: str = assem
      self.label: temp.Label = label

   def use(self) -> temp.TempList:
      return None

   def deff(self) -> temp.TempList:
      return None

   def jumps(self) -> Targets:
      return None



class MOVE(Instr):
   def __init__(self, assem: str, dest: temp.Temp, src: temp.Temp):
      self.assem: str = assem
      self.dest: temp.Temp = dest
      self.src: temp.Temp = src 

   def use(self) -> temp.TempList:
      return temp.TempList(self.src, None)

   def deff(self) -> temp.TempList:
      return temp.TempList(self.dest, None)

   def jumps(self) -> Targets:
      return None


class OPER(Instr):
    def __init__(self, assem: str, dest: temp.TempList, src: temp.TempList, j: temp.LabelList = None):
       self.assem: str = assem
       self.dest: temp.TempList = dest
       self.src: temp.TempList = src
       
       if j is not None:
           self.jump = Targets(j)
       else:
           self.jump = None 
    
    def use(self) -> temp.TempList:
        return self.src

    def deff(self) -> temp.TempList:
        return self.dest

    def jumps(self) -> Targets:
        return self.jump