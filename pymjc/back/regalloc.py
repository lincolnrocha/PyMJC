from __future__ import annotations
from abc import abstractmethod
from pymjc.back import graph
from pymjc.back import flowgraph
from pymjc.front import temp

class Color(temp.TempMap):
    def __init__(self, ig: InterferenceGraph, initial: temp.TempMap, registers: temp.TempList):
        pass
    
    def spills(self) -> temp.TempList:
        return None

    def temp_map(self, temp: temp.Temp) -> str:
        return temp.to_string()

class InterferenceGraph(graph.Graph):
    
    @abstractmethod
    def tnode(self, temp:temp.Temp) -> graph.Node:
        pass

    @abstractmethod
    def gtemp(self, node: graph.Node) -> temp.Temp:
        pass

    @abstractmethod
    def moves(self) -> MoveList:
        pass
    
    def spill_cost(self, node: graph.Node) -> int:
      return 1


class Liveness (InterferenceGraph):

    def __init__(self, flow: flowgraph.FlowGraph):
        self.live_map = {}


    def tnode(self, temp:temp.Temp) -> graph.Node:
        return None


    def gtemp(self, node: graph.Node) -> temp.Temp:
        return None

    def moves(self) -> MoveList:
        return None


class MoveList():

   def __init__(self, s: graph.Node, d: graph.Node, t: MoveList):
      self.src: graph.Node = s
      self.dst: graph.Node = d
      self.tail: MoveList = t
