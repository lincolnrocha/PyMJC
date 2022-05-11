import json
import os
import unittest

from tests import util
from pymjc.front.lexer import MJLexer

class LexerTest(unittest.TestCase):
    
    actual_values = {}
    
    test_suite_oracles = {}

    @classmethod
    def setUpClass(cls):
        test_suite_oracles_path = os.path.dirname(os.path.realpath(__file__)) + str(os.path.sep) + "testoracle" + str(os.path.sep) + "lexer_test_suite_oracles.json"
        with open(test_suite_oracles_path) as test_suite_oracles_file:
            cls.test_suite_oracles = json.load(test_suite_oracles_file)
            test_suite_oracles_file.close()

        test_data_path = os.path.dirname(os.path.realpath(__file__)) + str(os.path.sep) + "testdata" + str(os.path.sep)
        test_correct_files_path = os.path.join(test_data_path, "correct")
        file_name_list = os.listdir(test_correct_files_path)
        
        test_data_file_path_map = {}

        for file_name in file_name_list:
            test_data_file_path_map[file_name] = os.path.join(test_correct_files_path, file_name)

        test_faulty_files_path = os.path.join(test_data_path, "faulty" + str(os.path.sep) + "tokens")
        file_name_list = os.listdir(test_faulty_files_path)

        for file_name in file_name_list:
            test_data_file_path_map[file_name] = os.path.join(test_faulty_files_path, file_name)

        for file_name in cls.test_suite_oracles:
            with open(test_data_file_path_map[file_name], "r") as source_test_file:
                content = source_test_file.read()
                lexer = MJLexer()
                lexer.src_file_name = file_name
                token_list = list(lexer.tokenize(content))
                source_test_file.close()
                cls.actual_values[file_name] = util.compute_lexer_oracles(token_list, lexer.bad_tokens)
                lexer.bad_tokens.clear()


    def test_number_of_tokens(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_tokens"]
            expected = self.test_suite_oracles[test_file_name]["number_of_tokens"]
            self.assertEqual(actual, expected, test_file_name)

    def test_number_of_id(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_ID"]
            expected = self.test_suite_oracles[test_file_name]["number_of_ID"]
            self.assertEqual(actual, expected, test_file_name)

    def test_number_of_print(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_PRINT"]
            expected = self.test_suite_oracles[test_file_name]["number_of_PRINT"]
            self.assertEqual(actual, expected, test_file_name)

    def test_number_of_boolean(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_BOOLEAN"]
            expected = self.test_suite_oracles[test_file_name]["number_of_BOOLEAN"]
            self.assertEqual(actual, expected, test_file_name)

    def test_number_of_extends(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_EXTENDS"]
            expected = self.test_suite_oracles[test_file_name]["number_of_EXTENDS"]
            self.assertEqual(actual, expected, test_file_name)

    def test_number_of_string(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_STRING"]
            expected = self.test_suite_oracles[test_file_name]["number_of_STRING"]
            self.assertEqual(actual, expected, test_file_name)

    def test_number_of_public(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_PUBLIC"]
            expected = self.test_suite_oracles[test_file_name]["number_of_PUBLIC"]
            self.assertEqual(actual, expected, test_file_name)

    def test_number_of_length(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_LENGTH"]
            expected = self.test_suite_oracles[test_file_name]["number_of_LENGTH"]
            self.assertEqual(actual, expected, test_file_name)

    def test_number_of_static(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_STATIC"]
            expected = self.test_suite_oracles[test_file_name]["number_of_STATIC"]
            self.assertEqual(actual, expected, test_file_name)
    
    def test_number_of_return(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_RETURN"]
            expected = self.test_suite_oracles[test_file_name]["number_of_RETURN"]
            self.assertEqual(actual, expected, test_file_name)

    def test_number_of_while(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_WHILE"]
            expected = self.test_suite_oracles[test_file_name]["number_of_WHILE"]
            self.assertEqual(actual, expected, test_file_name)

    def test_number_of_class(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_CLASS"]
            expected = self.test_suite_oracles[test_file_name]["number_of_CLASS"]
            self.assertEqual(actual, expected, test_file_name)

    def test_number_of_false(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_FALSE"]
            expected = self.test_suite_oracles[test_file_name]["number_of_FALSE"]
            self.assertEqual(actual, expected, test_file_name)

    def test_number_of_else(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_ELSE"]
            expected = self.test_suite_oracles[test_file_name]["number_of_ELSE"]
            self.assertEqual(actual, expected, test_file_name)

    def test_number_of_true(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_TRUE"]
            expected = self.test_suite_oracles[test_file_name]["number_of_TRUE"]
            self.assertEqual(actual, expected, test_file_name)

    def test_number_of_void(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_VOID"]
            expected = self.test_suite_oracles[test_file_name]["number_of_VOID"]
            self.assertEqual(actual, expected, test_file_name)

    def test_number_of_main(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_MAIN"]
            expected = self.test_suite_oracles[test_file_name]["number_of_MAIN"]
            self.assertEqual(actual, expected, test_file_name)

    def test_number_of_this(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_THIS"]
            expected = self.test_suite_oracles[test_file_name]["number_of_THIS"]
            self.assertEqual(actual, expected, test_file_name)

    def test_number_of_int(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_INT"]
            expected = self.test_suite_oracles[test_file_name]["number_of_INT"]
            self.assertEqual(actual, expected, test_file_name)

    def test_number_of_new(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_NEW"]
            expected = self.test_suite_oracles[test_file_name]["number_of_NEW"]
            self.assertEqual(actual, expected, test_file_name)

    def test_number_of_if(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_IF"]
            expected = self.test_suite_oracles[test_file_name]["number_of_IF"]
            self.assertEqual(actual, expected, test_file_name)

    def test_number_of_num(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_NUM"]
            expected = self.test_suite_oracles[test_file_name]["number_of_NUM"]
            self.assertEqual(actual, expected, test_file_name)

    def test_number_of_and(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_AND"]
            expected = self.test_suite_oracles[test_file_name]["number_of_AND"]
            self.assertEqual(actual, expected, test_file_name)

    def test_number_of_not(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_NOT"]
            expected = self.test_suite_oracles[test_file_name]["number_of_NOT"]
            self.assertEqual(actual, expected, test_file_name)

    def test_number_of_assignment(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_ASSIGNMENT"]
            expected = self.test_suite_oracles[test_file_name]["number_of_ASSIGNMENT"]
            self.assertEqual(actual, expected, test_file_name)

    def test_number_of_less(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_LESS"]
            expected = self.test_suite_oracles[test_file_name]["number_of_LESS"]
            self.assertEqual(actual, expected, test_file_name)

    def test_number_of_plus(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_PLUS"]
            expected = self.test_suite_oracles[test_file_name]["number_of_PLUS"]
            self.assertEqual(actual, expected, test_file_name)

    def test_number_of_minus(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_MINUS"]
            expected = self.test_suite_oracles[test_file_name]["number_of_MINUS"]
            self.assertEqual(actual, expected, test_file_name)

    def test_number_of_times(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_TIMES"]
            expected = self.test_suite_oracles[test_file_name]["number_of_TIMES"]
            self.assertEqual(actual, expected, test_file_name)

    def test_number_of_dot(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_DOT"]
            expected = self.test_suite_oracles[test_file_name]["number_of_DOT"]
            self.assertEqual(actual, expected, test_file_name)

    def test_number_of_semicolon(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_SEMICOLON"]
            expected = self.test_suite_oracles[test_file_name]["number_of_SEMICOLON"]
            self.assertEqual(actual, expected, test_file_name)

    def test_number_of_comma(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_COMMA"]
            expected = self.test_suite_oracles[test_file_name]["number_of_COMMA"]
            self.assertEqual(actual, expected, test_file_name)

    def test_number_of_leftbrace(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_LEFTBRACE"]
            expected = self.test_suite_oracles[test_file_name]["number_of_LEFTBRACE"]
            self.assertEqual(actual, expected, test_file_name)

    def test_number_of_rightbrace(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_RIGHTBRACE"]
            expected = self.test_suite_oracles[test_file_name]["number_of_RIGHTBRACE"]
            self.assertEqual(actual, expected, test_file_name)

    def test_number_of_leftparent(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_LEFTPARENT"]
            expected = self.test_suite_oracles[test_file_name]["number_of_LEFTPARENT"]
            self.assertEqual(actual, expected, test_file_name)

    def test_number_of_rightparent(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_RIGHTPARENT"]
            expected = self.test_suite_oracles[test_file_name]["number_of_RIGHTPARENT"]
            self.assertEqual(actual, expected, test_file_name)

    def test_number_of_leftsqrbracket(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_LEFTSQRBRACKET"]
            expected = self.test_suite_oracles[test_file_name]["number_of_LEFTSQRBRACKET"]
            self.assertEqual(actual, expected, test_file_name)

    def test_number_of_rightsqrbracket(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_RIGHTSQRBRACKET"]
            expected = self.test_suite_oracles[test_file_name]["number_of_RIGHTSQRBRACKET"]
            self.assertEqual(actual, expected, test_file_name)


    def test_number_of_bad_tokens(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_bad_tokens"]
            expected = self.test_suite_oracles[test_file_name]["number_of_bad_tokens"]
            self.assertEqual(actual, expected, test_file_name)


    def test_number_of_at(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_AT"]
            expected = self.test_suite_oracles[test_file_name]["number_of_AT"]
            self.assertEqual(actual, expected, test_file_name)

    def test_number_of_hash(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_HASH"]
            expected = self.test_suite_oracles[test_file_name]["number_of_HASH"]
            self.assertEqual(actual, expected, test_file_name)

    def test_number_of_ampersand(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_AMPERSAND"]
            expected = self.test_suite_oracles[test_file_name]["number_of_AMPERSAND"]
            self.assertEqual(actual, expected, test_file_name)

    def test_number_of_pipe(self):
        for test_file_name in self.test_suite_oracles:
            actual = self.actual_values[test_file_name]["number_of_PIPE"]
            expected = self.test_suite_oracles[test_file_name]["number_of_PIPE"]
            self.assertEqual(actual, expected, test_file_name)