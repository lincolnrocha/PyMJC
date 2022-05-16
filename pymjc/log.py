import logging

from pymjc.front.visitor import SemanticErrorType


class MJLogger():

    def configure():
        logging.basicConfig(filename='pymjc.log', encoding='utf-8',
                            format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.DEBUG)

    def lexer_log(src_file_name: str, line_number: int, token_value: str):
        logging.error(
            f'LEXER - {src_file_name}, Line {line_number}: Bad character {token_value}')

    def parser_log(src_file_name: str, line_number: int, token_value: str):
        logging.error(
            f'PARSER - {src_file_name}, Line {line_number}: Syntax error near character {token_value}')

    def semantic_log(src_file_name: str, token_value: str, error_type: SemanticErrorType, error_msg: str):
        logging.error(
            f'SEMANTIC - {src_file_name}: [{error_type.name}] Semantic error near character {token_value} - {error_msg}')
