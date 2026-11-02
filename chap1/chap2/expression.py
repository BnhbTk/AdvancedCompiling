from ply import lex,yacc

tokens=("NB","LP","RP","PLUS","MUL")
t_NB="[0-9]+"
t_LP=r"\("
t_RP=r"\)"
t_PLUS=r"\+"
t_MUL=r"\*"
t_ignore=" \t"

def t_error(t):
    print(f"Lexical error {t}")

lex.lex()

precedence=(
    ("left","PLUS"),
    ("left","MUL")
)

def p_e(p):
    """ e : e PLUS e
    | e MUL e
    | NB
    | LP e RP
    """
    if len(p)==2:# this is E->nb
        p[0]=int(p[1])
    elif p[1]=="(":# this is E-> (E)
        p[0]=p[2]
    elif p[2]=="+": # this is E -> E + E
        p[0]=p[1]+p[3]
    else: # this is E -> E * E
        p[0]=p[1]*p[3]

def p_error(p):
    print("Syntax error")
    
parser=yacc.yacc()
value=parser.parse("2*(3+5)*6+3")
print(value)
    
