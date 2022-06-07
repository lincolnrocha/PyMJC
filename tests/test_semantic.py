import json
import os
import unittest
from pymjc.front.ast import Program

from pymjc.front.lexer import MJLexer
from pymjc.front.parser import MJParser
from pymjc.front.visitor import FillSymbolTableVisitor, TypeCheckingVisitor

from tests import util


class SemanticTest(unittest.TestCase):
    
    actual_values = {}
    
    test_suite_oracles = {}

    @classmethod
    def setUpClass(cls):
        test_suite_oracles_path = os.path.dirname(os.path.realpath(__file__)) + str(os.path.sep) + "testoracle" + str(os.path.sep) + "semantic_test_suite_oracles.json"
        with open(test_suite_oracles_path) as test_suite_oracles_file:
            cls.test_suite_oracles = json.load(test_suite_oracles_file)
            test_suite_oracles_file.close()

        test_data_path = os.path.dirname(os.path.realpath(__file__)) + str(os.path.sep) + "testdata" + str(os.path.sep)
        test_correct_files_path = os.path.join(test_data_path, "correct")
        file_name_list = os.listdir(test_correct_files_path)
        
        test_data_file_path_map = {}

        for file_name in file_name_list:
            test_data_file_path_map[file_name] = os.path.join(test_correct_files_path, file_name)

        test_faulty_files_path = os.path.join(test_data_path, "faulty" + str(os.path.sep) + "semantic")
        file_name_list = os.listdir(test_faulty_files_path)

        for file_name in file_name_list:
            test_data_file_path_map[file_name] = os.path.join(test_faulty_files_path, file_name)

        for file_name in cls.test_suite_oracles:
            with open(test_data_file_path_map[file_name], "r") as source_test_file:
                content = source_test_file.read()
                lexer = MJLexer()
                lexer.src_file_name = file_name
                parser = MJParser()
                parser.src_file_name = file_name
                program: Program = parser.parse(lexer.tokenize(content))
                symbol_table_creator = FillSymbolTableVisitor()
                symbol_table_creator.src_file_name = file_name
                symbol_table_creator.init_semantic_errors()
                symbol_table_creator.visit_program(program)

                type_checker = TypeCheckingVisitor()
                type_checker.src_file_name = file_name
                type_checker.fill_semantic_errors(symbol_table_creator.semantic_errors)
                type_checker.set_symbol_table(symbol_table_creator.get_symbol_table())
                type_checker.visit_program(program)

                semantic_errors = type_checker.semantic_errors
                source_test_file.close()
                cls.actual_values[file_name] = util.compute_semantic_oracles(semantic_errors)                


    def test_number_of_already_declared_class(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_ALREADY_DECLARED_CLASS"]
            expected = self.test_suite_oracles[test_file_name]["number_of_ALREADY_DECLARED_CLASS"]
            self.assertEqual(actual, expected, test_file_name)


    def test_number_of_already_declared_method(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_ALREADY_DECLARED_METHOD"]
            expected = self.test_suite_oracles[test_file_name]["number_of_ALREADY_DECLARED_METHOD"]
            self.assertEqual(actual, expected, test_file_name)

    def test_number_of_already_declared_field(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_ALREADY_DECLARED_FIELD"]
            expected = self.test_suite_oracles[test_file_name]["number_of_ALREADY_DECLARED_FIELD"]
            self.assertEqual(actual, expected, test_file_name)

    def test_number_of_already_declared_var(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_ALREADY_DECLARED_VAR"]
            expected = self.test_suite_oracles[test_file_name]["number_of_ALREADY_DECLARED_VAR"]
            self.assertEqual(actual, expected, test_file_name)
    
    def test_number_of_and_type_mismatch(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_AND_TYPE_MISMATCH"]
            expected = self.test_suite_oracles[test_file_name]["number_of_AND_TYPE_MISMATCH"]
            self.assertEqual(actual, expected, test_file_name)

    def test_number_of_arg_type_mismatch(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_ARG_TYPE_MISMATCH"]
            expected = self.test_suite_oracles[test_file_name]["number_of_ARG_TYPE_MISMATCH"]
            self.assertEqual(actual, expected, test_file_name)

    def test_number_of_array_assign_type_mismatch(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_ARRAY_ASSIGN_TYPE_MISMATCH"]
            expected = self.test_suite_oracles[test_file_name]["number_of_ARRAY_ASSIGN_TYPE_MISMATCH"]
            self.assertEqual(actual, expected, test_file_name)

    def test_number_of_array_length_type_mismatch(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_ARRAY_LENGTH_TYPE_MISMATCH"]
            expected = self.test_suite_oracles[test_file_name]["number_of_ARRAY_LENGTH_TYPE_MISMATCH"]
            self.assertEqual(actual, expected, test_file_name)

    def test_number_of_array_type_mismatch(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_ARRAY_TYPE_MISMATCH"]
            expected = self.test_suite_oracles[test_file_name]["number_of_ARRAY_TYPE_MISMATCH"]
            self.assertEqual(actual, expected, test_file_name)


    def test_number_of_assign_type_mismatch(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_ASSIGN_TYPE_MISMATCH"]
            expected = self.test_suite_oracles[test_file_name]["number_of_ASSIGN_TYPE_MISMATCH"]
            self.assertEqual(actual, expected, test_file_name)

    def test_number_of_duplicated_arg(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_DUPLICATED_ARG"]
            expected = self.test_suite_oracles[test_file_name]["number_of_DUPLICATED_ARG"]
            self.assertEqual(actual, expected, test_file_name)


    def test_number_of_if_type_mismatch(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_IF_TYPE_MISMATCH"]
            expected = self.test_suite_oracles[test_file_name]["number_of_IF_TYPE_MISMATCH"]
            self.assertEqual(actual, expected, test_file_name)

    def test_number_of_index_type_mismatch(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_INDEX_TYPE_MISMATCH"]
            expected = self.test_suite_oracles[test_file_name]["number_of_INDEX_TYPE_MISMATCH"]
            self.assertEqual(actual, expected, test_file_name)

    def test_number_of_invalid_object_identifier(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_INVALID_OBJECT_IDENTIFIER"]
            expected = self.test_suite_oracles[test_file_name]["number_of_INVALID_OBJECT_IDENTIFIER"]
            self.assertEqual(actual, expected, test_file_name)

    def test_number_of_less_than_type_mismatch(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_LESS_THAN_TYPE_MISMATCH"]
            expected = self.test_suite_oracles[test_file_name]["number_of_LESS_THAN_TYPE_MISMATCH"]
            self.assertEqual(actual, expected, test_file_name)

    def test_number_of_minus_type_mismatch(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_MINUS_TYPE_MISMATCH"]
            expected = self.test_suite_oracles[test_file_name]["number_of_MINUS_TYPE_MISMATCH"]
            self.assertEqual(actual, expected, test_file_name)

    def test_number_of_new_array_type_mismatch(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_NEW_ARRAY_TYPE_MISMATCH"]
            expected = self.test_suite_oracles[test_file_name]["number_of_NEW_ARRAY_TYPE_MISMATCH"]
            self.assertEqual(actual, expected, test_file_name)            

    def test_number_of_new_object_undeclared_class(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_NEW_OBJECT_UNDECLARED_CLASS"]
            expected = self.test_suite_oracles[test_file_name]["number_of_NEW_OBJECT_UNDECLARED_CLASS"]
            self.assertEqual(actual, expected, test_file_name)


    def test_number_of_not_type_mismatch(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_NOT_TYPE_MISMATCH"]
            expected = self.test_suite_oracles[test_file_name]["number_of_NOT_TYPE_MISMATCH"]
            self.assertEqual(actual, expected, test_file_name)

    def test_number_of_plus_type_mismatch(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_PLUS_TYPE_MISMATCH"]
            expected = self.test_suite_oracles[test_file_name]["number_of_PLUS_TYPE_MISMATCH"]
            self.assertEqual(actual, expected, test_file_name)

    def test_number_of_return_type_mismatch(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_RETURN_TYPE_MISMATCH"]
            expected = self.test_suite_oracles[test_file_name]["number_of_RETURN_TYPE_MISMATCH"]
            self.assertEqual(actual, expected, test_file_name)

    def test_number_of_time_type_mismatch(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_TIMES_TYPE_MISMATCH"]
            expected = self.test_suite_oracles[test_file_name]["number_of_TIMES_TYPE_MISMATCH"]
            self.assertEqual(actual, expected, test_file_name)

    def test_number_of_undeclared_class(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_UNDECLARED_CLASS"]
            expected = self.test_suite_oracles[test_file_name]["number_of_UNDECLARED_CLASS"]
            self.assertEqual(actual, expected, test_file_name)

    def test_number_of_undeclared_identifier(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_UNDECLARED_IDENTIFIER"]
            expected = self.test_suite_oracles[test_file_name]["number_of_UNDECLARED_IDENTIFIER"]
            self.assertEqual(actual, expected, test_file_name)

    def test_number_of_undeclared_method(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_UNDECLARED_METHOD"]
            expected = self.test_suite_oracles[test_file_name]["number_of_UNDECLARED_METHOD"]
            self.assertEqual(actual, expected, test_file_name)

    def test_number_of_undeclared_super_class(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_UNDECLARED_SUPER_CLASS"]
            expected = self.test_suite_oracles[test_file_name]["number_of_UNDECLARED_SUPER_CLASS"]
            self.assertEqual(actual, expected, test_file_name)

    def test_number_of_while_type_mismatch(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_WHILE_TYPE_MISMATCH"]
            expected = self.test_suite_oracles[test_file_name]["number_of_WHILE_TYPE_MISMATCH"]
            self.assertEqual(actual, expected, test_file_name)

    def test_number_of_wrong_arg_number(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_WRONG_ARG_NUMBER"]
            expected = self.test_suite_oracles[test_file_name]["number_of_WRONG_ARG_NUMBER"]
            self.assertEqual(actual, expected, test_file_name)
