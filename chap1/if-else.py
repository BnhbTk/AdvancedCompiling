from ply import lex,yacc




tokens=("IF","ELSE","INST","A1","A2","A3")

t_IF="if"
t_ELSE="else"
t_INST="inst"
t_A1="a1"
t_A2="a2"
t_A3="a3"

t_ignore=" \t"

def t_error(t):
    print(f"Lexical error {t}")

lex.lex()

def p_s(p):
    """ s : IF cdt s
    | IF cdt s ELSE s
    | INST
    """
def p_cdt(p):
    """ cdt : A1
    | A2
    | A3
    """

def p_error(p):
    print("Syntax error")
    
parser=yacc.yacc()

parser.parse("if a1 inst else")
