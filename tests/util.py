import re

def count_tokens(token_type, token_list):
    return len([token for token in token_list if  token.type == token_type])

def count_bad_tokens(token_value, token_list):
    return len([token for token in token_list if  token.value[0] == token_value])

def compute_lexer_oracles(token_list, bad_token_list):
    token_oracle = {"number_of_tokens":len(token_list),
                    "number_of_ID":count_tokens("ID", token_list), 
                    "number_of_PRINT":count_tokens("PRINT", token_list), 
                    "number_of_BOOLEAN":count_tokens("BOOLEAN", token_list), 
                    "number_of_EXTENDS":count_tokens("EXTENDS", token_list),
                    "number_of_STRING":count_tokens("STRING", token_list), 
                    "number_of_PUBLIC":count_tokens("PUBLIC", token_list), 
                    "number_of_LENGTH":count_tokens("LENGTH", token_list), 
                    "number_of_STATIC":count_tokens("STATIC", token_list), 
                    "number_of_RETURN":count_tokens("RETURN", token_list), 
                    "number_of_WHILE":count_tokens("WHILE", token_list), 
                    "number_of_CLASS":count_tokens("CLASS", token_list), 
                    "number_of_FALSE":count_tokens("FALSE", token_list), 
                    "number_of_ELSE":count_tokens("ELSE", token_list), 
                    "number_of_TRUE":count_tokens("TRUE", token_list), 
                    "number_of_VOID":count_tokens("VOID", token_list), 
                    "number_of_MAIN":count_tokens("MAIN", token_list), 
                    "number_of_THIS":count_tokens("THIS", token_list), 
                    "number_of_INT":count_tokens("INT", token_list), 
                    "number_of_NEW":count_tokens("NEW", token_list), 
                    "number_of_IF":count_tokens("IF", token_list), 
                    "number_of_NUM":count_tokens("NUM", token_list), 
                    "number_of_AND":count_tokens("AND", token_list), 
                    "number_of_NOT":count_tokens("NOT", token_list), 
                    "number_of_ASSIGNMENT":count_tokens("ASSIGNMENT", token_list), 
                    "number_of_LESS":count_tokens("LESS", token_list), 
                    "number_of_PLUS":count_tokens("PLUS", token_list),
                    "number_of_MINUS":count_tokens("MINUS", token_list), 
                    "number_of_TIMES":count_tokens("TIMES", token_list), 
                    "number_of_DOT":count_tokens("DOT", token_list), 
                    "number_of_SEMICOLON":count_tokens("SEMICOLON", token_list), 
                    "number_of_COMMA":count_tokens("COMMA", token_list), 
                    "number_of_LEFTBRACE":count_tokens("LEFTBRACE", token_list), 
                    "number_of_RIGHTBRACE":count_tokens("RIGHTBRACE", token_list), 
                    "number_of_LEFTPARENT":count_tokens("LEFTPARENT", token_list), 
                    "number_of_RIGHTPARENT":count_tokens("RIGHTPARENT", token_list),
                    "number_of_LEFTSQRBRACKET":count_tokens("LEFTSQRBRACKET", token_list), 
                    "number_of_RIGHTSQRBRACKET":count_tokens("RIGHTSQRBRACKET", token_list),
                    "number_of_bad_tokens":len(bad_token_list),                    
                    "number_of_AT":count_bad_tokens("@", bad_token_list),
                    "number_of_HASH":count_bad_tokens("#", bad_token_list),
                    "number_of_AMPERSAND":count_bad_tokens("&", bad_token_list),
                    "number_of_PIPE":count_bad_tokens("|", bad_token_list)}
    
    return token_oracle

def compute_parser_oracles(number_of_shift_reduce_conflicts = 0, number_of_reduce_reduce_conflicts = 0, parser_error=False):
    parser_oracle = {"number_of_shift_reduce":number_of_shift_reduce_conflicts,
                     "number_of_reduce_reduce":number_of_reduce_reduce_conflicts, 
                     "has_parser_error":parser_error}
    
    return parser_oracle

def process_debug_file(debug_file):
    shift_reduce_conflicts = len(re.findall(r'! shift\/reduce conflict', debug_file))
    reduce_reduce_conflicts = len(re.findall(r'! reduce\/reduce conflict', debug_file))
    return shift_reduce_conflicts, reduce_reduce_conflicts

def compute_semantic_oracles(semantic_errors):
    semantic_oracle = {"number_of_ALREADY_DECLARED_CLASS": semantic_errors["ALREADY_DECLARED_CLASS"],
                       "number_of_ALREADY_DECLARED_METHOD": semantic_errors["ALREADY_DECLARED_METHOD"],
                       "number_of_ALREADY_DECLARED_FIELD": semantic_errors["ALREADY_DECLARED_FIELD"],
                       "number_of_ALREADY_DECLARED_VAR": semantic_errors["ALREADY_DECLARED_VAR"],
                       "number_of_AND_TYPE_MISMATCH": semantic_errors["AND_TYPE_MISMATCH"],
                       "number_of_ARG_TYPE_MISMATCH": semantic_errors["ARG_TYPE_MISMATCH"],
                       "number_of_ARRAY_ASSIGN_TYPE_MISMATCH": semantic_errors["ARRAY_ASSIGN_TYPE_MISMATCH"],
                       "number_of_ARRAY_LENGTH_TYPE_MISMATCH": semantic_errors["ARRAY_LENGTH_TYPE_MISMATCH"],
                       "number_of_ARRAY_TYPE_MISMATCH": semantic_errors["ARRAY_TYPE_MISMATCH"],
                       "number_of_ASSIGN_TYPE_MISMATCH": semantic_errors["ASSIGN_TYPE_MISMATCH"],
                       "number_of_DUPLICATED_ARG": semantic_errors["DUPLICATED_ARG"],
                       "number_of_IF_TYPE_MISMATCH": semantic_errors["IF_TYPE_MISMATCH"],
                       "number_of_INDEX_TYPE_MISMATCH": semantic_errors["INDEX_TYPE_MISMATCH"],
                       "number_of_INVALID_OBJECT_IDENTIFIER": semantic_errors["INVALID_OBJECT_IDENTIFIER"],
                       "number_of_LESS_THAN_TYPE_MISMATCH": semantic_errors["LESS_THAN_TYPE_MISMATCH"],
                       "number_of_MINUS_TYPE_MISMATCH": semantic_errors["MINUS_TYPE_MISMATCH"],
                       "number_of_NEW_ARRAY_TYPE_MISMATCH": semantic_errors["NEW_ARRAY_TYPE_MISMATCH"],
                       "number_of_NEW_OBJECT_UNDECLARED_CLASS": semantic_errors["NEW_OBJECT_UNDECLARED_CLASS"],
                       "number_of_NOT_TYPE_MISMATCH": semantic_errors["NOT_TYPE_MISMATCH"],
                       "number_of_PLUS_TYPE_MISMATCH": semantic_errors["PLUS_TYPE_MISMATCH"],
                       "number_of_RETURN_TYPE_MISMATCH": semantic_errors["RETURN_TYPE_MISMATCH"],
                       "number_of_TIMES_TYPE_MISMATCH": semantic_errors["TIMES_TYPE_MISMATCH"],
                       "number_of_UNDECLARED_CLASS": semantic_errors["UNDECLARED_CLASS"],
                       "number_of_UNDECLARED_IDENTIFIER": semantic_errors["UNDECLARED_IDENTIFIER"],
                       "number_of_UNDECLARED_METHOD": semantic_errors["UNDECLARED_METHOD"],
                       "number_of_UNDECLARED_SUPER_CLASS": semantic_errors["UNDECLARED_SUPER_CLASS"], 
                       "number_of_WHILE_TYPE_MISMATCH": semantic_errors["WHILE_TYPE_MISMATCH"],
                       "number_of_WRONG_ARG_NUMBER": semantic_errors["WRONG_ARG_NUMBER"]}
    
    return semantic_oracle