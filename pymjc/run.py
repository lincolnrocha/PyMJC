import sys

from pymjc.back.mips import MipsFrame
from pymjc.front.ast import Program

from pymjc.front import translate
from pymjc.front.lexer import MJLexer
from pymjc.front.parser import MJParser
from pymjc.front.visitor import FillSymbolTableVisitor, PrettyPrintVisitor, TranslateVisitor, TypeCheckingVisitor

class MJCompiler():

    def compile(self, source_file):
        source_code = source_file.read()
        lexer = MJLexer()
        lexer.src_file_name = source_file.name
        parser = MJParser()
        parser.src_file_name = source_file.name
        program:Program = parser.parse(lexer.tokenize(source_code))

        symbol_table_creator = FillSymbolTableVisitor()
        symbol_table_creator.src_file_name = source_file.name
        symbol_table_creator.init_semantic_errors()
        symbol_table_creator.visit_program(program)

        type_checker = TypeCheckingVisitor()
        type_checker.src_file_name = source_file.name
        type_checker.fill_semantic_errors(symbol_table_creator.semantic_errors)
        type_checker.set_symbol_table(symbol_table_creator.get_symbol_table())
        type_checker.visit_program(program)

        translate_visitor = TranslateVisitor(symbol_table_creator.get_symbol_table(), MipsFrame())
        translate_visitor.src_file_name = source_file.name
        translate_visitor.visit_program(program)
        translate_visitor.set_symbol_table(symbol_table_creator.get_symbol_table())
        frags: translate.Frag = translate_visitor.get_result()
        


if __name__ == '__main__':
    args = sys.argv[1:]

    if len(args) == 1:
        with open(args[0], "r") as source_file:
            compiler = MJCompiler()
            compiler.compile(source_file)