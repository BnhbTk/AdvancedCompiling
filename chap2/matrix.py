from ply import lex,yacc

####### The scanner
tokens=("LB","RB","COMMA","CST")

t_LB=r"\["
t_RB=r"\]"
t_COMMA=","
t_CST="[0-9]+"
t_ignore=" "

def t_error(t):
    print(f"Illegal token {t}")

lex.lex()

######## The parser: here we also build the AST as a list of lists
def p_s(p):
    "s : LB lines RB"
    p[0]=p[2]

def p_lines(p):
    """lines : line
    | line COMMA lines
    """
    if len(p)==2:
        p[0]=[p[1]]
    else:
        p[0]=[p[1]]+p[3]

def p_line(p):
    """line : CST
    | CST line
    """
    if len(p)==2:
        p[0]=[int(p[1])]
    else:
        p[0]=[int(p[1])]+p[2]
        

def p_error(p):
    print("Syntax error")

parser=yacc.yacc()
mat=parser.parse("[1,2 3 4]")

# This is the algorithmic solution, not a pythonic way to do things
#l=len(mat[0])
# for i in range(1,len(mat)):
#     if len(mat[i])!=l:
#         raise ValueError("Malformed matrix")

# Check if there any row with a number of columns different from the number of columns
# in the first row
if any([len(row)!=len(mat[0]) for row in mat[1:]]):
    raise ValueError("Malformed matrix")
print(f"Well formed matrix {mat}")  

    
