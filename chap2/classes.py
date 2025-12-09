from __future__ import annotations
from ply import lex, yacc

class AST:
    def __init__(self):
        self.classes = []

    def add_class(self,kl:Klass):
        #Here we check for double definition
        if kl in self.classes:
            raise Exception(f"Class {kl.name} already defined")
        self.classes.append(kl)
    
    def search_name(self,name:str)->Klass:
        #This method is a utility function to search a class by name
        for kl in self.classes:
            if kl.name==name:
                return kl
        return None
    
    def __str__(self):
        return "\n".join([str(kl) for kl in self.classes])
    
    

class Klass:
    def __init__(self,name:str):
        self.name = name
        self.inherits = []
        
    def add_inherit(self,super:str):
        #Check for double declaration of super classes
        if super in self.inherits:
            raise Exception(f"Class {self.name} already inherits from {super}")
        else:
            self.inherits.append(super)
            

    def __eq__(self, value):
        return self.name==value.name
    
    def __str__(self):
        return f"class {self.name}"+(" ("+",".join(self.inherits)+")" if self.inherits else "")

tokens = ("LP","RP","COMMA","CLASS","ID")

t_LP=r"\("
t_RP=r"\)"
t_COMMA=","

def t_ID(t):
    r"[a-zA-Z_][a-zA-Z0-9_]*"
    if t.value == "class":
        t.type = "CLASS"
    return t

t_ignore=" \t\n"

def t_error(t):
    raise Exception(f"Lexical error at {t}")

lex.lex()

ast=AST()

def p_CD(p):
    """CD : CD C1
    | C1
    """
    if len(p)==2:
        p[0]=AST()
        p[0].add_class(p[1])
    else:
        p[0]=p[1]
        p[0].add_class(p[2])

def p_C1(p):
    """C1 : CLASS ID PARAM
    """
    p[0]=Klass(p[2])
    for super in p[3]:
        p[0].add_inherit(super)

def p_PARAM(p):
    """PARAM : LP INHER RP
    |
    """
    if len(p)==1:
        p[0]=[]
    else:
        p[0]=p[2]

def p_INHER(p):
    """INHER : INHER COMMA ID
    | ID
    """
    if len(p)==2:
        p[0]=[p[1]]
    else:
        p[0]=p[1]+[p[3]]    

def p_error(p):
    if p:
        raise Exception(f"Syntax error at {p.value}, unexpected {p.type}")
    else:
        raise Exception("Syntax error, unexpected EOF")

parser=yacc.yacc()
with open("sample.oop") as f:
    data = f.read()
    try:
        ast:AST=parser.parse(data)
        print("No problem found, this is the AST:")
        print(ast)
    except Exception as e:
        print(e)
