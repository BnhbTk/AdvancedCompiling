class Node:
    def max_depth(self):
        raise ValueError("You are not supposed to run this")




class Symbol(Node):
    def __init__(self,value:str):
        self.value=value
    
    def max_depth(self):
        return 0
    
    def __str__(self):
        return self.value

class Par(Node):
    def __init__(self,content:Node):
        self.content=content
    
    def max_depth(self):
        return self.content.max_depth()+1
    
    def __str__(self):
        return f"({self.content})"

class Concat(Node):
    def __init__(self,*children:list[Node]):
        self.children=children
    
    def max_depth(self):
        return max([c.max_depth() for c in self.children])
    
    def __str__(self):
        return "".join([f"{c}" for c in self.children])
    

#(abc)((a)b)
ast=Concat(
        Par(
            Concat(
                Symbol("a"),
                Symbol("b"),
                Symbol("c")
            )
        ),
        Par(
            Concat(
                Par(
                    Symbol("a")
                ),
                Symbol("b")
            )
        )
    )

print(ast.max_depth())
print(ast)
