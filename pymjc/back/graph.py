from __future__ import annotations
import sys

class Node():
    
    def __init__(self, graph: Graph):
      self.succs: NodeList = None
      self.preds: NodeList = None
      self.my_graph: Graph = graph
      self.my_key = graph.node_count
      graph.node_count += 1
      p: NodeList  = NodeList(self, None)
      if (graph.mylast is None):
          graph.mynodes = graph.mylast = p
      else:
          graph.mylast = graph.mylast.tail = p

    def succ(self) -> NodeList:
        return self.succs

    def pred(self) -> NodeList:
        return self.preds

    def cat(self, a: NodeList, b: NodeList) -> NodeList:
        if (a is None):
            return b
        else:
            return NodeList(a.head, self.cat(a.tail, b))

    def adj(self) -> NodeList:
        return self.cat(self.succ(), self.pred())

    def len_note_list(self, l: NodeList) -> int:
        i: int = 0
        p: NodeList = l
        while(p is not None):
          p = p.tail
          i += 1

        return i

    def in_degree(self) -> int:
        return self.len_note_list(self.pred())

    def out_degree(self) -> int:
        return self.len_note_list(self.succ())

    def degree(self) -> int:
        return self.in_degree() + self.out_degree()

    def goes_to(self, n: Node) -> bool:
        return Graph.in_list(n, self.succ())

    def comes_from(self, n: Node) -> bool:
        return Graph.in_list(n, self.pred())

    def adj(self, n: Node) -> bool:
        return self.goes_to(n) or self.comes_from(n)

    def to_string(self) -> str:
        return str(self.mykey)

class NodeList():
  def __init__(self, h: Node, t: NodeList):
    self.head: Node = h
    self.tail: NodeList = t


class Graph():
  def __init__(self):
    self.node_count = 0
    self.mynodes: NodeList = None 
    self.mylast: NodeList = None

  def nodes(self) -> NodeList:
    return self.mynodes

  def new_node(self) -> Node:
    return Node(self)

  def check(self, n: Node) -> None:
    if (n.mygraph is not self):
      raise RuntimeError("Graph.addEdge using nodes from the wrong graph")

  def in_list(a: Node , l: NodeList) -> bool:
    p: NodeList = l
    while(p is not None):
      if (p.head is a):
        return True      
      p = p.tail

    return False

  def add_edge(self, from_node: Node , to_node: Node) -> None:
    self.check(from_node)
    self.check(to_node)
    if (from_node.goes_to(to_node)):
      return None
    to_node.preds = NodeList(from_node, to_node.preds)
    from_node.succs = NodeList(to_node, from_node.succs)

  def delete_node(self, a: Node, l: NodeList) -> NodeList:
    if (l is None):
      raise RuntimeError("Graph.rmEdge: edge nonexistent")
    elif (a is l.head):
      return l.tail
    else:
      return NodeList(l.head, self.delete_node(a, l.tail))

  def rm_edge(self, from_node: Node, to_node: Node) -> None:
    to_node.preds = self.delete_node(from_node, to_node.preds)
    from_node.succs = self.delete_node(to_node, from_node.succs)

   #Print a human-readable dump for debugging.
  def show(self, out_path: str) -> None:
    if out_path is not None:
        sys.stdout = open(out_path, 'w')
    p: NodeList = self.nodes()
    while(p is not None):
      n: Node  = p.head
      print(n.to_string)
      q: NodeList = n.succ()
      print(": ")
      while(q is not None):
        print(q.head.to_string())
        print(" ")
        q = q.tail
      print("\n")
      p = p.tail