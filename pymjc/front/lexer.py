from sly import Lexer
from pymjc.log import MJLogger

class MJLexer(Lexer):

    def __init__(self):
        super().__init__
        self.bad_tokens = []
        self.src_file_name = "UnknownSRCFile"
        MJLogger.configure()

    tokens = {ID, PRINT, BOOLEAN, EXTENDS, STRING, PUBLIC, LENGTH, STATIC, RETURN, WHILE, CLASS, 
              FALSE, ELSE, TRUE, VOID, MAIN, THIS, INT, NEW, IF, NUM, AND, NOT, EQUALS, LESS, PLUS,
              MINUS, TIMES, DOT, SEMICOLON, COMMA, LEFTBRACE, RIGHTBRACE, LEFTPARENT, RIGHTPARENT,
              LEFTSQRBRACKET, RIGHTSQRBRACKET}

    ignore = ' \t\r\f'
    
    PRINT = r'System\.out\.println'
    
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ID['boolean'] = BOOLEAN
    ID['extends'] = EXTENDS
    ID['String'] = STRING
    ID['public'] = PUBLIC 
    ID['length'] = LENGTH
    ID['static'] = STATIC
    ID['return'] = RETURN
    ID['while'] = WHILE
    ID['class'] = CLASS
    ID['false'] = FALSE
    ID['else'] = ELSE
    ID['true'] = TRUE
    ID['void'] = VOID 
    ID['main'] = MAIN
    ID['this'] = THIS
    ID['int'] = INT
    ID['new'] = NEW
    ID['if'] = IF
    
    NUM = r'\d+'
    AND = r'\&\&'
    NOT = r'\!'
    EQUALS = r'\='
    LESS = r'\<'
    PLUS = r'\+'
    MINUS = r'\-'
    TIMES = r'\*' 
    DOT = r'\.'
    SEMICOLON = r'\;'
    COMMA = r'\,'
    LEFTBRACE  = r'\{'
    RIGHTBRACE = r'\}'
    LEFTPARENT = r'\('
    RIGHTPARENT = r'\)' 
    LEFTSQRBRACKET = r'\['
    RIGHTSQRBRACKET = r'\]'

    ignore_comment = r'(\/\/.*)|(\/\*\.?\*\/)'

    @_(r'\n+')
    def ignore_newline(self, token):
        self.lineno += token.value.count('\n')

    def error(self, token):
        MJLogger.lexer_log(self.src_file_name, self.lineno, token.value[0])
        self.index += 1
        self.bad_tokens.append(token)