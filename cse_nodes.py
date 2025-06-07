"""
CSE Structures for RPAL Compiler
Converted from C++ to Python
"""

from typing import List, Optional, Union, Any
from nodes import dt_bu, ast_stack
import re

class Base:
    """
    Base class representing nodes in control stack and stack stack
    
    Types and their storage:
    - string: type="string", arg_str=value
    - tuple: type="tuple", children=values as Base objects
    - integer: type="integer", arg_int=value  
    - boolean: type="boolean", arg_str="true" or "false"
    - function: type="lambda", arg_str=name, arg_int=stored index, children=function parameters, prev=called environment
    - dummy: type="dummy" (actual value of each print() output)
    """
    
    def __init__(self, type_name: str, *args, **kwargs):
        self.type = type_name
        self.arg_str = ""
        self.arg_int = 0
        self.prev: Optional['Base'] = None
        self.children: List['Base'] = []
        
        # Handle different constructor signatures
        if len(args) == 1:
            if isinstance(args[0], int):
                self.arg_int = args[0]
            elif isinstance(args[0], str):
                self.arg_str = args[0]
            elif isinstance(args[0], Base):
                self.prev = args[0]
        elif len(args) == 2:
            if isinstance(args[0], str) and isinstance(args[1], int):
                self.arg_str = args[0]
                self.arg_int = args[1]
            elif isinstance(args[0], str) and isinstance(args[1], Base):
                self.arg_str = args[0]
                self.prev = args[1]
        
        # Handle keyword arguments
        if 'prev' in kwargs:
            self.prev = kwargs['prev']
        if 'arg_str' in kwargs:
            self.arg_str = kwargs['arg_str']
        if 'arg_int' in kwargs:
            self.arg_int = kwargs['arg_int']

# Global stacks and structures
control_stk: List[Base] = []       # Working control stack
stack_stk: List[Base] = []         # Working stack stack  
parsing_env: List[Base] = []       # Stored environments
control_structures: List[List[Base]] = []  # Stores each function present in the syntax tree

# Mock structures (assuming these exist in your full implementation)
# ast_bu: List[Any] = []  # AST build up stack
# dt_bu: List[str] = []   # Data type build up

def add_in_built_to_env(env: Base) -> None:
    """Add built-in functions to environment"""
    
    # Defining internal variables (commented out in original)
    # env.children.append(Base("identifier", "hundred", Base("integer", 100)))
    
    # Defining built-in functions
    env.children.append(Base("identifier", "Print", Base("lambda", -1)))
    env.children.append(Base("identifier", "print", Base("lambda", -1)))
    env.children.append(Base("identifier", "Isinteger", Base("lambda", -2)))
    env.children.append(Base("identifier", "Isstring", Base("lambda", -3)))
    env.children.append(Base("identifier", "Istuple", Base("lambda", -4)))
    env.children.append(Base("identifier", "Isfunction", Base("lambda", -5)))
    env.children.append(Base("identifier", "Isdummy", Base("lambda", -6)))
    env.children.append(Base("identifier", "Stem", Base("lambda", -7)))
    env.children.append(Base("identifier", "Stern", Base("lambda", -8)))
    env.children.append(Base("identifier", "Conc", Base("lambda", -9)))
    env.children.append(Base("identifier", "Order", Base("lambda", -10)))
    env.children.append(Base("identifier", "Null", Base("lambda", -11)))
    env.children.append(Base("identifier", "ItoS", Base("lambda", -12)))

def print_base(env: Base) -> None:
    """Print a Base structure"""
    if env.type == "tuple":
        print("(", end="")
        if len(env.children) > 0:
            print_base(env.children[0])
        for i in range(1, len(env.children)):
            print(", ", end="")
            print_base(env.children[i])
        print(")", end="")
    elif env.type == "integer":
        print(env.arg_int, end="")
    elif env.type == "boolean":
        print(env.arg_str, end="")
    elif env.type == "string":
        i = 0
        while i < len(env.arg_str):
            if env.arg_str[i] == '\\':
                i += 1
                if i < len(env.arg_str):
                    if env.arg_str[i] == 'n':
                        print("\n", end="")
                    elif env.arg_str[i] == 't':
                        print("\t", end="")
                    elif env.arg_str[i] == 'b':
                        print("\b", end="")
                    elif env.arg_str[i] == '\\':
                        print("\\", end="")
                    elif env.arg_str[i] == '"':
                        print('"', end="")
                    elif env.arg_str[i] == "'":
                        print("'", end="")
                    else:
                        if i > 0:
                            sub = env.arg_str[i-1:i+1]
                            print(sub, end="")
                else:
                    print("\\", end="")
            else:
                print(env.arg_str[i], end="")
            i += 1

def in_built_functions(func: Base, func_args: Base) -> None:
    """Execute built-in functions based on function index"""
    val = func.arg_int
    
    if val == -1:  # Print
        print_base(func_args)
        print()
        stack_stk.append(Base("dummy"))
    elif val == -2:  # Isinteger
        if func_args.type == "integer":
            stack_stk.append(Base("boolean", "true"))
        else:
            stack_stk.append(Base("boolean", "false"))
    elif val == -3:  # Isstring
        if func_args.type == "string":
            stack_stk.append(Base("boolean", "true"))
        else:
            stack_stk.append(Base("boolean", "false"))
    elif val == -4:  # Istuple
        if func_args.type == "tuple":
            stack_stk.append(Base("boolean", "true"))
        else:
            stack_stk.append(Base("boolean", "false"))
    elif val == -5:  # Isfunction
        if func_args.type == "lambda":
            stack_stk.append(Base("boolean", "true"))
        else:
            stack_stk.append(Base("boolean", "false"))
    elif val == -6:  # Isdummy
        if func_args.type == "dummy":
            stack_stk.append(Base("boolean", "true"))
        else:
            stack_stk.append(Base("boolean", "false"))
    elif val == -7:  # Stem
        if func_args.type != "string":
            print("Expect a string with Stem")
            raise Exception("Error")
        if len(func_args.arg_str) == 0:
            print("Expect a string at least of size 1 with Stem")
            raise Exception("Error")
        stack_stk.append(Base("string", func_args.arg_str[0]))
    elif val == -8:  # Stern
        if func_args.type != "string":
            print("Expect a string with Stern")
            raise Exception("Error")
        if len(func_args.arg_str) == 0:
            print("Expect a string at least of size 1 with Stern")
            raise Exception("Error")
        stack_stk.append(Base("string", func_args.arg_str[1:]))
    elif val == -9:  # Conc
        if func_args.type != "string" or stack_stk[-1].type != "string":
            print("Expect two strings with Conc")
            raise Exception("Error")
        temp = stack_stk.pop()
        control_stk.pop()
        output = func_args.arg_str + temp.arg_str
        stack_stk.append(Base("string", output))
    elif val == -10:  # Order
        if func_args.type != "tuple":
            print("Expect a tuple with Order")
            raise Exception("Error")
        stack_stk.append(Base("integer", len(func_args.children)))
    elif val == -11:  # Null
        if func_args.type != "tuple":
            print("Expect a tuple with Null")
            raise Exception("Error")
        if len(func_args.children) == 0:
            stack_stk.append(Base("boolean", "true"))
        else:
            stack_stk.append(Base("boolean", "false"))
    elif val == -12:  # ItoS
        if func_args.type != "integer":
            print("Expect an integer with ItoS")
            raise Exception("Error")
        stack_stk.append(Base("string", str(func_args.arg_int)))

def clear_stacks() -> None:
    """Clear all stacks and structures"""
    global ast_stack, dt_bu
    ast_stack.clear()
    dt_bu.clear()

# Utility functions that might be referenced in the main CSE file
def is_bop(token: str) -> bool:
    """Check if token is a binary operator"""
    binary_ops = ["+", "-", "*", "/", "**", "eq", "ne", "gr", "ge", "ls", "le", "or", "&", "aug"]
    return token in binary_ops

def is_uop(token: str) -> bool:
    """Check if token is a unary operator"""
    unary_ops = ["neg", "not"]
    return token in unary_ops

# Mock Node class (assuming this exists in your AST implementation)
class CSE_Node:
    def __init__(self, token: str = ""):
        self.token = token
        self.children: List['CSE_Node'] = []