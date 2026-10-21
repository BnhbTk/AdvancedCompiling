from ply import lex,yacc


tokens=("LP","RP","CHAR")
t_LP=r"\("
t_RP=r"\)"


t_CHAR=r"[^\(\)]"

def t_error(t):
    print(f"Lexical error {t}")

lex.lex()

def p_s(p):
    """s : s t 
    | t
    """
    pass

def p_t(p):
    """t : LP s RP 
    | CHAR
    """
    pass

def p_error(p):
    print("Syntax error")

parser=yacc.yacc()
parser.parse("(abc)((a)b)")
    
