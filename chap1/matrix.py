from ply import lex

tokens=("LB","RB","CST","COMMA")

t_LB=r"\["
t_RB=r"\]"
t_CST="[0-9]+"
t_COMMA=","
t_ignore=" \t"

def t_error(t):
    raise Exception(t)

lexer=lex.lex()

lex.input("[1 2 3,2 4 5 125,,]")

while token:=lexer.token():
    print(token)
