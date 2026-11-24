from collections import namedtuple
from typing import Any


def to_bytes(st:dict[str,Any])->tuple[bytearray,dict[str,int]]:
    adrs={v:0 for v in st}
    memory=bytearray()
    adr=0
    for name,v in st.items():
        adrs[name]=len(memory)
        if type(v) is int:
            tmp=v.to_bytes(4,byteorder='big')
            memory.extend(tmp)
        elif type(v) is bool:
            adr+=1
            memory.append(1 if v else 0)
        else:
            s=[ord(c) for c in f"{v}"]
            memory.extend(s)
            memory.append(0)
    return memory,adrs

Instruction=namedtuple("Instruction",["op","param"])

def load_asm(file_name:str)->list[Instruction]:
    with open(file_name) as f:
        block=list(map(lambda s:s.split(" "),filter(lambda s:s,f.read().split("\n"))))
        return [Instruction(s[0],int(s[1]) if len(s)>1 else 0) for s in block]

def execute(instructions:list[Instruction],memory:bytearray,stack_size:int=100000):
    def push_int(v:int):
        nonlocal sp
        stack[sp:sp+4]=v.to_bytes(4,byteorder='big')
        sp+=4
    def push_bool(v:bool):
        nonlocal sp
        stack[sp]=1 if v else 0
        sp+=1

    def pop_int()->int:
        nonlocal sp
        reg=stack[sp-4:sp]
        sp-=4
        return int.from_bytes(reg,'big')

    def pop_bool()->bool:
        nonlocal sp
        reg=stack[sp-1]
        sp-=1
        return reg==1

    stack=bytearray(100000)
    sp=0
    cp=0
    while True:
        inst=instructions[cp]
        cp+=1
        match inst.op:
            case "add":
                push_int(pop_int()+pop_int())
            case "sub":
                push_int(-pop_int()+pop_int())
            case "mul":
                push_int(pop_int()*pop_int())
            case "div":
                a=pop_int()
                push_int(pop_int()//a)
            case "mod":
                a=pop_int()
                push_int(pop_int()%a)
            case "minus":
                push_int(-pop_int())
            case "and":
                push_int(pop_bool() and pop_bool())
            case "and":
                push_int(pop_bool() or pop_bool())
            case "not":
                push_int(pop_bool() or pop_bool())
            case "pushi":
                push_int(inst.param)
            case "pushb":
                push_bool(inst.param==1)
            case "loadi":
                push_int(int.from_bytes(memory[inst.param:inst.param+4],"big"))
            case "loadb":
                push_bool(memory[inst.param]==1)
            case "storei":
                memory[inst.param:inst.param+4]=pop_int().to_bytes(4,"big")
            case "storeb":
                memory[inst.param]=1 if pop_bool() else 0
            case "printi":
                print(pop_int(),end="")
            case "printb":
                print(pop_bool(),end="")
            case "print":
                tmp=pop_int()
                while memory[tmp]:
                    print(chr(memory[tmp]),end="")
                    tmp+=1
            case "eqi":
                push_bool(pop_int()==pop_int())
            case "eqb":
                push_bool(pop_bool()==pop_bool())
            case "gt":
                push_bool(pop_int()<pop_int())
            case "gte":
                push_bool(pop_int()<=pop_int())
            case "jz":
                if pop_bool():
                    cp=inst.param
            case "jnz":
                if not pop_bool():
                    cp=inst.param
            case "goto":
                cp=inst.param
            case "halt":
                break
            case _:
                raise Exception(f"Unknown code {inst.op}")

# This is the how memory will be organized
memory,adrs=to_bytes({"i":0,"s":"\n"})
print("Loading file...",end="")
prgm=load_asm("simple.asm")
print("Done")
execute(prgm,memory)
