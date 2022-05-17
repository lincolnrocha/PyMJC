from pymjc.front.ast import *
from pymjc.front.lexer import MJLexer
from sly import Parser

from pymjc.log import MJLogger

class MJParser(Parser):

    def __init__(self):
        self.syntax_error = False
        self.src_file_name = "UnknownSRCFile"
        super().__init__
        
    precedence = (('nonassoc', LESS, AND),
                  ('left', PLUS, MINUS),        
                  ('left', TIMES),
                  ('right', NOT),
                  ('right', DOT)
                 )
                 
    tokens = MJLexer.tokens

    syntax_error = False

    debugfile = 'parser.out'


    ###################################
	#Program and Class Declarations   #
    ###################################    
    @_('MainClass ClassDeclarationStar')
    def Goal(self, p):
        return p
    
    @_('CLASS Identifier LEFTBRACE PUBLIC STATIC VOID MAIN LEFTPARENT STRING LEFTSQRBRACKET RIGHTSQRBRACKET Identifier RIGHTPARENT LEFTBRACE Statement RIGHTBRACE RIGHTBRACE')
    def MainClass(self, p):
        return p

    @_('Empty')
    def ClassDeclarationStar(self, p):
        return p

    @_('ClassDeclaration ClassDeclarationStar')
    def ClassDeclarationStar(self, p):
        return p

    @_('CLASS Identifier SuperOpt LEFTBRACE VarDeclarationStar MethodDeclarationStar RIGHTBRACE')
    def ClassDeclaration(self, p):
        return p


    @_('Empty')
    def SuperOpt(self, p):
        return p
    
    @_('EXTENDS Identifier')
    def SuperOpt(self, p):
        return p

    @_('Empty')
    def VarDeclarationStar(self, p):
        return p

    @_('VarDeclarationStar VarDeclaration')
    def VarDeclarationStar(self, p):
        return p

    @_('Type Identifier SEMICOLON')
    def VarDeclaration(self, p):
        return p

    @_('Empty')
    def MethodDeclarationStar(self, p):
        return p

    @_('MethodDeclarationStar MethodDeclaration')
    def MethodDeclarationStar(self, p):
        return p

    @_('PUBLIC Type Identifier LEFTPARENT FormalParamListOpt RIGHTPARENT LEFTBRACE VarDeclarationStar StatementStar RETURN Expression SEMICOLON RIGHTBRACE')
    def MethodDeclaration(self, p):
        return p

    @_('Empty')
    def FormalParamListOpt(self, p):
        return p
        
    @_('FormalParamStar')
    def FormalParamListOpt(self, p):            
        return p

    @_('FormalParam')
    def FormalParamStar(self, p):
        return p

    @_('FormalParamStar COMMA FormalParam')
    def FormalParamStar(self, p):
        return p

    @_('Type Identifier')
    def FormalParam(self, p):
        return p
        
    ###################################
    #Type Declarations                #
    ###################################

    @_('INT')
    def Type(self, p):
        return p

    @_('INT LEFTSQRBRACKET RIGHTSQRBRACKET')
    def Type(self, p):
        return p

    @_('BOOLEAN')
    def Type(self, p):
        return p

    @_('Identifier')
    def Type(self, p):
        return p

    ###################################
    #Statements Declarations          #
    ###################################

    @_('Empty')
    def StatementStar(self, p):
        return p

    @_('Statement StatementStar')
    def StatementStar(self, p):
        return p

    @_('LEFTBRACE StatementStar RIGHTBRACE')
    def Statement(self, p):
        return p

    @_('IF LEFTPARENT Expression RIGHTPARENT Statement ELSE Statement')
    def Statement(self, p):
        return p

    @_('WHILE LEFTPARENT Expression RIGHTPARENT Statement')
    def Statement(self, p):
        return p

    @_('PRINT LEFTPARENT Expression RIGHTPARENT SEMICOLON')
    def Statement(self, p):
        return p

    @_('Identifier EQUALS Expression SEMICOLON')
    def Statement(self, p):
        return p

    @_('Identifier LEFTSQRBRACKET Expression RIGHTSQRBRACKET EQUALS Expression SEMICOLON')
    def Statement(self, p):
        return p

    ###################################
    #Expression Declarations          #
    ###################################

    @_('Expression AND Expression')
    def Expression(self, p):
        return p

    @_('Expression LESS Expression')
    def Expression(self, p):
        return p

    @_('Expression PLUS Expression')
    def Expression(self, p):
        return p

    @_('Expression MINUS Expression')
    def Expression(self, p):
        return p

    @_('Expression TIMES Expression')
    def Expression(self, p):
        return p

    @_('Expression LEFTSQRBRACKET Expression RIGHTSQRBRACKET')
    def Expression(self, p):
        return p

    @_('Expression DOT LENGTH')
    def Expression(self, p):
        return p

    @_('Expression DOT Identifier LEFTPARENT ExpressionListOpt RIGHTPARENT')
    def Expression(self, p):
        return p

    @_('Empty')
    def ExpressionListOpt(self, p):
        return p

    @_('ExpressionListStar')
    def ExpressionListOpt(self, p):
        return p

    @_('Expression')
    def ExpressionListStar(self, p):
        return p

    @_('ExpressionListStar COMMA Expression')
    def ExpressionListStar(self, p):
        return p

    @_('THIS')
    def Expression(self, p):
        return p

    @_('NEW INT LEFTSQRBRACKET Expression RIGHTSQRBRACKET')
    def Expression(self, p):
        return p

    @_('NEW Identifier LEFTPARENT RIGHTPARENT')
    def Expression(self, p):
        return p

    @_('NOT Expression')
    def Expression(self, p):
        return p

    @_('LEFTPARENT Expression RIGHTPARENT')
    def Expression(self, p):
        return p

    @_('Identifier')
    def Expression(self, p):
        return p

    @_('Literal')
    def Expression(self, p):
        return p

    ###################################
    #Basic Declarations               #
    ###################################
    @_('ID')
    def Identifier(self, p):
        return p

    @_('')
    def Empty(self, p):
        return p


    ##################################
    #Literals Declarations           #
    ##################################
    @_('BooleanLiteral')
    def Literal(self, p):
        return p

    @_('IntLiteral')
    def Literal(self, p):
        return p

    @_('TRUE')
    def BooleanLiteral(self, p):
        return p

    @_('FALSE')
    def BooleanLiteral(self, p):
        return p

    @_('NUM')
    def IntLiteral(self, p):
        return p

    def error(self, p):
        MJLogger.parser_log(self.src_file_name, p.lineno, p.value[0])
        self.syntax_error = True