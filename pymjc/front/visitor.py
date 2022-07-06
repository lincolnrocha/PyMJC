from __future__ import annotations
from abc import ABC, abstractmethod
import enum
from typing import List

from pymjc.front.ast import *
from pymjc.front.frame import Access, Frame
from pymjc.front import translate
from pymjc.front import tree
from pymjc.front import temp
from pymjc.front.visitorkinds import *
from pymjc.front.symbol import *
from pymjc.log import MJLogger
from pymjc.util import Converter

class SemanticErrorType(enum.Enum):
    ALREADY_DECLARED_CLASS = 1
    ALREADY_DECLARED_METHOD = 2
    ALREADY_DECLARED_FIELD = 3
    ALREADY_DECLARED_VAR = 4
    AND_TYPE_MISMATCH = 5
    ARG_TYPE_MISMATCH = 6
    ARRAY_ASSIGN_TYPE_MISMATCH = 7
    ARRAY_LENGTH_TYPE_MISMATCH = 8
    ARRAY_TYPE_MISMATCH = 9
    ASSIGN_TYPE_MISMATCH = 10
    DUPLICATED_ARG = 11
    IF_TYPE_MISMATCH = 12
    INDEX_TYPE_MISMATCH = 13
    INVALID_OBJECT_IDENTIFIER = 14
    LESS_THAN_TYPE_MISMATCH = 15
    MINUS_TYPE_MISMATCH = 16
    NEW_ARRAY_TYPE_MISMATCH = 17
    NEW_OBJECT_UNDECLARED_CLASS = 18
    NOT_TYPE_MISMATCH = 19
    PLUS_TYPE_MISMATCH = 20
    RETURN_TYPE_MISMATCH = 21
    TIMES_TYPE_MISMATCH = 22
    UNDECLARED_CLASS = 23
    UNDECLARED_IDENTIFIER = 24
    UNDECLARED_METHOD = 25
    UNDECLARED_SUPER_CLASS = 26 
    WHILE_TYPE_MISMATCH = 27
    WRONG_ARG_NUMBER = 28


########################################
# AST Simple Visitors
########################################

class PrettyPrintVisitor(Visitor):

    def __init__(self) -> None:
        super().__init__()
        self.iden = 1

    def inc_iden(self) -> None:
        self.iden = self.iden + 1

    def dec_iden(self) -> None:
        self.iden = self.iden - 1

    def get_iden(self) -> str:
        return  " " * self.iden

    def visit_program(self, element: Program) -> None:
        element.main_class.accept(self)
        for index in range(element.class_decl_list.size()):
            print()
            element.class_decl_list.element_at(index).accept(self)

    def visit_main_class(self, element: MainClass) -> None:
        print("class", end=' ')
        element.class_name_id.accept(self)
        print(" {")
        print(self.get_iden(),"public static void main (String [] ", end=' ')
        element.arg_name_id.accept(self)
        print(") {")
        print()
        self.inc_iden()
        element.statement.accept(self)
        self.dec_iden()
        print()
        print(self.get_iden(), "}")
        print("}")

    def visit_class_decl_extends(self, element: ClassDeclExtends) -> None:
        print("class", end=' ')
        element.class_name_id.accept(self)
        print(" extends", end=' ')
        element.super_class_name_id.accept(self)
        print(" {")

        self.inc_iden()
        for index in range(element.var_decl_list.size()):
            #print(self.get_iden(), end='')
            element.var_decl_list.element_at(index).accept(self)
            if (index + 1 < element.var_decl_list.size() ): 
                print()
    
        for index in range(element.method_decl_list.size()):
            print()
            element.method_decl_list.element_at(index).accept(self)
        self.dec_iden()
        print()
        print("}")


    def visit_class_decl_simple(self, element: ClassDeclSimple) -> None:
        print("class", end=' ')
        element.class_name_id.accept(self)
        print(" {")

        self.inc_iden()
        for index in range(element.var_decl_list.size()):
            element.var_decl_list.element_at(index).accept(self)
            if (index + 1 < element.var_decl_list.size()): 
                print()
    
        for index in range(element.method_decl_list.size()):
            print()
            element.method_decl_list.element_at(index).accept(self)
            
        self.dec_iden()
        print()
        print("}")


    def visit_var_decl(self, element: VarDecl) -> None:
        print(self.get_iden(), end='')
        element.type.accept(self)
        print(" ", end='')
        element.name_id.accept(self)
        print(";")
     

    def visit_method_decl(self, element: MethodDecl) -> None:
        print(self.get_iden(), "public", end=' ')
        element.type.accept(self)
        print(" ", end='')
        element.name_id.accept(self)
        print(" (", end='')

        for index in range(element.formal_param_list.size()):
            element.formal_param_list.element_at(index).accept(self)
            if(index + 1 < element.formal_param_list.size()):
                print(", ", end='')
        
        print(") {")

        self.inc_iden()
        for index in range(element.var_decl_list.size()):
            #print(self.get_iden(), end='')
            element.var_decl_list.element_at(index).accept(self)
        
        for index in range(element.statement_list.size()):
            #print(self.get_iden(), end='')
            element.statement_list.element_at(index).accept(self)
            if(index + 1 < element.statement_list.size()):
                print()

        print(self.get_iden(), "return ", end='')
        element.return_exp.accept(self)
        print(";")
        self.dec_iden()
        print(self.get_iden(), "}")


    def visit_formal(self, element: Formal) -> None:
        element.type.accept(self)
        print(" ", end='')
        element.name_id.accept(self)


    def visit_int_array_type(self, element: IntArrayType) -> None:
        print("int []", end='')

    
    def visit_boolean_type(self, element: BooleanType) -> None:
        print("boolean", end='')

    
    def visit_integer_type(self, element: IntegerType) -> None:
        print("int", end='')

    
    def visit_identifier_type(self, element: IdentifierType) -> None:
        print(element.name, end='')

    
    def visit_block(self, element: Block) -> None:
        print(self.get_iden(),"{ ")
        self.inc_iden()
        for index in range(element.statement_list.size()):
            print(self.get_iden(), end='')
            element.statement_list.element_at(index).accept(self)
            print()

        self.dec_iden()
        print(self.get_iden(), "} ")

    def visit_if(self, element: If) -> None:
        print(self.get_iden(), "if (", end='')
        element.condition_exp.accept(self)
        print(")")
        self.inc_iden()
        element.if_statement.accept(self)
        self.dec_iden()
        print()
        print(self.get_iden(), "else")
        self.inc_iden()
        element.else_statement.accept(self)
        self.dec_iden()
  

    def visit_while(self, element: While) -> None:
        print(self.get_iden(),"while (", end='')
        element.condition_exp.accept(self)
        print(")")
        self.inc_iden()
        element.statement.accept(self)
        self.dec_iden()

    
    def visit_print(self, element: Print) -> None:
        print(self.get_iden(), "System.out.println(", end='')
        element.print_exp.accept(self)
        print(");", end='')


    def visit_assign(self, element: Assign) -> None:
        print(self.get_iden(), end='')
        element.left_side_id.accept(self)
        print(" = ", end='')
        element.right_side_exp.accept(self)
        print(";", end='')

    
    def visit_array_assign(self, element: ArrayAssign) -> None:
        print(self.get_iden(), end='')
        element.array_name_id.accept(self)
        print("[", end='')
        element.array_exp.accept(self)
        print("] = ", end='')
        element.right_side_exp.accept(self)
        print(";", end='')

    
    def visit_and(self, element: And) -> None:
        print("(", end='')
        element.left_side_exp.accept(self)
        print(" && ", end='')
        element.right_side_exp.accept(self)
        print(")", end='')

    def visit_less_than(self, element: LessThan) -> None:
        print("(", end='')
        element.left_side_exp.accept(self)
        print(" < ", end='')
        element.right_side_exp.accept(self)
        print(")", end='')


    def visit_plus(self, element: Plus) -> None:
        print("(", end='')
        element.left_side_exp.accept(self)
        print(" + ", end='')
        element.right_side_exp.accept(self)
        print(")", end='')


    def visit_minus(self, element: Minus) -> None:
        print("(", end='')
        element.left_side_exp.accept(self)
        print(" - ", end='')
        element.right_side_exp.accept(self)
        print(")", end='')

    
    def visit_times(self, element: Times) -> None:
        print("(", end='')
        element.left_side_exp.accept(self)
        print(" * ", end='')
        element.right_side_exp.accept(self)
        print(")", end='')


    def visit_array_lookup(self, element: ArrayLookup) -> None:
        element.out_side_exp.accept(self)
        print("[", end='')
        element.in_side_exp.accept(self)
        print("]", end='')

    def visit_array_length(self, element: ArrayLength) -> None:
        element.length_exp.accept(self)
        print(".length", end='')


    def visit_call(self, element: Call) -> None:
        element.callee_exp.accept(self)
        print(".", end='')
        element.callee_name_id.accept(self)
        print("(", end='')
        for index in range(element.arg_list.size()):
            element.arg_list.element_at(index).accept(self)
            if( index + 1 < element.arg_list.size()):
                print(", ", end='')
        print(")", end='')


    def visit_integer_literal(self, element: IntegerLiteral) -> None:
        print(element.value, end='')


    def visit_true_exp(self, element: TrueExp) -> None:
        print("true", end='')


    def visit_false_exp(self, element: FalseExp) -> None:
        print("false", end='')


    def visit_identifier_exp(self, element: IdentifierExp) -> None:
        print(element.name, end='')

    def visit_this(self, element: This) -> None:
        print("this", end='')

    def visit_new_array(self, element: NewArray) -> None:
        print("new int[", end='') 
        element.new_exp.accept(self)
        print("]", end='')


    def visit_new_object(self, element: NewObject) -> None:
        print("new ", end='')
        element.object_name_id.accept(self)
        print("()", end='')


    def visit_not(self, element: Not) -> None:
        print("!", end='')
        element.negated_exp.accept(self)


    def visit_identifier(self, element: Identifier) -> None:
        print(element.name, end='')
    


class DepthFirstVisitor(Visitor):

    def visit_program(self, element: Program) -> None:
        element.main_class.accept(self)
        for index in range(element.class_decl_list.size()):
            element.class_decl_list.element_at(index).accept(self)

    def visit_main_class(self, element: MainClass) -> None:
        element.class_name_id.accept(self)
        element.arg_name_id.accept(self)
        element.statement.accept(self)

    def visit_class_decl_extends(self, element: ClassDeclExtends) -> None:
        element.class_name_id.accept(self)
        element.super_class_name_id.accept(self)
        for index in range(element.var_decl_list.size()):
            element.var_decl_list.element_at(index).accept(self)
    
        for index in range(element.method_decl_list.size()):
            element.method_decl_list.element_at(index).accept(self)


    def visit_class_decl_simple(self, element: ClassDeclSimple) -> None:
        element.class_name_id.accept(self)

        for index in range(element.var_decl_list.size()):
            element.var_decl_list.element_at(index).accept(self)
    
        for index in range(element.method_decl_list.size()):
            element.method_decl_list.element_at(index).accept(self)


    def visit_var_decl(self, element: VarDecl) -> None:
        element.type.accept(self)
        element.name_id.accept(self)
     

    def visit_method_decl(self, element: MethodDecl) -> None:
        element.type.accept(self)
        element.name_id.accept(self)

        for index in range(element.formal_param_list.size()):
            element.formal_param_list.element_at(index).accept(self)

        for index in range(element.var_decl_list.size()):
            element.var_decl_list.element_at(index).accept(self)

        for index in range(element.statement_list.size()):
            element.statement_list.element_at(index).accept(self)

        element.return_exp.accept(self)


    def visit_formal(self, element: Formal) -> None:
        element.type.accept(self)
        element.name_id.accept(self)


    def visit_int_array_type(self, element: IntArrayType) -> None:
        return None
    
    def visit_boolean_type(self, element: BooleanType) -> None:
        return None
    
    def visit_integer_type(self, element: IntegerType) -> None:
        return None

    def visit_identifier_type(self, element: IdentifierType) -> None:
        return None

    
    def visit_block(self, element: Block) -> None:
        for index in range(element.statement_list.size()):
            element.statement_list.element_at(index).accept(self)

    def visit_if(self, element: If) -> None:
        element.condition_exp.accept(self)
        element.if_statement.accept(self)
        element.else_statement.accept(self)
  

    def visit_while(self, element: While) -> None:
        element.condition_exp.accept(self)
        element.statement.accept(self)

    
    def visit_print(self, element: Print) -> None:
        element.print_exp.accept(self)

    def visit_assign(self, element: Assign) -> None:
        element.left_side_id.accept(self)
        element.right_side_exp.accept(self)

    
    def visit_array_assign(self, element: ArrayAssign) -> None:
        element.array_name_id.accept(self)
        element.array_exp.accept(self)
        element.right_side_exp.accept(self)

    
    def visit_and(self, element: And) -> None:
        element.left_side_exp.accept(self)
        element.right_side_exp.accept(self)

    def visit_less_than(self, element: LessThan) -> None:
        element.left_side_exp.accept(self)
        element.right_side_exp.accept(self)


    def visit_plus(self, element: Plus) -> None:
        element.left_side_exp.accept(self)
        element.right_side_exp.accept(self)


    def visit_minus(self, element: Minus) -> None:
        element.left_side_exp.accept(self)
        element.right_side_exp.accept(self)

    
    def visit_times(self, element: Times) -> None:
        element.left_side_exp.accept(self)
        element.right_side_exp.accept(self)


    def visit_array_lookup(self, element: ArrayLookup) -> None:
        element.out_side_exp.accept(self)
        element.in_side_exp.accept(self)

    def visit_array_length(self, element: ArrayLength) -> None:
        element.length_exp.accept(self)



    def visit_call(self, element: Call) -> None:
        element.callee_exp.accept(self)
        element.callee_name_id.accept(self)
        for index in range(element.arg_list.size()):
            element.arg_list.element_at(index).accept(self)


    def visit_integer_literal(self, element: IntegerLiteral) -> None:
        return None


    def visit_true_exp(self, element: TrueExp) -> None:
        return None


    def visit_false_exp(self, element: FalseExp) -> None:
        return None


    def visit_identifier_exp(self, element: IdentifierExp) -> None:
        return None

    def visit_this(self, element: This) -> None:
        return None

    def visit_new_array(self, element: NewArray) -> None:
        element.new_exp.accept(self)


    def visit_new_object(self, element: NewObject) -> None:
        element.object_name_id.accept(self)


    def visit_not(self, element: Not) -> None:
        element.negated_exp.accept(self)


    def visit_identifier(self, element: Identifier) -> None:
        return None


#TODO
class FillSymbolTableVisitor(Visitor):
    def __init__(self) -> None:
        super().__init__()
        self.semantic_errors = {}
        self.symbol_table = SymbolTable()
        self.src_file_name = "UnknownSRCFile"

    def init_semantic_errors(self) -> None:
        for error_type in SemanticErrorType:
            self.semantic_errors[error_type.name] = 0

    def fill_semantic_errors(self, semantic_errors) -> None:
            self.semantic_errors = semantic_errors

    def add_semantic_error(self, error_type: SemanticErrorType) -> None:
            self.semantic_errors[error_type.name] += 1

    def get_symbol_table(self) -> SymbolTable:
        return self.symbol_table

    def visit_program(self, element: Program) -> None:
        self.symbol_table.add_scope(element.main_class.class_name_id.name, ClassEntry())

        for index in range(element.class_decl_list.size()):
            class_decl = element.class_decl_list.element_at(index)
            class_entry = None
            
            if isinstance(class_decl, ClassDeclExtends):
                class_entry = ClassEntry(class_decl.super_class_name_id.name)
            else:
                class_entry = ClassEntry()

            if not self.symbol_table.add_scope(class_decl.class_name_id.name, class_entry) :
                self.add_semantic_error(SemanticErrorType.ALREADY_DECLARED_CLASS)

        element.main_class.accept(self)
        for index in range(element.class_decl_list.size()):
            element.class_decl_list.element_at(index).accept(self)


    def visit_main_class(self, element: MainClass) -> None:
        self.symbol_table.set_curr_class(element.class_name_id.name)
        element.class_name_id.accept(self)
        #self.symbol_table.add_method("main", MethodEntry(IdentifierType("void")))
        self.symbol_table.add_method("main", MethodEntry(None))
        element.arg_name_id.accept(self)
        #self.symbol_table.add_param(element.arg_name_ideintifier.name, IdentifierType("String[]"))
        self.symbol_table.add_param(element.arg_name_id.name, None)
        element.statement.accept(self)
        return None

    def visit_class_decl_extends(self, element: ClassDeclExtends) -> None:
        self.symbol_table.set_curr_class(element.class_name_id.name)
        element.class_name_id.accept(self)

        if not self.symbol_table.contains_class(element.super_class_name_id.name):
            self.add_semantic_error(SemanticErrorType.UNDECLARED_SUPER_CLASS)
            MJLogger.semantic_log(self.src_file_name, SemanticErrorType.UNDECLARED_SUPER_CLASS.name, element.super_class_name_id.name)
            
        element.super_class_name_id.accept(self)
        
        for index in range(element.var_decl_list.size()):
            element.var_decl_list.element_at(index).accept(self)

        for index in range(element.method_decl_list.size()):
            element.method_decl_list.element_at(index).accept(self)

        self.symbol_table.add_extends_entry(element.class_name_id.name, element.super_class_name_id.name)

        return None

    def visit_class_decl_simple(self, element: ClassDeclSimple) -> None:
        self.symbol_table.set_curr_class(element.class_name_id.name)
        element.class_name_id.accept(self)

        for index in range(element.var_decl_list.size()):
            element.var_decl_list.element_at(index).accept(self)


        for index in range(element.method_decl_list.size()):
            element.method_decl_list.element_at(index).accept(self)


    def visit_var_decl(self, element: VarDecl) -> None:
        element.type.accept(self)
        element.name_id.accept(self)

        if(self.symbol_table.curr_method is not None):
            if not self.symbol_table.add_local(element.name_id.name, element.type):
                self.add_semantic_error(SemanticErrorType.ALREADY_DECLARED_VAR)
                MJLogger.semantic_log(self.src_file_name, SemanticErrorType.ALREADY_DECLARED_VAR.name, self.symbol_table.curr_method_name + "#" + element.name_id.name)
        
        elif not self.symbol_table.add_field(element.name_id.name, element.type):
                self.add_semantic_error(SemanticErrorType.ALREADY_DECLARED_FIELD)
                MJLogger.semantic_log(self.src_file_name, SemanticErrorType.ALREADY_DECLARED_FIELD.name, self.symbol_table.curr_class_name + "#" + element.name_id.name)
        
        return None

    def visit_method_decl(self, element: MethodDecl) -> None:
        element.type.accept(self)
        element.name_id.accept(self)

        if not self.symbol_table.add_method(element.name_id.name, MethodEntry(element.type)):
            self.add_semantic_error(SemanticErrorType.ALREADY_DECLARED_METHOD)
            MJLogger.semantic_log(self.src_file_name, SemanticErrorType.ALREADY_DECLARED_METHOD.name, self.symbol_table.curr_class_name + "#" + element.name_id.name)

        for index in range(element.formal_param_list.size()):
            element.formal_param_list.element_at(index).accept(self)

        for index in range(element.var_decl_list.size()):
            element.var_decl_list.element_at(index).accept(self)

        for index in range(element.statement_list.size()):
            element.statement_list.element_at(index).accept(self)

        element.return_exp.accept(self)

        return None


    def visit_formal(self, element: Formal) -> None:
        element.type.accept(self)
        element.type.accept(self)
        if not self.symbol_table.add_param(element.name_id.name, element.type):
            self.add_semantic_error(SemanticErrorType.DUPLICATED_ARG)
            MJLogger.semantic_log(self.src_file_name, SemanticErrorType.DUPLICATED_ARG.name, self.symbol_table.curr_class_name + "#" + self.symbol_table.curr_method_name + "#" + element.name_id.name)            


    def visit_int_array_type(self, element: IntArrayType) -> None:
        return None
    
    def visit_boolean_type(self, element: BooleanType) -> None:
        return None
    
    def visit_integer_type(self, element: IntegerType) -> None:
        return None

    def visit_identifier_type(self, element: IdentifierType) -> None:
        return None

    
    def visit_block(self, element: Block) -> None:
        for index in range(element.statement_list.size()):
            element.statement_list.element_at(index).accept(self)

    def visit_if(self, element: If) -> None:
        element.condition_exp.accept(self)
        element.if_statement.accept(self)
        element.else_statement.accept(self)
        return None
  

    def visit_while(self, element: While) -> None:
        element.condition_exp.accept(self)
        element.statement.accept(self)
        return None
    
    def visit_print(self, element: Print) -> None:
        element.print_exp.accept(self)
        return None

    def visit_assign(self, element: Assign) -> None:
        element.left_side_id.accept(self)
        element.right_side_exp.accept(self)
        return None

    
    def visit_array_assign(self, element: ArrayAssign) -> None:
        element.array_name_id.accept(self)
        element.array_exp.accept(self)
        element.right_side_exp.accept(self)
        return None
    
    def visit_and(self, element: And) -> None:
        element.left_side_exp.accept(self)
        element.right_side_exp.accept(self)
        return None

    def visit_less_than(self, element: LessThan) -> None:
        element.left_side_exp.accept(self)
        element.right_side_exp.accept(self)
        return None


    def visit_plus(self, element: Plus) -> None:
        element.left_side_exp.accept(self)
        element.right_side_exp.accept(self)
        return None


    def visit_minus(self, element: Minus) -> None:
        element.left_side_exp.accept(self)
        element.right_side_exp.accept(self)
        return None

    
    def visit_times(self, element: Times) -> None:
        element.left_side_exp.accept(self)
        element.right_side_exp.accept(self)
        return None


    def visit_array_lookup(self, element: ArrayLookup) -> None:
        element.out_side_exp.accept(self)
        element.in_side_exp.accept(self)
        return None

    def visit_array_length(self, element: ArrayLength) -> None:
        element.length_exp.accept(self)
        return None



    def visit_call(self, element: Call) -> None:
        element.callee_exp.accept(self)
        element.callee_name_id.accept(self)
        for index in range(element.arg_list.size()):
            element.arg_list.element_at(index).accept(self)
        
        return None


    def visit_integer_literal(self, element: IntegerLiteral) -> None:
        return None


    def visit_true_exp(self, element: TrueExp) -> None:
        return None


    def visit_false_exp(self, element: FalseExp) -> None:
        return None


    def visit_identifier_exp(self, element: IdentifierExp) -> None:
        return None

    def visit_this(self, element: This) -> None:
        return None

    def visit_new_array(self, element: NewArray) -> None:
        element.new_exp.accept(self)
        return None


    def visit_new_object(self, element: NewObject) -> None:
        element.object_name_id.accept(self)
        return None


    def visit_not(self, element: Not) -> None:
        element.negated_exp.accept(self)
        return None


    def visit_identifier(self, element: Identifier) -> None:
        return None




########################################
# AST Type Visitors
########################################

class TypeDepthFirstVisitor(TypeVisitor):

    def visit_program(self, element: Program) -> Type:
        element.main_class.accept_type(self)
        for index in range(element.class_decl_list.size()):
            element.class_decl_list.element_at(index).accept_type(self)
        return None

    def visit_main_class(self, element: MainClass) -> Type:
        element.class_name_id.accept_type(self)
        element.arg_name_id.accept_type(self)
        element.statement.accept_type(self)
        return None

    def visit_class_decl_extends(self, element: ClassDeclExtends) -> Type:
        element.class_name_id.accept_type(self)
        element.super_class_name_id.accept_type(self)
        
        for index in range(element.var_decl_list.size()):
            element.var_decl_list.element_at(index).accept_type(self)
    
        for index in range(element.method_decl_list.size()):
            element.method_decl_list.element_at(index).accept_type(self)

        return None    

    def visit_class_decl_simple(self, element: ClassDeclSimple) -> Type:
        element.class_name_id.accept_type(self)

        for index in range(element.var_decl_list.size()):
            element.var_decl_list.element_at(index).accept_type(self)
    
        for index in range(element.method_decl_list.size()):
            element.method_decl_list.element_at(index).accept_type(self)
        
        return None

    def visit_var_decl(self, element: VarDecl) -> Type:
        element.type.accept_type(self)
        element.name_id.accept_type(self)
        return None
     

    def visit_method_decl(self, element: MethodDecl) -> Type:
        element.type.accept_type(self)
        element.name_id.accept_type(self)

        for index in range(element.formal_param_list.size()):
            element.formal_param_list.element_at(index).accept_type(self)

        for index in range(element.var_decl_list.size()):
            element.var_decl_list.element_at(index).accept_type(self)

        for index in range(element.statement_list.size()):
            element.statement_list.element_at(index).accept_type(self)

        element.return_exp.accept_type(self)
        return None


    def visit_formal(self, element: Formal) -> Type:
        element.type.accept_type(self)
        element.name_id.accept_type(self)
        return None


    def visit_int_array_type(self, element: IntArrayType) -> Type:
        return None
    
    def visit_boolean_type(self, element: BooleanType) -> Type:
        return None
    
    def visit_integer_type(self, element: IntegerType) -> Type:
        return None

    
    def visit_identifier_type(self, element: IdentifierType) -> Type:
        return None

    
    def visit_block(self, element: Block) -> Type:
        for index in range(element.statement_list.size()):
            element.statement_list.element_at(index).accept_type(self)
        
        return None

    def visit_if(self, element: If) -> Type:
        element.condition_exp.accept_type(self)
        element.if_statement.accept_type(self)
        element.else_statement.accept_type(self)
        return None
  

    def visit_while(self, element: While) -> Type:
        element.condition_exp.accept_type(self)
        element.statement.accept_type(self)
        return None

    
    def visit_print(self, element: Print) -> Type:
        element.print_exp.accept_type(self)
        return None


    def visit_assign(self, element: Assign) -> Type:
        element.left_side_id.accept_type(self)
        element.right_side_exp.accept_type(self)
        return None

    
    def visit_array_assign(self, element: ArrayAssign) -> Type:
        element.array_name_id.accept_type(self)
        element.array_exp.accept_type(self)
        element.right_side_exp.accept_type(self)
        return None

    
    def visit_and(self, element: And) -> Type:
        element.left_side_exp.accept_type(self)
        element.right_side_exp.accept_type(self)
        return None

    def visit_less_than(self, element: LessThan) -> Type:
        element.left_side_exp.accept_type(self)
        element.right_side_exp.accept_type(self)
        return None


    def visit_plus(self, element: Plus) -> Type:
        element.left_side_exp.accept_type(self)
        element.right_side_exp.accept_type(self)
        return None


    def visit_minus(self, element: Minus) -> Type:
        element.left_side_exp.accept_type(self)
        element.right_side_exp.accept_type(self)
        return None

    
    def visit_times(self, element: Times) -> Type:
        element.left_side_exp.accept_type(self)
        element.right_side_exp.accept_type(self)
        return None


    def visit_array_lookup(self, element: ArrayLookup) -> Type:
        element.out_side_exp.accept_type(self)
        element.in_side_exp.accept_type(self)
        return None

    def visit_array_length(self, element: ArrayLength) -> Type:
        element.length_exp.accept_type(self)
        return None


    def visit_call(self, element: Call) -> Type:
        element.callee_exp.accept_type(self)
        element.callee_name_id.accept_type(self)
        for index in range(element.arg_list.size()):
            element.arg_list.element_at(index).accept_type(self)
        return None


    def visit_integer_literal(self, element: IntegerLiteral) -> Type:
        return None


    def visit_true_exp(self, element: TrueExp) -> Type:
        return None


    def visit_false_exp(self, element: FalseExp) -> Type:
        return None


    def visit_identifier_exp(self, element: IdentifierExp) -> Type:
        return None


    def visit_this(self, element: This) -> Type:
        return None


    def visit_new_array(self, element: NewArray) -> Type:
        element.new_exp.accept_type(self)
        return None


    def visit_new_object(self, element: NewObject) -> Type:
        element.object_name_id.accept_type(self)
        return None


    def visit_not(self, element: Not) -> Type:
        element.negated_exp.accept_type(self)
        return None


    def visit_identifier(self, element: Identifier) -> Type:
        return None


class TypeCheckingVisitor(TypeVisitor): 
    def __init__(self) -> None:
        super().__init__()
        self.semantic_errors = {}
        self.src_file_name = "UnknownSRCFile"

    def init_semantic_errors(self) -> None:
        for error_type in SemanticErrorType:
            self.semantic_errors[error_type.name] = 0

    def fill_semantic_errors(self, semantic_errors) -> None:
            self.semantic_errors = semantic_errors

    def add_semantic_error(self, error_type: SemanticErrorType) -> None:
            self.semantic_errors[error_type.name] += 1

    def set_symbol_table(self, symbol_table: SymbolTable):
        self.symbol_table = symbol_table

    def get_symbol_table(self) -> SymbolTable:
        return self.symbol_table

    def visit_program(self, element: Program) -> Type:
        element.main_class.accept_type(self)
        for index in range(element.class_decl_list.size()):
            element.class_decl_list.element_at(index).accept_type(self)
        return None

    def visit_main_class(self, element: MainClass) -> Type:
        self.symbol_table.set_curr_class(element.class_name_id.name)
        self.symbol_table.set_curr_method("main")
        element.class_name_id.accept_type(self)
        element.arg_name_id.accept_type(self)
        element.statement.accept_type(self)
        return None

    def visit_class_decl_extends(self, element: ClassDeclExtends) -> Type:
        self.symbol_table.set_curr_class(element.class_name_id.name)
        element.class_name_id.accept_type(self)
        element.super_class_name_id.accept_type(self)

        for index in range(element.var_decl_list.size()):
            element.var_decl_list.element_at(index).accept_type(self)
    
        for index in range(element.method_decl_list.size()):
            element.method_decl_list.element_at(index).accept_type(self)

        return None    

    def visit_class_decl_simple(self, element: ClassDeclSimple) -> Type:
        self.symbol_table.set_curr_class(element.class_name_id.name)
        element.class_name_id.accept_type(self)

        for index in range(element.var_decl_list.size()):
            element.var_decl_list.element_at(index).accept_type(self)
    
        for index in range(element.method_decl_list.size()):
            element.method_decl_list.element_at(index).accept_type(self)
        
        return None

    def visit_var_decl(self, element: VarDecl) -> Type:
        element.type.accept_type(self)
        element.name_id.accept_type(self)
        return None
     

    def visit_method_decl(self, element: MethodDecl) -> Type:
        self.symbol_table.set_curr_method(element.name_id.name)
        element.type.accept_type(self)
        element.name_id.accept_type(self)

        for index in range(element.formal_param_list.size()):
            element.formal_param_list.element_at(index).accept_type(self)

        for index in range(element.var_decl_list.size()):
            element.var_decl_list.element_at(index).accept_type(self)

        for index in range(element.statement_list.size()):
            element.statement_list.element_at(index).accept_type(self)

        method_return_type = self.symbol_table.curr_method.get_return_type()
        return_exp_type = element.return_exp.accept_type(self)
        
        if(type(method_return_type) != type(return_exp_type)):
            self.add_semantic_error(SemanticErrorType.RETURN_TYPE_MISMATCH)
            error_msg = self.symbol_table.curr_class_name + "#" + self.symbol_table.curr_method_name
            error_msg = " expected return type " + str(type(method_return_type)) + " not " + str(type(return_exp_type))
            MJLogger.semantic_log(self.src_file_name, SemanticErrorType.RETURN_TYPE_MISMATCH.name, error_msg)

        return None


    def visit_formal(self, element: Formal) -> Type:
        element.type.accept_type(self)
        element.name_id.accept_type(self)
        return None


    def visit_int_array_type(self, element: IntArrayType) -> Type:
        return element
    
    def visit_boolean_type(self, element: BooleanType) -> Type:
        return element
    
    def visit_integer_type(self, element: IntegerType) -> Type:
        return element

    
    def visit_identifier_type(self, element: IdentifierType) -> Type:
        if(not self.symbol_table.contains_class(element.name)):
            self.add_semantic_error(SemanticErrorType.UNDECLARED_CLASS)
            MJLogger.semantic_log(self.src_file_name, SemanticErrorType.UNDECLARED_CLASS.name, element.name)

        return element

    
    def visit_block(self, element: Block) -> Type:
        for index in range(element.statement_list.size()):
            element.statement_list.element_at(index).accept_type(self)
        
        return None

    def visit_if(self, element: If) -> Type:
        condition_exp_type = element.condition_exp.accept_type(self)
        if(not isinstance(condition_exp_type, BooleanType)):
            self.add_semantic_error(SemanticErrorType.IF_TYPE_MISMATCH)
            error_msg = self.symbol_table.curr_class_name + "#" + self.symbol_table.curr_method_name
            error_msg = error_msg + " if condition type must be BooleanType not " + str(type(condition_exp_type))
            MJLogger.semantic_log(self.src_file_name, SemanticErrorType.IF_TYPE_MISMATCH.name, error_msg)

        element.if_statement.accept_type(self)
        element.else_statement.accept_type(self)
        return None
  

    def visit_while(self, element: While) -> Type:
        condition_exp_type = element.condition_exp.accept_type(self)
        if(not isinstance(condition_exp_type, BooleanType)):
            self.add_semantic_error(SemanticErrorType.WHILE_TYPE_MISMATCH)
            error_msg = self.symbol_table.curr_class_name + "#" + self.symbol_table.curr_method_name
            error_msg = error_msg + " while condition type must be BooleanType not " + str(type(condition_exp_type))
            MJLogger.semantic_log(self.src_file_name, SemanticErrorType.WHILE_TYPE_MISMATCH.name, error_msg)

        element.statement.accept_type(self)
        return None

    
    def visit_print(self, element: Print) -> Type:
        element.print_exp.accept_type(self)
        return None


    def visit_assign(self, element: Assign) -> Type:
        curr_class = self.symbol_table.curr_class
        curr_method = self.symbol_table.curr_method
        check_field_decl = curr_class.contains_field(element.left_side_id.name)
        check_local_decl = curr_method.contains_local(element.left_side_id.name)
        check_param_decl = curr_method.contains_param(element.left_side_id.name)
            
        if(not (check_field_decl or check_local_decl or check_param_decl)):
            self.add_semantic_error(SemanticErrorType.UNDECLARED_IDENTIFIER)
            error_msg = self.symbol_table.curr_class_name + "#" + self.symbol_table.curr_method_name + " " + element.left_side_id.name + " is an undeclared identifier."
            MJLogger.semantic_log(self.src_file_name, SemanticErrorType.UNDECLARED_IDENTIFIER.name, error_msg)            

        left_side_type = element.left_side_id.accept_type(self)
        right_side_type = element.right_side_exp.accept_type(self)

        if((type(left_side_type) is None) or (type(right_side_type) is None) or (type(left_side_type) != type(right_side_type))):
            self.add_semantic_error(SemanticErrorType.ASSIGN_TYPE_MISMATCH)
            error_msg = self.symbol_table.curr_class_name + "#" + self.symbol_table.curr_method_name
            error_msg = error_msg + " left side type " + str(type(left_side_type))
            error_msg = error_msg + " and right side type " + str(type(right_side_type))
            MJLogger.semantic_log(self.src_file_name, SemanticErrorType.ASSIGN_TYPE_MISMATCH.name, error_msg)

        return None

    
    def visit_array_assign(self, element: ArrayAssign) -> Type:
        curr_class = self.symbol_table.curr_class
        curr_method = self.symbol_table.curr_method
        check_field_decl = curr_class.contains_field(element.array_name_id.name)
        check_local_decl = curr_method.contains_local(element.array_name_id.name)
        check_param_decl = curr_method.contains_param(element.array_name_id.name)
            
        if(not (check_field_decl or check_local_decl or check_param_decl)):
            self.add_semantic_error(SemanticErrorType.UNDECLARED_IDENTIFIER)
            error_msg = self.symbol_table.curr_class_name + "#" + self.symbol_table.curr_method_name + " " + element.array_name_id.name + " is an undeclared identifier."
            MJLogger.semantic_log(self.src_file_name, SemanticErrorType.UNDECLARED_IDENTIFIER.name, error_msg)

        array_type = element.array_name_id.accept_type(self)
        array_index_type = element.array_exp.accept_type(self)

        if(not isinstance(array_index_type, IntegerType)):
            self.add_semantic_error(SemanticErrorType.INDEX_TYPE_MISMATCH)
            error_msg = self.symbol_table.curr_class_name + "#" + self.symbol_table.curr_method_name
            error_msg = error_msg + " the index of array " + str(element.array_name_id.name)
            error_msg = error_msg + " must be IntegerType"
            MJLogger.semantic_log(self.src_file_name, SemanticErrorType.INDEX_TYPE_MISMATCH.name, error_msg)


        right_side_type = element.right_side_exp.accept_type(self)

        if((not isinstance(array_type, IntArrayType)) or (not isinstance(right_side_type, IntegerType))):
            self.add_semantic_error(SemanticErrorType.ARRAY_ASSIGN_TYPE_MISMATCH)
            error_msg = self.symbol_table.curr_class_name + "#" + self.symbol_table.curr_method_name
            error_msg = error_msg + " the array " + str(element.array_name_id.name)
            error_msg = error_msg + " must be IntArrayType and must be assigned with values of IntegerType"
            MJLogger.semantic_log(self.src_file_name, SemanticErrorType.ARRAY_ASSIGN_TYPE_MISMATCH.name, error_msg)

        return None

    
    def visit_and(self, element: And) -> Type:
        left_side_type = element.left_side_exp.accept_type(self)
        if(not isinstance(left_side_type, BooleanType)):
            self.add_semantic_error(SemanticErrorType.AND_TYPE_MISMATCH)
            error_msg = self.symbol_table.curr_class_name + "#" + self.symbol_table.curr_method_name
            error_msg = error_msg + " the AND left side type must be BooleanType"
            MJLogger.semantic_log(self.src_file_name, SemanticErrorType.AND_TYPE_MISMATCH.name, error_msg)
            return None

        right_side_type = element.right_side_exp.accept_type(self)
        if(not isinstance(right_side_type, BooleanType)):
            self.add_semantic_error(SemanticErrorType.AND_TYPE_MISMATCH)
            error_msg = self.symbol_table.curr_class_name + "#" + self.symbol_table.curr_method_name
            error_msg = error_msg + " the AND right side type must be BooleanType"
            MJLogger.semantic_log(self.src_file_name, SemanticErrorType.AND_TYPE_MISMATCH.name, error_msg)
            return None

        return BooleanType()

    def visit_less_than(self, element: LessThan) -> Type:
        left_side_type = element.left_side_exp.accept_type(self)
        if(not isinstance(left_side_type, IntegerType)):
            self.add_semantic_error(SemanticErrorType.LESS_THAN_TYPE_MISMATCH)
            error_msg = self.symbol_table.curr_class_name + "#" + self.symbol_table.curr_method_name
            error_msg = error_msg + " the LessThen left side type must be IntegerType"
            MJLogger.semantic_log(self.src_file_name, SemanticErrorType.LESS_THAN_TYPE_MISMATCH.name, error_msg)
            return None

        right_side_type = element.right_side_exp.accept_type(self)
        if(not isinstance(right_side_type, IntegerType)):
            self.add_semantic_error(SemanticErrorType.LESS_THAN_TYPE_MISMATCH)
            error_msg = self.symbol_table.curr_class_name + "#" + self.symbol_table.curr_method_name
            error_msg = error_msg + " the LessThen right side type must be IntegerType"
            MJLogger.semantic_log(self.src_file_name, SemanticErrorType.LESS_THAN_TYPE_MISMATCH.name, error_msg)
            return None

        return BooleanType()


    def visit_plus(self, element: Plus) -> Type:
        left_side_type = element.left_side_exp.accept_type(self)
        if(not isinstance(left_side_type, IntegerType)):
            self.add_semantic_error(SemanticErrorType.PLUS_TYPE_MISMATCH)
            error_msg = self.symbol_table.curr_class_name + "#" + self.symbol_table.curr_method_name
            error_msg = error_msg + " the PLUS left side type must be IntegerType"
            MJLogger.semantic_log(self.src_file_name, SemanticErrorType.PLUS_TYPE_MISMATCH.name, error_msg)
            return None

        right_side_type = element.right_side_exp.accept_type(self)
        if(not isinstance(right_side_type, IntegerType)):
            self.add_semantic_error(SemanticErrorType.PLUS_TYPE_MISMATCH)
            error_msg = self.symbol_table.curr_class_name + "#" + self.symbol_table.curr_method_name
            error_msg = error_msg + " the PLUS right side type must be IntegerType"
            MJLogger.semantic_log(self.src_file_name, SemanticErrorType.PLUS_TYPE_MISMATCH.name, error_msg)
            return None

        return IntegerType()


    def visit_minus(self, element: Minus) -> Type:
        left_side_type = element.left_side_exp.accept_type(self)
        if(not isinstance(left_side_type, IntegerType)):
            self.add_semantic_error(SemanticErrorType.MINUS_TYPE_MISMATCH)
            error_msg = self.symbol_table.curr_class_name + "#" + self.symbol_table.curr_method_name
            error_msg = error_msg + " the MINUS left side type must be IntegerType"
            MJLogger.semantic_log(self.src_file_name, SemanticErrorType.MINUS_TYPE_MISMATCH.name, error_msg)
            return None

        right_side_type = element.right_side_exp.accept_type(self)
        if(not isinstance(right_side_type, IntegerType)):
            self.add_semantic_error(SemanticErrorType.MINUS_TYPE_MISMATCH)
            error_msg = self.symbol_table.curr_class_name + "#" + self.symbol_table.curr_method_name
            error_msg = error_msg + " the MINUS right side type must be IntegerType"
            MJLogger.semantic_log(self.src_file_name, SemanticErrorType.MINUS_TYPE_MISMATCH.name, error_msg)
            return None

        return IntegerType()

    
    def visit_times(self, element: Times) -> Type:
        left_side_type = element.left_side_exp.accept_type(self)
        if(not isinstance(left_side_type, IntegerType)):
            self.add_semantic_error(SemanticErrorType.TIMES_TYPE_MISMATCH)
            error_msg = self.symbol_table.curr_class_name + "#" + self.symbol_table.curr_method_name
            error_msg = error_msg + " the TIMES left side type must be IntegerType"
            MJLogger.semantic_log(self.src_file_name, SemanticErrorType.TIMES_TYPE_MISMATCH.name, error_msg)
            return None

        right_side_type = element.right_side_exp.accept_type(self)
        if(not isinstance(right_side_type, IntegerType)):
            self.add_semantic_error(SemanticErrorType.TIMES_TYPE_MISMATCH)
            error_msg = self.symbol_table.curr_class_name + "#" + self.symbol_table.curr_method_name
            error_msg = error_msg + " the TIMES right side type must be IntegerType"
            MJLogger.semantic_log(self.src_file_name, SemanticErrorType.TIMES_TYPE_MISMATCH.name, error_msg)
            return None

        return IntegerType()


    def visit_array_lookup(self, element: ArrayLookup) -> Type:
        out_side_exp_type = element.out_side_exp.accept_type(self)
        if(not isinstance(out_side_exp_type, IntArrayType)):
            self.add_semantic_error(SemanticErrorType.ARRAY_TYPE_MISMATCH)
            error_msg = self.symbol_table.curr_class_name + "#" + self.symbol_table.curr_method_name
            error_msg = error_msg + " array must be IntArrayType"
            MJLogger.semantic_log(self.src_file_name, SemanticErrorType.ARRAY_TYPE_MISMATCH.name, error_msg)
            return None

        in_side_exp_type = element.in_side_exp.accept_type(self)
        if(not isinstance(in_side_exp_type, IntegerType)):
            self.add_semantic_error(SemanticErrorType.INDEX_TYPE_MISMATCH)
            error_msg = self.symbol_table.curr_class_name + "#" + self.symbol_table.curr_method_name
            error_msg = error_msg + " the index of array must be IntegerType"
            MJLogger.semantic_log(self.src_file_name, SemanticErrorType.INDEX_TYPE_MISMATCH.name, error_msg)
            return None

        return IntegerType()

    def visit_array_length(self, element: ArrayLength) -> Type:
        length_exp_type = element.length_exp.accept_type(self)
        if(not isinstance(length_exp_type, IntArrayType)):
            self.add_semantic_error(SemanticErrorType.ARRAY_LENGTH_TYPE_MISMATCH)
            error_msg = self.symbol_table.curr_class_name + "#" + self.symbol_table.curr_method_name
            error_msg = error_msg + " array must be IntArrayType"
            MJLogger.semantic_log(self.src_file_name, SemanticErrorType.ARRAY_LENGTH_TYPE_MISMATCH.name, error_msg)
            return None

        return IntegerType()


    def visit_call(self, element: Call) -> Type:
        callee_exp_type = element.callee_exp.accept_type(self)
        
        if(not isinstance(callee_exp_type, IdentifierType)):
            self.add_semantic_error(SemanticErrorType.INVALID_OBJECT_IDENTIFIER)
            error_msg = self.symbol_table.curr_class_name + "#" + self.symbol_table.curr_method_name
            error_msg = error_msg + " invalid object identifier in call."
            MJLogger.semantic_log(self.src_file_name, SemanticErrorType.INVALID_OBJECT_IDENTIFIER.name, error_msg)
            return None
        
        class_entry = self.symbol_table.get_class_entry(callee_exp_type.name)
        if(class_entry is None):
            self.add_semantic_error(SemanticErrorType.UNDECLARED_CLASS)
            error_msg = self.symbol_table.curr_class_name + "#" + self.symbol_table.curr_method_name
            error_msg = error_msg + " " + callee_exp_type.name + " is an undeclared class in call."                
            MJLogger.semantic_log(self.src_file_name, SemanticErrorType.UNDECLARED_CLASS.name, error_msg)
            return None
        
        method_entry = class_entry.get_method(element.callee_name_id.name)

        if(method_entry is None):
            self.add_semantic_error(SemanticErrorType.UNDECLARED_METHOD)
            error_msg = self.symbol_table.curr_class_name + "#" + self.symbol_table.curr_method_name
            error_msg = error_msg + " " + element.callee_name_id.name + " is an undeclared method in call."                
            MJLogger.semantic_log(self.src_file_name, SemanticErrorType.UNDECLARED_METHOD.name, error_msg)
            return None
        
        method_return_type = method_entry.get_return_type()
        if(element.arg_list.size() != method_entry.get_num_params()):
            self.add_semantic_error(SemanticErrorType.WRONG_ARG_NUMBER)
            error_msg = self.symbol_table.curr_class_name + "#" + self.symbol_table.curr_method_name
            error_msg = error_msg + " " + element.callee_name_id.name + " wrong number of args for call."                
            MJLogger.semantic_log(self.src_file_name, SemanticErrorType.WRONG_ARG_NUMBER.name, error_msg)
            return method_return_type


        for index in range(element.arg_list.size()):
            arg_type = element.arg_list.element_at(index).accept_type(self)
            expected_type = method_entry.get_param_by_position(index)

            if((arg_type is None) or (type(arg_type) != type(expected_type))):
                self.add_semantic_error(SemanticErrorType.ARG_TYPE_MISMATCH)
                error_msg = self.symbol_table.curr_class_name + "#" + self.symbol_table.curr_method_name
                error_msg = error_msg + " expected " + str(type(expected_type)) + " got " + str(type(arg_type))                
                MJLogger.semantic_log(self.src_file_name, SemanticErrorType.ARG_TYPE_MISMATCH.name, error_msg)                

        return method_return_type


    def visit_integer_literal(self, element: IntegerLiteral) -> Type:
        return IntegerType()


    def visit_true_exp(self, element: TrueExp) -> Type:
        return BooleanType()


    def visit_false_exp(self, element: FalseExp) -> Type:
        return BooleanType()


    def visit_identifier_exp(self, element: IdentifierExp) -> Type:
        return_type = None

        if(self.symbol_table.curr_method is not None):
            return_type = self.symbol_table.curr_method.get_param_by_name(element.name)
            if(return_type is None):
                return_type = self.symbol_table.curr_method.get_local_by_name(element.name)
                if(return_type is not None):
                    return return_type
            else:
                return return_type

        if(self.symbol_table.curr_class is not None):
            return_type = self.symbol_table.curr_class.get_field(element.name)
            if(return_type is not None):
                return return_type

        self.add_semantic_error(SemanticErrorType.UNDECLARED_IDENTIFIER)
        error_msg = self.symbol_table.curr_class_name + "#" + self.symbol_table.curr_method_name
        error_msg = error_msg + element.name + " is an undeclared identifier."                
        MJLogger.semantic_log(self.src_file_name, SemanticErrorType.UNDECLARED_IDENTIFIER.name, error_msg)

        return return_type


    def visit_this(self, element: This) -> Type:
        if(self.symbol_table.curr_class is None):
            self.add_semantic_error(SemanticErrorType.UNDECLARED_CLASS)
            error_msg = self.symbol_table.curr_class_name + "#" + self.symbol_table.curr_method_name
            error_msg = error_msg + " calling THIS is an undeclared class."
            MJLogger.semantic_log(self.src_file_name, SemanticErrorType.UNDECLARED_CLASS.name, error_msg)
        
        return IdentifierType(self.symbol_table.curr_class_name)


    def visit_new_array(self, element: NewArray) -> Type:
        new_exp_type = element.new_exp.accept_type(self)
        if(not isinstance(new_exp_type, IntegerType)):
            self.add_semantic_error(SemanticErrorType.NEW_ARRAY_TYPE_MISMATCH)
            error_msg = self.symbol_table.curr_class_name + "#" + self.symbol_table.curr_method_name
            error_msg = error_msg + " new array type mismatch."
            MJLogger.semantic_log(self.src_file_name, SemanticErrorType.NEW_ARRAY_TYPE_MISMATCH.name, error_msg)            
        
        return IntArrayType()


    def visit_new_object(self, element: NewObject) -> Type:
        if(not self.symbol_table.contains_class(element.object_name_id.name)):
            self.add_semantic_error(SemanticErrorType.NEW_OBJECT_UNDECLARED_CLASS)
            error_msg = self.symbol_table.curr_class_name + "#" + self.symbol_table.curr_method_name
            error_msg = error_msg + element.object_name_id.name + " is an undeclared class."
            MJLogger.semantic_log(self.src_file_name, SemanticErrorType.NEW_OBJECT_UNDECLARED_CLASS.name, error_msg)

        return IdentifierType(element.object_name_id.name)


    def visit_not(self, element: Not) -> Type:
        negated_exp_type = element.negated_exp.accept_type(self)

        if(not isinstance(negated_exp_type, BooleanType)):
            self.add_semantic_error(SemanticErrorType.NOT_TYPE_MISMATCH)
            error_msg = self.symbol_table.curr_class_name + "#" + self.symbol_table.curr_method_name
            error_msg = error_msg + " the NOT expression must be BooleanType."
            MJLogger.semantic_log(self.src_file_name, SemanticErrorType.NOT_TYPE_MISMATCH.name, error_msg)
            return None

        return BooleanType()


    def visit_identifier(self, element: Identifier) -> Type:
        return_type = None

        if(self.symbol_table.curr_method is not None):
            return_type = self.symbol_table.curr_method.get_param_by_name(element.name)

            if((return_type is None) and (self.symbol_table.curr_method == "main")):
                return IntArrayType()

            if(return_type is None):
                return_type = self.symbol_table.curr_method.get_local_by_name(element.name)
                if(return_type is not None):
                    return return_type
            else:
                return return_type

        if(self.symbol_table.curr_class is not None):
            return_type = self.symbol_table.curr_class.get_field(element.name)
            if(return_type is not None):
                return return_type

        if(self.symbol_table.contains_class(element.name)):
            return_type = IdentifierType(element.name)
        
        return return_type


#TODO
class TranslateVisitor(IRVisitor):

    def __init__(self, symbol_table: SymbolTable, frame: Frame) -> None:
        super().__init__()
        self.symbol_table: SymbolTable = symbol_table
        self.current_frame: Frame = frame
        self.frags: translate.Frag = translate.Frag()
        self.head_frags = self.frags
        self.var_access = {}
        self.src_file_name = "UnknownSRCFile"
        self.call_class_name = None

    def set_symbol_table(self, symbol_table: SymbolTable):
        self.symbol_table = symbol_table

    def get_symbol_table(self) -> SymbolTable:
        return self.symbol_table

    def proc_entry_exit(self, body: tree.Stm) -> None:
        proc_frag = translate.ProcFrag(body, self.current_frame)
        self.frags.add_next(proc_frag)
        self.frags = self.frags.get_next()

    def get_result(self) -> translate.Frag:
        return self.head_frags

    def visit_program(self, element: Program) -> translate.Exp:
        element.main_class.accept_ir(self)

        for index in range(len(element.class_decl_list)):
            element.class_decl_list.element_at(index).accept_ir(self)

        return None

    def visit_main_class(self, element: MainClass) -> translate.Exp:
        element.class_name_id.accept_ir(self)
        element.arg_name_id.accept_ir(self)
        self.symbol_table.set_curr_class(element.class_name_id.name)
        self.symbol_table.set_curr_method("main")

        escapes_list = List[bool]
        for i in range(self.symbol_table.curr_method.get_num_params()):
            escapes_list.append(False)
        
        frame_aux = self.current_frame.new_frame(Symbol.symbol(element.class_name_id.name + "$" + self.symbol_table.curr_method_name), escapes_list)
        self.current_frame = frame_aux
        
        stmt: translate.Exp = element.statement.accept_ir(self)
        return_exp: translate.Exp = translate.Exp(tree.CONST(0))
        body: tree.Stm = tree.MOVE(tree.TEMP(self.current_frame.RV()), tree.ESEQ(tree.EXP(stmt.un_ex()), return_exp.un_ex()))

        stmt_list = List[tree.Stm]
        stmt_list.append(body)
        self.current_frame.proc_entry_exit1(stmt_list)
        self.proc_entry_exit(Converter.to_SEQ(stmt_list))

        return None


    def visit_class_decl_extends(self, element: ClassDeclExtends) -> translate.Exp:
        self.symbol_table.set_curr_class(element.class_name_id.name)
        element.class_name_id.accept_ir(self)
        element.super_class_name_id.accept_ir(self)

        for index in range(element.var_decl_list.size()):
            element.var_decl_list.element_at(index).accept_ir(self)
        
        for index in range(element.method_decl_list.size()):
            element.method_decl_list.element_at(index).accept_ir(self)

        return None

    def visit_class_decl_simple(self, element: ClassDeclSimple) -> translate.Exp:
        self.symbol_table.set_curr_class(element.class_name_id.name)
        element.class_name_id.accept_ir(self)

        for index in range(element.var_decl_list.size()):
            element.var_decl_list.element_at(index).accept_ir(self)
        
        for index in range(element.method_decl_list.size()):
            element.method_decl_list.element_at(index).accept_ir(self)

        return None

    def visit_var_decl(self, element: VarDecl) -> translate.Exp:
        element.name_id.accept_ir(self)
        element.type.accept_ir(self)
        return None
  
    def visit_method_decl(self, element: MethodDecl) -> translate.Exp:
        self.symbol_table.set_curr_method(element.name_id.name)
        element.type.accept_ir(self)
        element.name_id.accept_ir(self)

        escapes_list = List[bool]

        for index in range(element.formal_param_list.size()):
            element.formal_param_list.element_at(index).accept_ir(self)
            escapes_list.append(False)

        for index in range(element.var_decl_list.size()):
            element.var_decl_list.element_at(index).accept_ir(self)

        self.current_frame = self.current_frame.new_frame(Symbol.symbol(self.symbol_table.curr_class_name + "$" + self.symbol_table.curr_method_name), escapes_list)

        body: tree.Stm
        body_list = List[tree.Stm]
        return_exp: tree.Exp = element.return_exp.accept_ir(self).un_ex()

        if element.statement_list.size() == 0:
            body = tree.MOVE(tree.TEMP(self.current_frame.RV()), return_exp)
        else:
            body = tree.EXP(element.statement_list.element_at(0).accept_ir(self).un_ex())
            for i in range(1, element.statement_list.size()):
                body = tree.SEQ(body, tree.EXP(element.statement_list.element_at(i).accept_ir(self).un_ex()))
            
            body = tree.MOVE(tree.TEMP(self.current_frame.RV()), tree.ESEQ(body, return_exp))
        
        body_list.append(body)
        self.current_frame.proc_entry_exit1(body_list)
        self.proc_entry_exit(Converter.to_SEQ(body_list))
        self.var_access = {}
        return None

    
    def visit_formal(self, element: Formal) -> translate.Exp:
        element.type.accept_ir(self)
        element.name_id.accept_ir(self)
        return None

    def visit_int_array_type(self, element: IntArrayType) -> translate.Exp:
        return None

    def visit_boolean_type(self, element: BooleanType) -> translate.Exp:
        return None

    def visit_integer_type(self, element: IntegerType) -> translate.Exp:
        return None


    def visit_identifier_type(self, element: IdentifierType) -> translate.Exp:
        return None


    def visit_block(self, element: Block) -> translate.Exp:
        if(element.statement_list.size() == 0):
            return translate.Nx(None)

        exp: translate.Exp = element.statement_list.element_at(0).accept_ir(self)
        
        if(element.statement_list.size() == 1):
            return exp
        
        stm: tree.Stm = exp.un_nx()
        
        for i in range(1, element.statement_list.size()):
            exp = element.statement_list.element_at(i).accept_ir(self)
            stm = tree.SEQ(stm, exp.un_nx())

        return translate.Nx(stm)

       
    def visit_if(self, element: If) -> translate.Exp:
        exp: translate.Exp = element.condition_exp.accept_ir(self)
        if_stm: translate.Exp = element.if_statement.accept_ir(self)
        else_stm: translate.Exp = element.else_statement.accept_ir(self)
        
        true_label: temp.Label = temp.Label()
        false_label: temp.Label = temp.Label()
        end_if_label: temp.Label = temp.Label()

        return translate.Nx(tree.SEQ(
                                tree.SEQ(
                                    tree.SEQ(
                                        tree.SEQ(
                                            tree.CJUMP(tree.CJUMP.EQ, exp.un_ex(), tree.CONST(1), true_label, false_label),
                                            tree.SEQ(tree.LABEL(true_label), if_stm.un_nx())),
                                        tree.JUMP(end_if_label)),
                                    tree.SEQ(tree.LABEL(false_label), else_stm.un_nx())), 
                                tree.LABEL(end_if_label)))
  

    def visit_while(self, element: While) -> translate.Exp:
        test: temp.Label = temp.Label()
        true_label: temp.Label = temp.Label()
        false_label: temp.Label = temp.Label()
        exp: translate.Exp = element.condition_exp.accept_ir(self)
        body: translate.Exp = element.statement.accept_ir(self)

       
        return translate.Nx(tree.SEQ(
                                tree.SEQ(
                                    tree.SEQ(tree.LABEL(test),
                                             tree.CJUMP(tree.CJUMP.EQ, exp.un_ex(), tree.CONST(1),true_label,false_label)),
                                    tree.SEQ(tree.LABEL(true_label),body.un_nx())), 
                                tree.LABEL(false_label)))



    def visit_print(self, element: Print) -> translate.Exp:
        print_exp: translate.Exp = element.print_exp.accept_ir(self)
        
        args = List[tree.Exp]
        args.add(print_exp.un_ex())
        
        exp: tree.Exp = self.current_frame.external_call("print", args)

        return translate.Nx(tree.MOVE(tree.TEMP(temp.Temp()), exp))

    def visit_assign(self, element: Assign) -> translate.Exp:
        var: translate.Exp = element.left_side_id.accept_ir(self)
        exp: translate.Exp = element.right_side_exp.accept_ir(self)
        
        if (isinstance(var.un_ex(), tree.TEMP)):
            return translate.Nx(tree.MOVE (var.un_ex(),  exp.un_ex()))
        else:
            temp: temp.Temp = temp.Temp()
            return translate.Nx(tree.MOVE(tree.MEM(tree.BINOP.PLUS, tree.TEMP(temp), var.un_ex())), exp.un_ex())


    def visit_array_assign(self, element: ArrayAssign) -> translate.Exp:
        word_size = self.current_frame.word_size()
        array_exp: tree.Exp = element.array_name_id.accept_ir(self).un_ex()

        if (not isinstance(array_exp, tree.TEMP)):
            temp_01: temp.Temp = temp.Temp()
            temp_02: temp.Temp = temp.Temp()
            array_exp = tree.ESEQ(tree.SEQ(
                                tree.MOVE(tree.TEMP(temp_01), tree.BINOP(tree.BINOP.MUL, array_exp, tree.CONST(word_size))), 
                                tree.MOVE(tree.TEMP(temp_02), tree.MEM(tree.BINOP(tree.BINOP.PLUS, tree.TEMP(temp.Temp(0), tree.TEMP(temp_01))))), 
                                tree.TEMP(temp_02)))


        index_exp: tree.Exp = element.array_exp.accept_ir(self).un_ex()
        temp_index = temp.Temp = temp.Temp()
        temp_size = temp.Temp = temp.Temp()
        args: tree.ExpList = tree.ExpList()
        true_label: temp.Label = temp.Label()
        false_label: temp.Label = temp.Label()

        index_exp = tree.ESEQ(
                        tree.SEQ(
                            tree.SEQ(
                                tree.SEQ(
                                    tree.SEQ(
                                        tree.SEQ(
                                            tree.MOVE(
                                                tree.TEMP(temp_index), 
                                                tree.BINOP(tree.BINOP.MUL, index_exp, tree.CONST(word_size))),
                                            tree.MOVE(tree.TEMP(temp_size), tree.MEM(array_exp))),
                                        tree.CJUMP(tree.CJUMP.GE, tree.TEMP(temp_index), tree.TEMP(temp_size), true_label, false_label)),
                                    tree.LABEL(true_label)),
                                tree.MOVE(
                                    tree.TEMP(temp.Temp()), 
                                    self.current_frame.external_call("_error", args))), 
                            tree.LABEL(false_label)),
                        tree.TEMP(temp_index))



        value_exp: tree.Exp = element.right_side_exp.accept_ir(self).un_ex()
        
        return translate.Nx(
            tree.MOVE(tree.MEM(
                          tree.BINOP(
                               tree.BINOP.PLUS, array_exp, 
                               tree.BINOP(tree.BINOP.PLUS, index_exp,tree.CONST(word_size)))), 
                      value_exp))


    def visit_and(self, element: And) -> translate.Exp:
        left_side_exp: translate.Exp = element.left_side_exp.accept_ir(self)
        right_side_exp: translate.Exp = element.right_side_exp.accept_ir(self)

        binop: tree.BINOP = tree.BINOP(tree.BINOP.AND, left_side_exp.un_ex(), right_side_exp.un_ex())
        return translate.Ex(binop)


    def visit_less_than(self, element: LessThan) -> translate.Exp:
        left_side_exp: translate.Exp = element.left_side_exp.accept_ir(self)
        right_side_exp: translate.Exp = element.right_side_exp.accept_ir(self)

        return translate.RelCx(tree.CJUMP.LT, right_side_exp.un_ex(), left_side_exp.un_ex())



    def visit_plus(self, element: Plus) -> translate.Exp:
        left_side_exp: translate.Exp = element.left_side_exp.accept_ir(self)
        right_side_exp: translate.Exp = element.right_side_exp.accept_ir(self)

        binop: tree.BINOP = tree.BINOP(tree.BINOP.PLUS, left_side_exp.un_ex(), right_side_exp.un_ex())
        return translate.Ex(binop)


    def visit_minus(self, element: Minus) -> translate.Exp:
        left_side_exp: translate.Exp = element.left_side_exp.accept_ir(self)
        right_side_exp: translate.Exp = element.right_side_exp.accept_ir(self)

        binop: tree.BINOP = tree.BINOP(tree.BINOP.MINUS, left_side_exp.un_ex(), right_side_exp.un_ex())
        return translate.Ex(binop)



    def visit_times(self, element: Times) -> translate.Exp:
        left_side_exp: translate.Exp = element.left_side_exp.accept_ir(self)
        right_side_exp: translate.Exp = element.right_side_exp.accept_ir(self)

        binop: tree.BINOP = tree.BINOP(tree.BINOP.MUL, left_side_exp.un_ex(), right_side_exp.un_ex())
        return translate.Ex(binop)


    def visit_array_lookup(self, element: ArrayLookup) -> translate.Exp:
        t_index: temp.Temp = temp.Temp()
        t_size: temp.Temp() = temp.Temp()
        array: translate.Exp = element.out_side_exp.accept_ir(self).un_ex()
        index: translate.Exp = element.in_side_exp.accept_ir(self).un_ex()
        false_label: temp.Label = temp.Label()
        true_label: temp.Label = temp.Label()
        args = List[tree.Exp]
        word_size = self.current_frame.word_size()

        stm_01: tree.Stm = tree.SEQ(
                                tree.SEQ(
                                    tree.SEQ(
                                        tree.SEQ(
                                            tree.SEQ(
                                                tree.MOVE(tree.TEMP(t_index),tree.BINOP(tree.BINOP.MUL,index,tree.CONST(word_size))),
                                                tree.MOVE(tree.TEMP(t_size),tree.MEM(array))),
                                            tree.CJUMP(tree.CJUMP.GE,tree.TEMP(t_index),tree.TEMP(t_size),true_label,false_label)),
                                            tree.LABEL(true_label)),
                                            tree.MOVE(tree.TEMP(temp.Temp()), self.current_frame.external_call("_error",args))),
                                tree.LABEL(false_label))
        
        t: temp.Temp = temp.Temp()
        stm_02: tree.Stm = tree.SEQ(
                                stm_01,
                                tree.MOVE(
                                    tree.TEMP(t),
                                    tree.MEM(
                                        tree.BINOP(
                                            tree.BINOP.PLUS,array,
                                            tree.BINOP(
                                                tree.BINOP.PLUS,
                                                tree.BINOP(
                                                    tree.BINOP.MUL, index, 
                                                    tree.CONST(word_size)),
                                                    tree.CONST(word_size))))))
        
        return translate.Ex(tree.ESEQ(stm_02,tree.TEMP(t)))


    def visit_array_length(self, element: ArrayLength) -> translate.Exp:
        exp: translate.Exp = element.length_exp.accept_ir(self)
        mem: tree.MEM = tree.MEM(exp.un_ex())
        return translate.Ex(mem)

    def visit_call(self, element: Call) -> translate.Exp:
        class_exp: translate.Exp = element.callee_exp.accept_ir(self)
        fn_label: temp.Label = temp.Label(self.call_class_name + "$" + element.callee_name_id.name)
        
        arg_list: tree.ExpList = tree.ExpList(class_exp.un_ex(), None)
        args = List[tree.Exp]
        
        args.append(class_exp.un_ex())

        for i in range(element.arg_list.size()):
            arg: translate.Exp = element.arg_list.element_at(i).accept_ir(self)
            args.insert(0, arg.un_ex())
        
        arg_list = Converter.to_ExpList(args)
        fn_call: tree.CALL = tree.CALL(tree.NAME(fn_label), arg_list)
        return translate.Ex(fn_call)


    def visit_integer_literal(self, element: IntegerLiteral) -> translate.Exp:
        return translate.Ex(tree.CONST(element.value))

    def visit_true_exp(self, element: TrueExp) -> translate.Exp:
        true_const = tree.CONST(1)
        return translate.Ex(true_const)


    def visit_false_exp(self, element: FalseExp) -> translate.Exp:
        false_const = tree.CONST(0)
        return translate.Ex(false_const)


    def visit_identifier_exp(self, element: IdentifierExp) -> translate.Exp:
        type: Type  = self.symbol_table.curr_method.get_param_by_name(element.name)
        
        if(type is None):
            type = self.symbol_table.curr_method.get_local_by_name(element.name)
            if(type is None):
                type = self.symbol_table.curr_class.get_field(element.name)
        
        if (isinstance(type, IdentifierType)):
            self.call_class_name = type.name
            
        access: Access = self.var_access.get(element.name)
        if (access is None):
            access = self.current_frame.alloc_local(False)
            self.var_access[element.name] = access

        return translate.Ex(access.exp(tree.TEMP(self.current_frame.FP())))

    def visit_this(self, element: This) -> translate.Exp:
        self.call_class_name = self.symbol_table.curr_class_name
        return translate.Ex(tree.MEM(tree.TEMP(self.current_frame.FP())))


    def visit_new_array(self, element: NewArray) -> translate.Exp:
        exp: translate.Exp = element.new_exp.accept_ir(self)
        word_size = self.current_frame.word_size()
        # computing array size
        num_of_items: tree.BINOP = tree.BINOP(tree.BINOP.PLUS, exp.un_ex(), tree.CONST(1))
        array_size: tree.Exp = tree.BINOP(tree.BINOP.MUL, num_of_items, tree.CONST(word_size))

        temp_01: temp.Temp = temp.Temp()
        temp_02: temp.Temp = temp.Temp()
        args = List[tree.Exp]
        args.append(array_size)
        
       # call malloc get pointer to space allocated in temp_01
        alloc: tree.Exp = self.current_frame.external_call("malloc", args)
        stm_01: tree.Stm = tree.MOVE(tree.TEMP(temp_01), alloc)

        cj: temp.Label = temp.Label()
        false_label: temp.Label = temp.Label()
        true_label: temp.Label = temp.Label()

        # array initialization
        stm_02: tree.Stm = tree.SEQ(
                                tree.SEQ(
                                    tree.SEQ(
                                        tree.SEQ(
                                            tree.SEQ(
                                                tree.SEQ(
                                                    tree.MOVE(tree.TEMP(temp_02),tree.CONST(word_size)),
                                                    tree.SEQ(tree.LABEL(cj), tree.CJUMP(tree.CJUMP.LT, tree.TEMP(temp_02), array_size, false_label, true_label))),
                                                tree.LABEL(true_label)),
                                            tree.MOVE(tree.MEM(tree.BINOP(tree.BINOP.PLUS,tree.TEMP(temp_01),tree.TEMP(temp_02))),tree.CONST(0))),
                                        tree.MOVE(tree.TEMP(temp_02),tree.BINOP(tree.BINOP.PLUS,tree.TEMP(temp_02), tree.CONST(word_size)))),
                                    tree.JUMP(cj)),
                                tree.SEQ(tree.LABEL(false_label),tree.MOVE(tree.MEM(tree.TEMP(temp_01)),tree.BINOP(tree.BINOP.MUL,exp.un_ex(),tree.CONST(word_size)))))

	       
        return translate.Ex(tree.ESEQ(tree.SEQ(stm_01,stm_02), tree.TEMP(temp_01)))


    def visit_new_object(self, element: NewObject) -> translate.Exp:
        self.call_class_name = element.object_name_id.name
        c: ClassEntry = self.symbol_table.get_class_entry(element.object_name_id.name)
        tam: int = len(c.get_fields().keys())

        params = List[tree.Exp]
        params.append(tree.BINOP(tree.BINOP.MUL, tree.CONST(tam + 1), tree.CONST(self.current_frame.word_size())))
        
        alloc: tree.Exp = self.current_frame.external_call("malloc", params)
        return translate.Ex(tree.MOVE(tree.TEMP(temp.Temp()), alloc))


    def visit_not(self, element: Not) -> translate.Exp:
        exp: translate.Exp = element.negated_exp.accept_ir(self)
        binop: tree.BINOP = tree.BINOP(tree.BINOP.XOR, tree.CONST(1), exp.un_ex())
        return translate.Ex(binop)


    def visit_identifier(self, element: Identifier) -> translate.Exp:
        self.call_class_name = element.name
        access: Access = self.var_access.get(element.name)
        if access is None:
            access = self.current_frame.alloc_local(False)
            self.var_access[element.name] = access
        
        return translate.Ex(access.exp(tree.TEMP(self.current_frame.FP())))