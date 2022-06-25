from __future__ import annotations
from abc import ABC, abstractmethod

from pymjc.front import ast
from pymjc.front import temp
from pymjc.front import translate


########################################
# AST Simple Visitor
########################################

class Visitor(ABC):

    @abstractmethod
    def visit_program(self, element: ast.Program) -> None:
        pass

    @abstractmethod
    def visit_main_class(self, element: ast.MainClass) -> None:
        pass

    @abstractmethod
    def visit_class_decl_extends(self, element: ast.ClassDeclExtends) -> None:
        pass

    @abstractmethod
    def visit_class_decl_simple(self, element: ast.ClassDeclSimple) -> None:
        pass

    @abstractmethod
    def visit_var_decl(self, element: ast.VarDecl) -> None:
        pass
  
    @abstractmethod
    def visit_method_decl(self, element: ast.MethodDecl) -> None:
        pass

    @abstractmethod
    def visit_formal(self, element: ast.Formal) -> None:
        pass

    @abstractmethod
    def visit_int_array_type(self, element: ast.IntArrayType) -> None:
        pass

    @abstractmethod
    def visit_boolean_type(self, element: ast.BooleanType) -> None:
        pass

    @abstractmethod
    def visit_integer_type(self, element: ast.IntegerType) -> None:
        pass

    @abstractmethod
    def visit_identifier_type(self, element: ast.IdentifierType) -> None:
        pass

    @abstractmethod
    def visit_block(self, element: ast.Block) -> None:
        pass

    @abstractmethod
    def visit_if(self, element: ast.If) -> None:
        pass
  
    @abstractmethod
    def visit_while(self, element: ast.While) -> None:
        pass

    @abstractmethod
    def visit_print(self, element: ast.Print) -> None:
        pass

    @abstractmethod
    def visit_assign(self, element: ast.Assign) -> None:
        pass

    @abstractmethod
    def visit_array_assign(self, element: ast.ArrayAssign) -> None:
        pass

    @abstractmethod
    def visit_and(self, element: ast.And) -> None:
        pass

    @abstractmethod
    def visit_less_than(self, element: ast.LessThan) -> None:
        pass

    @abstractmethod
    def visit_plus(self, element: ast.Plus) -> None:
        pass

    @abstractmethod
    def visit_minus(self, element: ast.Minus) -> None:
        pass

    @abstractmethod
    def visit_times(self, element: ast.Times) -> None:
        pass

    @abstractmethod
    def visit_array_lookup(self, element: ast.ArrayLookup) -> None:
        pass

    @abstractmethod
    def visit_array_length(self, element: ast.ArrayLength) -> None:
        pass

    @abstractmethod
    def visit_call(self, element: ast.Call) -> None:
        pass

    @abstractmethod
    def visit_integer_literal(self, element: ast.IntegerLiteral) -> None:
        pass

    @abstractmethod
    def visit_true_exp(self, element: ast.TrueExp) -> None:
        pass

    @abstractmethod
    def visit_false_exp(self, element: ast.FalseExp) -> None:
        pass

    @abstractmethod
    def visit_identifier_exp(self, element: ast.IdentifierExp) -> None:
        pass

    @abstractmethod
    def visit_this(self, element: ast.This) -> None:
        pass

    @abstractmethod
    def visit_new_array(self, element: ast.NewArray) -> None:
        pass

    @abstractmethod
    def visit_new_object(self, element: ast.NewObject) -> None:
        pass


    @abstractmethod
    def visit_not(self, element: ast.Not) -> None:
        pass

    @abstractmethod
    def visit_identifier(self, element: ast.Identifier) -> None:
        pass



########################################
# AST Type Visitor
########################################
class TypeVisitor(ABC):

    @abstractmethod
    def visit_program(self, element: ast.Program) -> ast.Type:
        pass

    @abstractmethod
    def visit_main_class(self, element: ast.MainClass) -> ast.Type:
        pass

    @abstractmethod
    def visit_class_decl_extends(self, element: ast.ClassDeclExtends) -> ast.Type:
        pass

    @abstractmethod
    def visit_class_decl_simple(self, element: ast.ClassDeclSimple) -> ast.Type:
        pass

    @abstractmethod
    def visit_var_decl(self, element: ast.VarDecl) -> ast.Type:
        pass
  
    @abstractmethod
    def visit_method_decl(self, element: ast.MethodDecl) -> ast.Type:
        pass

    @abstractmethod
    def visit_formal(self, element: ast.Formal) -> ast.Type:
        pass

    @abstractmethod
    def visit_int_array_type(self, element: ast.IntArrayType) -> ast.Type:
        pass

    @abstractmethod
    def visit_boolean_type(self, element: ast.BooleanType) -> ast.Type:
        pass

    @abstractmethod
    def visit_integer_type(self, element: ast.IntegerType) -> ast.Type:
        pass

    @abstractmethod
    def visit_identifier_type(self, element: ast.IdentifierType) -> ast.Type:
        pass

    @abstractmethod
    def visit_block(self, element: ast.Block) -> ast.Type:
        pass

    @abstractmethod
    def visit_if(self, element: ast.If) -> ast.Type:
        pass
  
    @abstractmethod
    def visit_while(self, element: ast.While) -> ast.Type:
        pass

    @abstractmethod
    def visit_print(self, element: ast.Print) -> ast.Type:
        pass

    @abstractmethod
    def visit_assign(self, element: ast.Assign) -> ast.Type:
        pass

    @abstractmethod
    def visit_array_assign(self, element: ast.ArrayAssign) -> ast.Type:
        pass

    @abstractmethod
    def visit_and(self, element: ast.And) -> ast.Type:
        pass

    @abstractmethod
    def visit_less_than(self, element: ast.LessThan) -> ast.Type:
        pass

    @abstractmethod
    def visit_plus(self, element: ast.Plus) -> ast.Type:
        pass

    @abstractmethod
    def visit_minus(self, element: ast.Minus) -> ast.Type:
        pass

    @abstractmethod
    def visit_times(self, element: ast.Times) -> ast.Type:
        pass

    @abstractmethod
    def visit_array_lookup(self, element: ast.ArrayLookup) -> ast.Type:
        pass

    @abstractmethod
    def visit_array_length(self, element: ast.ArrayLength) -> ast.Type:
        pass

    @abstractmethod
    def visit_call(self, element: ast.Call) -> ast.Type:
        pass

    @abstractmethod
    def visit_integer_literal(self, element: ast.IntegerLiteral) -> ast.Type:
        pass

    @abstractmethod
    def visit_true_exp(self, element: ast.TrueExp) -> ast.Type:
        pass

    @abstractmethod
    def visit_false_exp(self, element: ast.FalseExp) -> ast.Type:
        pass

    @abstractmethod
    def visit_identifier_exp(self, element: ast.IdentifierExp) -> ast.Type:
        pass

    @abstractmethod
    def visit_this(self, element: ast.This) -> ast.Type:
        pass

    @abstractmethod
    def visit_new_array(self, element: ast.NewArray) -> ast.Type:
        pass

    @abstractmethod
    def visit_new_object(self, element: ast.NewObject) -> ast.Type:
        pass


    @abstractmethod
    def visit_not(self, element: ast.Not) -> ast.Type:
        pass

    @abstractmethod
    def visit_identifier(self, element: ast.Identifier) -> ast.Type:
        pass



########################################
# Intermediate Representation Visitor
########################################
class IRVisitor(ABC):

    @abstractmethod
    def visit_program(self, element: ast.Program) -> translate.Exp:
        pass

    @abstractmethod
    def visit_main_class(self, element: ast.MainClass) -> translate.Exp:
        pass

    @abstractmethod
    def visit_class_decl_extends(self, element: ast.ClassDeclExtends) -> translate.Exp:
        pass

    @abstractmethod
    def visit_class_decl_simple(self, element: ast.ClassDeclSimple) -> translate.Exp:
        pass

    @abstractmethod
    def visit_var_decl(self, element: ast.VarDecl) -> translate.Exp:
        pass
  
    @abstractmethod
    def visit_method_decl(self, element: ast.MethodDecl) -> translate.Exp:
        pass

    @abstractmethod
    def visit_formal(self, element: ast.Formal) -> translate.Exp:
        pass

    @abstractmethod
    def visit_int_array_type(self, element: ast.IntArrayType) -> translate.Exp:
        pass

    @abstractmethod
    def visit_boolean_type(self, element: ast.BooleanType) -> translate.Exp:
        pass

    @abstractmethod
    def visit_integer_type(self, element: ast.IntegerType) -> translate.Exp:
        pass

    @abstractmethod
    def visit_identifier_type(self, element: ast.IdentifierType) -> translate.Exp:
        pass

    @abstractmethod
    def visit_block(self, element: ast.Block) -> translate.Exp:
        pass

    @abstractmethod
    def visit_if(self, element: ast.If) -> translate.Exp:
        pass
  
    @abstractmethod
    def visit_while(self, element: ast.While) -> translate.Exp:
        pass

    @abstractmethod
    def visit_print(self, element: ast.Print) -> translate.Exp:
        pass

    @abstractmethod
    def visit_assign(self, element: ast.Assign) -> translate.Exp:
        pass

    @abstractmethod
    def visit_array_assign(self, element: ast.ArrayAssign) -> translate.Exp:
        pass

    @abstractmethod
    def visit_and(self, element: ast.And) -> translate.Exp:
        pass

    @abstractmethod
    def visit_less_than(self, element: ast.LessThan) -> translate.Exp:
        pass

    @abstractmethod
    def visit_plus(self, element: ast.Plus) -> translate.Exp:
        pass

    @abstractmethod
    def visit_minus(self, element: ast.Minus) -> translate.Exp:
        pass

    @abstractmethod
    def visit_times(self, element: ast.Times) -> translate.Exp:
        pass

    @abstractmethod
    def visit_array_lookup(self, element: ast.ArrayLookup) -> translate.Exp:
        pass

    @abstractmethod
    def visit_array_length(self, element: ast.ArrayLength) -> translate.Exp:
        pass

    @abstractmethod
    def visit_call(self, element: ast.Call) -> translate.Exp:
        pass

    @abstractmethod
    def visit_integer_literal(self, element: ast.IntegerLiteral) -> translate.Exp:
        pass

    @abstractmethod
    def visit_true_exp(self, element: ast.TrueExp) -> translate.Exp:
        pass

    @abstractmethod
    def visit_false_exp(self, element: ast.FalseExp) -> translate.Exp:
        pass

    @abstractmethod
    def visit_identifier_exp(self, element: ast.IdentifierExp) -> translate.Exp:
        pass

    @abstractmethod
    def visit_this(self, element: ast.This) -> translate.Exp:
        pass

    @abstractmethod
    def visit_new_array(self, element: ast.NewArray) -> translate.Exp:
        pass

    @abstractmethod
    def visit_new_object(self, element: ast.NewObject) -> translate.Exp:
        pass


    @abstractmethod
    def visit_not(self, element: ast.Not) -> translate.Exp:
        pass

    @abstractmethod
    def visit_identifier(self, element: ast.Identifier) -> translate.Exp:
        pass