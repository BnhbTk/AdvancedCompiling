from ply import lex,yacc





class Node:
    def value_of(self):
        raise NotImplementedError()

class Nb(Node):
    def __init__(self,val:int):
        self.val=val
    
    def __str__(self):
        return f"{self.val}"
    
    def value_of(self):
        return self.val

class Plus(Node):
    def __init__(self,c1:Node,c2:Node):
        self.c1=c1
        self.c2=c2
    
    def __str__(self):
        return f"+({self.c1},{self.c2})"
    
    def value_of(self):
        return self.c1.value_of()+self.c2.value_of()

class Mul(Node):
    def __init__(self,c1:Node,c2:Node):
        self.c1=c1
        self.c2=c2
    
    def __str__(self):
        return f"*({self.c1},{self.c2})"
    
    def value_of(self):
        return self.c1.value_of()*self.c2.value_of()

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
        p[0]=Nb(int(p[1]))
    elif p[1]=="(":# this is E-> (E)
        p[0]=p[2]
    elif p[2]=="+": # this is E -> E + E
        p[0]=Plus(p[1],p[3])
    else: # this is E -> E * E
        p[0]=Mul(p[1],p[3])

def p_error(p):
    print("Syntax error")
    
parser=yacc.yacc()
ast=parser.parse("2*(3+5)*6+3")
print(ast.value_of())
    
