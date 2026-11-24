from ply import lex,yacc

# The scanner: notice how the keyword is processed
tokens=("CLASS","ID","LP","RP","COMMA")

t_LP=r"\("
t_RP=r"\)"
t_COMMA=","

def t_ID(t):
    "[a-zA-Z][a-zA-Z0-9]*"
    if t.value=="class":
        t.type="CLASS"
    return t

t_ignore=" \t\n\r"

def t_error(t):
    raise ValueError(f"Illegal token {t}")

lexer=lex.lex()

# The parser is yet to be written
