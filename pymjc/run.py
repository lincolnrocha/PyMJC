import sys
from pymjc.front.ast import Program

from pymjc.front.lexer import MJLexer
from pymjc.front.parser import MJParser
from pymjc.front.visitor import PrettyPrintVisitor

class MJCompiler():

    def compile(self, source_file):
        source_code = source_file.read()
        lexer = MJLexer()
        lexer.src_file_name = source_file.name
        parser = MJParser()
        parser.src_file_name = source_file.name
        result:Program = parser.parse(lexer.tokenize(source_code))

        print("AST PrettyPrintVisitor")
        visitor = PrettyPrintVisitor()
        visitor.visit_program(result)
        

if __name__ == '__main__':
    args = sys.argv[1:]

    if len(args) == 1:
        with open(args[0], "r") as source_file:
            compiler = MJCompiler()
            compiler.compile(source_file)