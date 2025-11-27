# This import allows to use the special class ABC (intended as a base class
# for all abstract classes)
from abc import ABC

# This import is used to declare the type of the arguments of the constructor
# of PR
from typing import Tuple

# The base class
class Node(ABC):
    pass

    def __str__(self)->str:
        return ""


class Symbol(Node):
    """This class represents a simple symbol in the AST
    """
    
    def __init__(self,c:str):
        """This constructor builds a symbol node. It takes the symbol as an argument

        Args:
            c (str): the symbol to be stored in the node
        """
        self.c:str=c
    
    def __str__(self)->str:
        """This methods returns a string representation of the node (in this case,
        it is just the symbol itself)

        Returns:
            str: the string description of the object
        """
        return self.c
    


class PR(Node):
    """This class represent a pair of parentheses and the content inside.There is just one content inside the parentheses
    """
    def __init__(self,node:Node):
        """This constructor builds the PR node. It takes one node as a child
        Args:
            *node (Node): the child of this nod
        """
        self.node=node
    
    def __str__(self)->str:
        """This methods returns a string representation of this node. It consist of "("
        followed by the string representations of its content and a final ")". This function is recursive.

        Returns:
            str: The string representation of this node
        """
        return f'PR({node})'

class PR(Node):
    """This class represent a pair of parentheses and the content inside.There is just one content inside the parentheses
    """
    def __init__(self,node:Node):
        """This constructor builds the PR node. It takes one node as a child
        Args:
            *node (Node): the child of this nod
        """
        self.node=node
    
    def __str__(self)->str:
        """This methods returns a string representation of this node. It consist of "("
        followed by the string representations of its content and a final ")". This function is recursive.

        Returns:
            str: The string representation of this node
        """
        return f'({self.node})'

class Concat(Node):
    """This class represent the concatenation of many nodes. It stores them as children
    """
    def __init__(self,*nodes:Tuple[Node]):
        """This constructor builds the Concat node. It takes the children as varagrs
        Args:
            *node (Tuple[Node]): the child of this nod
        """
        self.children=nodes
    
    def __str__(self)->str:
        """This methods returns a string representation of this node. It consist of a conctaenation of
        its children. This function is recursive.

        Returns:
            str: The string representation of this node
        """
        return f'{"".join([str(ch) for ch in self.children])}'


if __name__=="__main__":
    node:Node=Concat(Concat(Symbol("a"),PR(Concat(Concat(Symbol("a"),PR(Concat(Symbol("b"),Symbol("c")))),Symbol("c")))),Symbol("d")) # This represents the word a(a(bc)c)d
    print(node)
