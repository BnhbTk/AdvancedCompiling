from ply import lex,yacc

#####Data structures
class Klass:
    def __init__(self,name:str):
        self.name=name
        self.super_classes=[]
    
    def __eq__(self, value):
        return self.name==value.name
    
    def __str__(self):
        return f"class {self.name} {self.super_classes}"

    def add_super_class(self,name:str):
        if name==self.name:
            raise ValueError("A class cannot inherit from itself")
        if name in self.super_classes:
            raise ValueError(f"Class {name} has been defined twice as a super class")
        self.super_classes.append(name)
    
    def __repr__(self):
        return self.name

class SymbolTable:
    def __init__(self):
        self.classes=[]
    
    def add_class(self,new_class:Klass):
        if new_class in self.classes:
            raise ValueError(f"Redefinition of class{new_class.name}")
        self.classes.append(new_class)
    
    def __str__(self):
        return "\n".join(f"{cl}" for cl in self.classes)

    def build_inheritance_graph(self):
        for kl in self.classes:
            supers=[]
            for sc in kl.super_classes:
                try:
                    super=self.get_class_by_name(sc)
                    supers.append(super)
                except:
                    raise ValueError(f"Unknown class {sc}")
            kl.super_classes=supers
    
    def check_circular_inheritance(self):
        nodes={kl.name:[] for kl in self.classes}
        for kl in self.classes:
            for sc in kl.super_classes:
                nodes[sc.name].append(kl.name)
        while nodes:
            nodes_with_no_pred=[n for n in nodes if not nodes[n]]
            if not nodes_with_no_pred:
                circuit=[next(iter(nodes.keys()))]
                while True:
                    if  nodes[circuit[-1]][0] not in circuit:
                        circuit.append(nodes[circuit[-1]][0])
                    else:
                        break
                raise ValueError(f"Circular inheritance detected between {circuit}")
            for remove_node in nodes_with_no_pred:
                for n in nodes:
                    if remove_node in nodes[n]:
                        nodes[n].remove(remove_node)
            nodes={n:pred for n,pred in nodes.items() if n not in nodes_with_no_pred}
        
    def get_class_by_name(self,name:str)->Klass:
        return next(kl for kl in self.classes if kl.name==name)
        

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

lexer=lex.lex()

def p_s(p):
    "s : cd"
    p[0]=p[1]
    p[0].build_inheritance_graph()
    p[0].check_circular_inheritance()

def p_cd(p):
    """cd : cd c1
    | c1
    """
    if len(p)==2:
        ast=SymbolTable()
        ast.add_class(p[1])
        p[0]=ast
    else:
        p[0]=p[1]
        p[0].add_class(p[2])

def p_c1(p):
    """c1 : CLASS ID param
    """
    kl=Klass(p[2])
    for n in p[3]:
        kl.add_super_class(n)
    p[0]=kl

def p_param(p):
    """param : LP inher RP 
    |
    """
    if len(p)==1:
        p[0]=[]
    else:
        p[0]=p[2]

def p_inher(p):
    """inher : inher COMMA ID 
    | ID
    """
    if len(p)==2:
        p[0]=[p[1]]
    else:
        p[0]=p[1]+[p[3]]
    
def p_error(p):
    raise ValueError("Syntax error")

parser=yacc.yacc()

with open("sample.oop") as f:
    text=f.read()

ast=parser.parse(text)
print(ast)
