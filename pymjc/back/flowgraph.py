from __future__ import annotations
from abc import abstractmethod
import sys
from typing import List
from pymjc.back import assem, graph
from pymjc.front import temp, tree

class FlowGraph (graph.Graph):
    
    @abstractmethod
    def deff(self,  node:graph.Node) -> temp.TempList:
        pass

    @abstractmethod
    def use(self,  node:graph.Node) -> temp.TempList:
        pass

    @abstractmethod
    def is_move(self,  node:graph.Node) -> bool:
        pass

    def show(self, out_path: str = None) -> None:
        #sys.stdout
        if out_path is not None:
            sys.stdout = open(out_path, 'w')
        node_list: graph.NodeList = self.nodes()

        while(node_list is not None):
            node: graph.Node = node_list.head
            print(node.to_string())
            print(": ")

            def_list: temp.TempList = self.deff(node)
            while(def_list is not None):
                print(def_list.head.to_string())
                print(" ")
                def_list = def_list.tail

            if self.is_move(node) is True:
                print("<= ")
            else:
                print("<- ")

            use_list: temp.TempList = self.use(node)
            while(use_list is not None):
                print(use_list.head.to_string())
                print(" ")
                use_list = use_list.tail

            print("; goto ")

            succ_list : graph.NodeList = node.succ()
            while (succ_list is not None):
                print(succ_list.head.to_string())
                print(" ")
                succ_list = succ_list.tail

            print("\n")
            node_list = node_list.tail


class AssemFlowGraph (FlowGraph):
    def __init__(self, instrs: assem.InstrList):
        self.instructions = {}
        self.labels = {}
        self.mapping =  {}

        node: graph.Node = None
        last_node: graph.Node = None
        label_instr: assem.Instr = None
        branch_instr: assem.Instr = None
        
        label_list = List[assem.Instr]
        a: assem.InstrList = instrs

        while(a is not None):
            if (isinstance(a.head, tree.LABEL)):
                label_instr = a.head
                label_list.append(a.head)
            else:
                node = self.new_node()
                branch_instr = a.head
                self.instructions[node] = branch_instr

                if (label_instr is not None):
                    self.labels[node] = label_instr.label
                    for l in label_list:
                        self.mapping[l.label] = node
                    
                    label_list = List[assem.Instr]
                    label_instr = None
                
                if (last_node is not None):
                    self.add_edge(last_node, node)
                
                last_node = node
            
            a = a.tail
        
        i:int = 0
        a = instrs
        while (a is not None): #looking for jump labels
            if (isinstance(a.head, assem.OPER)):
                oper = a.head
                if (oper.jumps() is not None): #if the flow changes
                    jump_labels: temp.LabelList = oper.jumps().labels
                    while(jump_labels is not None):
                        l: temp.Label = jump_labels.head
                        if (self.mapping.get(l) is None):
                            self.add_edge(self.get_node_by_id(i), last_node)
                        else:
                            self.add_edge(self.get_node_by_id(i), self.mapping.get(l))
                        jump_labels = jump_labels.tail
                i += 1
            a = a.tail

    def get_node_by_id(self, n: int) -> graph.Node:
        node_list: graph.NodeList = self.nodes()
        while(node_list is not None):
            if node_list.head.my_key is n:
                return node_list.head
            node_list = node_list.tail
        print("NODE ID NOT FOUND")
        return None

    def instr(self, node: graph.Node) -> assem.Instr: 
        return self.instructions.get(node)

    def deff(self, node: graph.Node) -> temp.TempList:
        deff_instr: assem.Instr = self.instructions.get(node)
        if deff_instr is not None:
            return deff_instr.deff()

        return None
	
    def use(self, node: graph.Node) -> temp.TempList:
        use_instr: assem.Instr = self.instructions.get(node)
        if use_instr is not None:
            return use_instr.use()
        return None
	
    def is_move(self, node: graph.Node) -> bool:
        return isinstance(self.instructions.get(node), assem.MOVE)
