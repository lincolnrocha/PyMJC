from __future__ import annotations
from abc import ABC, abstractmethod

from pymjc.front.visitorkinds import *
from pymjc.front import translate

class Component(ABC):
    @abstractmethod
    def accept(self, visitor: Visitor) -> None:
        pass

    @abstractmethod
    def accept_type(self, visitor: TypeVisitor) -> Type:
        pass

    @abstractmethod
    def accept_ir(self, visitor: IRVisitor) -> translate.Exp:
        pass

class Program(Component):
    def __init__(self, main_class: MainClass, class_decl_list: ClassDeclList):
        self.main_class = main_class
        self.class_decl_list = class_decl_list
    
    def accept(self, visitor: Visitor) -> None:
        visitor.visit_program(self)

    def accept_type(self, visitor: TypeVisitor) -> Type:
        return visitor.visit_program(self)
    
    def accept_ir(self, visitor: IRVisitor) -> translate.Exp:
        return visitor.visit_program(self)

class MainClass(Component):
    def __init__(self, class_name_id: Identifier, arg_name_id: Identifier, statement: Statement) -> None:
        self.class_name_id = class_name_id
        self.arg_name_id = arg_name_id
        self.statement = statement

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_main_class(self)

    def accept_type(self, visitor: TypeVisitor) -> Type:
        return visitor.visit_main_class(self)

    def accept_ir(self, visitor: IRVisitor) -> translate.Exp:
        return visitor.visit_main_class(self)

class ClassDecl(Component):

    @abstractmethod
    def accept(self, visitor: Visitor) -> None:
        pass

    @abstractmethod
    def accept_type(self, visitor: TypeVisitor) -> Type:
        pass

    @abstractmethod
    def accept_ir(self, visitor: IRVisitor) -> translate.Exp:
        pass


class ClassDeclList():
    def __init__(self):
        self.class_decl_list = []
    
    def add_element(self, element: ClassDecl) -> None: 
      self.class_decl_list.append(element)

    def element_at(self, index: int) -> ClassDecl: 
      return self.class_decl_list[index]

    def get_elements(self): 
      return self.class_decl_list

    def size(self) -> int: 
      return len(self.class_decl_list)

class ClassDeclExtends(ClassDecl):
    def __init__(self, class_name_id: Identifier, super_class_name_id: Identifier, var_decl_list: VarDeclList, method_decl_list: MethodDeclList):
        self.class_name_id = class_name_id
        self.super_class_name_id = super_class_name_id
        self.var_decl_list = var_decl_list
        self.method_decl_list = method_decl_list

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_class_decl_extends(self)

    def accept_type(self, visitor: TypeVisitor) -> Type:
        return visitor.visit_class_decl_extends(self)

    def accept_ir(self, visitor: IRVisitor) -> translate.Exp:
        return visitor.visit_class_decl_extends(self)


class ClassDeclSimple(ClassDecl):
    def __init__(self, class_name_id: Identifier, var_decl_list: VarDeclList, method_decl_list: MethodDeclList):
        self.class_name_id = class_name_id
        self.var_decl_list = var_decl_list
        self.method_decl_list = method_decl_list

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_class_decl_simple(self)

    def accept_type(self, visitor: TypeVisitor) -> Type:
        return visitor.visit_class_decl_simple(self)

    def accept_ir(self, visitor: IRVisitor) -> translate.Exp:
        return visitor.visit_class_decl_simple(self)

class VarDecl(Component):
    def __init__(self, type: Type, name_id: Identifier):
        self.type = type
        self.name_id = name_id

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_var_decl(self)

    def accept_type(self, visitor: TypeVisitor) -> Type:
        return visitor.visit_var_decl(self)

    def accept_ir(self, visitor: IRVisitor) -> translate.Exp:
        return visitor.visit_var_decl(self)

class VarDeclList():
    def __init__(self):
        self.var_decl_list = []
    
    def add_element(self, element: VarDecl) -> None: 
      self.var_decl_list.append(element)

    def element_at(self, index: int) -> VarDecl: 
      return self.var_decl_list[index]

    def get_elements(self): 
      return self.var_decl_list    

    def size(self) -> int: 
      return len(self.var_decl_list)


class MethodDecl(Component):
    def __init__(self, type: Type, name_id: Identifier, formal_param_list: FormalList, var_decl_list: VarDeclList, statement_list: StatementList, return_exp: Exp):
        self.type = type
        self.name_id = name_id
        self.formal_param_list = formal_param_list
        self.var_decl_list = var_decl_list
        self.statement_list = statement_list
        self.return_exp = return_exp

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_method_decl(self)

    def accept_type(self, visitor: TypeVisitor) -> Type:
        return visitor.visit_method_decl(self)

    def accept_ir(self, visitor: IRVisitor) -> translate.Exp:
        return visitor.visit_method_decl(self)

class MethodDeclList():
    def __init__(self):
        self.method_decl_list = []
    
    def add_element(self, element: MethodDecl) -> None: 
      self.method_decl_list.append(element)

    def element_at(self, index: int) -> MethodDecl: 
      return self.method_decl_list[index]

    def get_elements(self): 
      return self.method_decl_list

    def size(self) -> int: 
      return len(self.method_decl_list)


class Formal(Component):
    def __init__(self, type: Type, name_id: Identifier):
        self.type = type
        self.name_id = name_id

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_formal(self)

    def accept_type(self, visitor: TypeVisitor) -> Type:
        return visitor.visit_formal(self)

    def accept_ir(self, visitor: IRVisitor) -> translate.Exp:
        return visitor.visit_formal(self)

class FormalList():
    def __init__(self):
        self.formal_list = []
    
    def add_element(self, element: Formal) -> None: 
      self.formal_list.append(element)

    def element_at(self, index: int) -> Formal: 
      return self.formal_list[index]

    def get_elements(self): 
      return self.formal_list

    def size(self) -> int: 
      return len(self.formal_list)


class Statement(Component):

    @abstractmethod
    def accept(self, visitor: Visitor) -> None:
        pass

    @abstractmethod
    def accept_type(self, visitor: TypeVisitor) -> Type:
        pass

    @abstractmethod    
    def accept_ir(self, visitor: IRVisitor) -> translate.Exp:
        pass

class StatementList():
    def __init__(self):
        self.statement_list = []
    
    def add_element(self, element: Statement) -> None: 
      self.statement_list.append(element)

    def element_at(self, index: int) -> Statement: 
      return self.statement_list[index]

    def get_element(self): 
      return self.statement_list

    def size(self) -> int: 
      return len(self.statement_list)


class Print(Statement):
    def __init__(self, print_exp: Exp):
        self.print_exp = print_exp

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_print(self)

    def accept_type(self, visitor: TypeVisitor) -> Type:
        return visitor.visit_print(self)

    def accept_ir(self, visitor: IRVisitor) -> translate.Exp:
        return visitor.visit_print(self)

class If(Statement):
    def __init__(self, condition_exp: Exp, if_statement: Statement, else_statement: Statement):
        self.condition_exp = condition_exp
        self.if_statement = if_statement
        self.else_statement = else_statement

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_if(self)

    def accept_type(self, visitor: TypeVisitor) -> Type:
        return visitor.visit_if(self)

    def accept_ir(self, visitor: IRVisitor) -> translate.Exp:
        return visitor.visit_if(self)

class While(Statement):
    def __init__(self, condition_exp: Exp, statement: Statement):
        self.condition_exp = condition_exp
        self.statement = statement

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_while(self)

    def accept_type(self, visitor: TypeVisitor) -> Type:
        return visitor.visit_while(self)

    def accept_ir(self, visitor: IRVisitor) -> translate.Exp:
        return visitor.visit_while(self)

class Assign(Statement):
    def __init__(self, left_side_id: Identifier, right_side_exp: Exp):
        self.left_side_id = left_side_id
        self.right_side_exp = right_side_exp

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_assign(self)

    def accept_type(self, visitor: TypeVisitor) -> Type:
        return visitor.visit_assign(self)

    def accept_ir(self, visitor: IRVisitor) -> translate.Exp:
        return visitor.visit_assign(self)


class Block(Statement):
    def __init__(self, statement_list: StatementList):
        self.statement_list = statement_list

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_block(self)

    def accept_type(self, visitor: TypeVisitor) -> Type:
        return visitor.visit_block(self)

    def accept_ir(self, visitor: IRVisitor) -> translate.Exp:
        return visitor.visit_block(self)

class ArrayAssign(Statement):
    def __init__(self, array_name_id: Identifier, array_exp: Exp, right_side_exp: Exp):
        self.array_name_id = array_name_id
        self.array_exp = array_exp
        self.right_side_exp = right_side_exp

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_array_assign(self)

    def accept_type(self, visitor: TypeVisitor) -> Type:
        return visitor.visit_array_assign(self)

    def accept_ir(self, visitor: IRVisitor) -> translate.Exp:
        return visitor.visit_array_assign(self)

class Identifier(Component):
    def __init__(self, name: str):
        self.name = name

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_identifier(self)

    def accept_type(self, visitor: TypeVisitor) -> Type:
        return visitor.visit_identifier(self)

    def accept_ir(self, visitor: IRVisitor) -> translate.Exp:
        return visitor.visit_identifier(self)

class Type(Component):

    @abstractmethod
    def accept(self, visitor: Visitor) -> None:
        pass
    
    @abstractmethod
    def accept_type(self, visitor: TypeVisitor) -> Type:
        pass

    @abstractmethod
    def accept_ir(self, visitor: IRVisitor) -> translate.Exp:
        pass

class BooleanType(Type):
    
    def accept(self, visitor: Visitor) -> None:
        visitor.visit_boolean_type(self)

    def accept_type(self, visitor: TypeVisitor) -> Type:
        return visitor.visit_boolean_type(self)

    def accept_ir(self, visitor: IRVisitor) -> translate.Exp:
        return visitor.visit_boolean_type(self)

class IntegerType(Type):
    
    def accept(self, visitor: Visitor) -> None:
        visitor.visit_integer_type(self)

    def accept_type(self, visitor: TypeVisitor) -> Type:
        return visitor.visit_integer_type(self)

    def accept_ir(self, visitor: IRVisitor) -> translate.Exp:
        return visitor.visit_integer_type(self)

class IntArrayType(Type):

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_int_array_type(self)
    
    def accept_type(self, visitor: TypeVisitor) -> Type:
        return visitor.visit_int_array_type(self)

    def accept_ir(self, visitor: IRVisitor) -> translate.Exp:
        return visitor.visit_int_array_type(self)

class IdentifierType(Type):
    def __init__(self, name: str):
        self.name = name

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_identifier_type(self)

    def accept_type(self, visitor: TypeVisitor) -> Type:
        return visitor.visit_identifier_type(self)

    def accept_ir(self, visitor: IRVisitor) -> translate.Exp:
        return visitor.visit_identifier_type(self)

class Exp(Component):

    @abstractmethod
    def accept(self, visitor: Visitor) -> None:
        pass
    
    @abstractmethod
    def accept_type(self, visitor: TypeVisitor) -> Type:
        pass

    @abstractmethod
    def accept_ir(self, visitor: IRVisitor) -> translate.Exp:
        pass

class ExpList():
    def __init__(self):
        self.exp_list = []
    
    def add_element(self, element: Exp) -> None: 
      self.exp_list.append(element)

    def element_at(self, index: int) -> Exp: 
      return self.exp_list[index]

    def get_elements(self): 
      return self.exp_list

    def size(self) -> int: 
      return len(self.exp_list)

class This(Exp):

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_this(self)

    def accept_type(self, visitor: TypeVisitor) -> Type:
        return visitor.visit_this(self)

    def accept_ir(self, visitor: IRVisitor) -> translate.Exp:
        return visitor.visit_this(self)

class IdentifierExp(Exp):
    def __init__(self, name: str):
        self.name = name

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_identifier_exp(self)

    def accept_type(self, visitor: TypeVisitor) -> Type:
        return visitor.visit_identifier_exp(self)

    def accept_ir(self, visitor: IRVisitor) -> translate.Exp:
        return visitor.visit_identifier_exp(self)

class FalseExp(Exp):
    def accept(self, visitor: Visitor) -> None:
        visitor.visit_false_exp(self)

    def accept_type(self, visitor: TypeVisitor) -> Type:
        return visitor.visit_false_exp(self)

    def accept_ir(self, visitor: IRVisitor) -> translate.Exp:
        return visitor.visit_false_exp(self)

class TrueExp(Exp):
    def accept(self, visitor: Visitor) -> None:
        visitor.visit_true_exp(self)

    def accept_type(self, visitor: TypeVisitor) -> Type:
        return visitor.visit_true_exp(self)

    def accept_ir(self, visitor: IRVisitor) -> translate.Exp:
        return visitor.visit_true_exp(self)

class IntegerLiteral(Exp):
    def __init__(self, value: int):
        self.value = value
    
    def accept(self, visitor: Visitor) -> None:
        visitor.visit_integer_literal(self)

    def accept_type(self, visitor: TypeVisitor) -> Type:
        return visitor.visit_integer_literal(self)

    def accept_ir(self, visitor: IRVisitor) -> translate.Exp:
        return visitor.visit_integer_literal(self)

class Minus(Exp):
    def __init__(self, left_side_exp: Exp, right_side_exp: Exp):
        self.left_side_exp = left_side_exp
        self.right_side_exp = right_side_exp
    
    def accept(self, visitor: Visitor) -> None:
        visitor.visit_minus(self)

    def accept_type(self, visitor: TypeVisitor) -> Type:
        return visitor.visit_minus(self)

    def accept_ir(self, visitor: IRVisitor) -> translate.Exp:
        return visitor.visit_minus(self)

class Plus(Exp):
    def __init__(self, left_side_exp: Exp, right_side_exp: Exp):
        self.left_side_exp = left_side_exp
        self.right_side_exp = right_side_exp
    
    def accept(self, visitor: Visitor) -> None:
        visitor.visit_plus(self)

    def accept_type(self, visitor: TypeVisitor) -> Type:
        return visitor.visit_plus(self)

    def accept_ir(self, visitor: IRVisitor) -> translate.Exp:
        return visitor.visit_plus(self)


class Times(Exp):
    def __init__(self, left_side_exp: Exp, right_side_exp: Exp):
        self.left_side_exp = left_side_exp
        self.right_side_exp = right_side_exp
    
    def accept(self, visitor: Visitor) -> None:
        visitor.visit_times(self)

    def accept_type(self, visitor: TypeVisitor) -> Type:
        return visitor.visit_times(self)

    def accept_ir(self, visitor: IRVisitor) -> translate.Exp:
        return visitor.visit_times(self)

class LessThan(Exp):
    def __init__(self, left_side_exp: Exp, right_side_exp: Exp):
        self.left_side_exp = left_side_exp
        self.right_side_exp = right_side_exp
    
    def accept(self, visitor: Visitor) -> None:
        visitor.visit_less_than(self)

    def accept_type(self, visitor: TypeVisitor) -> Type:
        return visitor.visit_less_than(self)
    
    def accept_ir(self, visitor: IRVisitor) -> translate.Exp:
        return visitor.visit_less_than(self)

class And(Exp):
    def __init__(self, left_side_exp: Exp, right_side_exp: Exp):
        self.left_side_exp = left_side_exp
        self.right_side_exp = right_side_exp
    
    def accept(self, visitor: Visitor) -> None:
        visitor.visit_and(self)

    def accept_type(self, visitor: TypeVisitor) -> Type:
        return visitor.visit_and(self)

    def accept_ir(self, visitor: IRVisitor) -> translate.Exp:
        return visitor.visit_and(self)

class ArrayLookup(Exp):
    def __init__(self, out_side_exp: Exp, in_side_exp: Exp):
        self.out_side_exp = out_side_exp
        self.in_side_exp = in_side_exp
    
    def accept(self, visitor: Visitor) -> None:
        visitor.visit_array_lookup(self)

    def accept_type(self, visitor: TypeVisitor) -> Type:
        return visitor.visit_array_lookup(self)

    def accept_ir(self, visitor: IRVisitor) -> translate.Exp:
        return visitor.visit_array_lookup(self)

class Call(Exp):
    def __init__(self, callee_exp: Exp, callee_name_id: Identifier, arg_list: ExpList):
        self.callee_exp = callee_exp
        self.callee_name_id = callee_name_id
        self.arg_list = arg_list
    
    def accept(self, visitor: Visitor) -> None:
        visitor.visit_call(self)

    def accept_type(self, visitor: TypeVisitor) -> Type:
        return visitor.visit_call(self)

    def accept_ir(self, visitor: IRVisitor) -> translate.Exp:
        return visitor.visit_call(self)


class ArrayLength(Exp):
    def __init__(self, length_exp: Exp):
        self.length_exp = length_exp
    
    def accept(self, visitor: Visitor) -> None:
        visitor.visit_array_length(self)

    def accept_type(self, visitor: TypeVisitor) -> Type:
        return visitor.visit_array_length(self)

    def accept_ir(self, visitor: IRVisitor) -> translate.Exp:
        return visitor.visit_array_length(self)

class Not(Exp):
    def __init__(self, negated_exp: Exp):
        self.negated_exp = negated_exp
    
    def accept(self, visitor: Visitor) -> None:
        visitor.visit_not(self)

    def accept_type(self, visitor: TypeVisitor) -> Type:
        return visitor.visit_not(self)

    def accept_ir(self, visitor: IRVisitor) -> translate.Exp:
        return visitor.visit_not(self)

class NewArray(Exp):
    def __init__(self, new_exp: Exp):
        self.new_exp = new_exp
    
    def accept(self, visitor: Visitor) -> None:
        visitor.visit_new_array(self)

    def accept_type(self, visitor: TypeVisitor) -> Type:
        return visitor.visit_new_array(self)

    def accept_ir(self, visitor: IRVisitor) -> translate.Exp:
        return visitor.visit_new_array(self)

class NewObject(Exp):
    def __init__(self, object_name_id: Identifier):
        self.object_name_id = object_name_id
    
    def accept(self, visitor: Visitor) -> None:
        visitor.visit_new_object(self)

    def accept_type(self, visitor: TypeVisitor) -> Type:
        return visitor.visit_new_object(self)

    def accept_ir(self, visitor: IRVisitor) -> translate.Exp:
        return visitor.visit_new_object(self)