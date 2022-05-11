import json
import os
import unittest

from pymjc.front.lexer import MJLexer
from pymjc.front.parser import MJParser

from tests import util


class ParserTest(unittest.TestCase):
    
    actual_values = {}
    
    test_suite_oracles = {}

    @classmethod
    def setUpClass(cls):
        test_suite_oracles_path = os.path.dirname(os.path.realpath(__file__)) + str(os.path.sep) + "testoracle" + str(os.path.sep) + "parser_test_suite_oracles.json"
        with open(test_suite_oracles_path) as test_suite_oracles_file:
            cls.test_suite_oracles = json.load(test_suite_oracles_file)
            test_suite_oracles_file.close()

        test_data_path = os.path.dirname(os.path.realpath(__file__)) + str(os.path.sep) + "testdata" + str(os.path.sep)
        test_correct_files_path = os.path.join(test_data_path, "correct")
        file_name_list = os.listdir(test_correct_files_path)
        
        test_data_file_path_map = {}

        for file_name in file_name_list:
            test_data_file_path_map[file_name] = os.path.join(test_correct_files_path, file_name)

        test_faulty_files_path = os.path.join(test_data_path, "faulty" + str(os.path.sep) + "syntax")
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
                parser.parse(lexer.tokenize(content))
                source_test_file.close()
                debug_file = open(parser.debugfile, "r" )
                number_of_shift_reduce, number_of_reduce_reduce = util.process_debug_file(debug_file.read())
                debug_file.close()
                cls.actual_values[file_name] = util.compute_parser_oracles(number_of_shift_reduce, number_of_reduce_reduce, parser.syntax_error)                


    def test_number_of_shift_reduce_conflicts(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_shift_reduce"]
            expected = self.test_suite_oracles[test_file_name]["number_of_shift_reduce"]
            self.assertEqual(actual, expected, test_file_name)

    def test_number_of_reduce_reduce_conflicts(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_reduce_reduce"]
            expected = self.test_suite_oracles[test_file_name]["number_of_reduce_reduce"]
            self.assertEqual(actual, expected, test_file_name)

    def test_syntax_error(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["has_parser_error"]
            expected = self.test_suite_oracles[test_file_name]["has_parser_error"]
            self.assertEqual(actual, expected, test_file_name)
