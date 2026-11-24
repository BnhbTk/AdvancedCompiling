import ply.lex as lex
import ply.yacc as yacc

# The scanner
tokens=("OP","CP","C")
t_OP=r"\("
t_CP=r"\)"
t_C="[^()]"

def t_error(t):
    print(f"Lexical error {t}")

lexer=lex.lex()

# The scanner: notice the semantic actions that computes the maximum depth
def p_s(p):
    """s : s t
    | t
    """
    if len(p) == 2:
        p[0]=p[1]
    else:
        p[0]=max(p[1],p[2])

def p_t(p):
    """t : OP s CP
    | C
    """
    if len(p)==2:
        p[0]=0
    else:
        p[0]=p[2]+1

def p_error(p):
    print("Syntax error")

parser=yacc.yacc()

pf=parser.parse("a(b)((c))")
print(f"Max depth={pf}")
