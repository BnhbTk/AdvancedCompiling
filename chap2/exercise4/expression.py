from ply import lex,yacc

##### The scanner
tokens=("VAR","CST","PLUS","MUL","SUB","DIV","LP","RP")
t_VAR="[a-zA-Z][a-zA-Z0-9]*"
t_CST="[0-9]+"
t_PLUS=r"\+"
t_MUL=r"\*"
t_SUB="-"
t_DIV="/"
t_LP=r"\("
t_RP=r"\)"
t_ignore=" "

def t_error(t):
    raise ValueError(f"Illegal token {t}")

lex.lex()

##### The parser
precedence=(
    ("left","PLUS","SUB"),
    ("left","MUL","DIV"),
    ("nonassoc","UMINUS")
)
def p_e_1(p):
    "e : e PLUS e"

def p_e_2(p):
    "e : e MUL e"

def p_e_3(p):
    "e : e SUB e"
    
def p_e_4(p):
    "e : e DIV e"

def p_e_5(p):
    "e : LP e RP"

def p_e_6(p):
    "e : SUB e %prec UMINUS"

def p_e_7(p):
    "e : CST"

def p_e_8(p):
    "e : VAR"

def p_error(p):
    raise ValueError("Syntax error")

parser=yacc.yacc()

parser.parse("((2 * x - 3 * y) * (x + y + 6)) / (((x - 1) * (y + 2)) - (x / (y - 4)))")
