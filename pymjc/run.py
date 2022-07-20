import sys
from typing import List

from pymjc import util
from pymjc.back import assem, flowgraph, mips, regalloc
from pymjc.front import ast, canon, lexer, parser,translate, tree, visitor

class MJCompiler():

    def compile(self, source_file):

        #Lexical and Semantic Analysis
        source_code = source_file.read()
        mj_lexer = lexer.MJLexer()
        mj_lexer.src_file_name = source_file.name
        mj_parser = parser.MJParser()
        mj_parser.src_file_name = source_file.name
        program:ast.Program = mj_parser.parse(mj_lexer.tokenize(source_code))

        #Semantic Analysis: Symbol Table Construction 
        symbol_table_creator = visitor.FillSymbolTableVisitor()
        symbol_table_creator.src_file_name = source_file.name
        symbol_table_creator.init_semantic_errors()
        symbol_table_creator.visit_program(program)

        #Semantic Analysis: Type Checking
        type_checker = visitor.TypeCheckingVisitor()
        type_checker.src_file_name = source_file.name
        type_checker.fill_semantic_errors(symbol_table_creator.semantic_errors)
        type_checker.set_symbol_table(symbol_table_creator.get_symbol_table())
        type_checker.visit_program(program)

        #Translation to Intermidiate Representation
        translate_visitor = visitor.TranslateVisitor(symbol_table_creator.get_symbol_table(), mips.MipsFrame())
        translate_visitor.src_file_name = source_file.name
        translate_visitor.visit_program(program)
        translate_visitor.set_symbol_table(symbol_table_creator.get_symbol_table())
        program_frags: translate.Frag = translate_visitor.get_result()

        #Instrucion Selection - MIPS
        stm_list: tree.StmList
        frags_assem_instr = List[List[assem.Instr]]
        frag: translate.Frag = program_frags
        while(frag is not None):
            if(isinstance(frag, translate.ProcFrag)):
                stm_list = canon.Canon.linearize(frag.body)
                basic_blocks: canon.BasicBlocks = canon.BasicBlocks(stm_list)
                schedule: canon.TraceSchedule  = canon.TraceSchedule(basic_blocks)
                assem_instr = List[assem.Instr]

                instr_list: List[assem.Instr] = frag.frame.codegen(util.Converter.to_ListStm(schedule.stms))
                for instr in instr_list:
                  assem_instr.append(instr)

                frag.frame.proc_entry_exit2(assem_instr)
                frag.frame.proc_entry_exit3(assem_instr)
                frags_assem_instr.append(assem_instr)     

            frag = frag.get_next()

        #Flow Graph Building
        flow_graph: flowgraph.AssemFlowGraph = None
        for assem_instr in frags_assem_instr:
            flow_graph = flowgraph.AssemFlowGraph(util.Converter.to_InstrList(assem_instr))
            flow_graph.show()



if __name__ == '__main__':
    args = sys.argv[1:]

    if len(args) == 1:
        with open(args[0], "r") as source_file:
            compiler = MJCompiler()
            compiler.compile(source_file)