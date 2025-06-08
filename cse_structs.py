from typing import List, Optional

class Base:
    def __init__(
        self,
        type_: str,
        arg_str: Optional[str] = None,
        arg_int: Optional[int] = None,
        prev: Optional['Base'] = None
    ):
        self.type = type_
        self.arg_str = arg_str
        self.arg_int = arg_int
        self.prev = prev
        self.children: List['Base'] = []

    # Mimic C++-style overloaded constructors using classmethods
    @classmethod
    def from_type(cls, type_: str):
        return cls(type_)

    @classmethod
    def from_type_arg_int(cls, type_: str, arg_int: int):
        return cls(type_, arg_int=arg_int)

    @classmethod
    def from_type_arg_str(cls, type_: str, arg_str: str):
        return cls(type_, arg_str=arg_str)

    @classmethod
    def from_type_arg_str_arg_int(cls, type_: str, arg_str: str, arg_int: int):
        return cls(type_, arg_str=arg_str, arg_int=arg_int)

    @classmethod
    def from_type_arg_str_prev(cls, type_: str, arg_str: str, prev: 'Base'):
        return cls(type_, arg_str=arg_str, prev=prev)

    @classmethod
    def from_type_prev(cls, type_: str, prev: 'Base'):
        return cls(type_, prev=prev)

    def __repr__(self):
        return (
            f"Base(type={self.type}, arg_str={self.arg_str}, "
            f"arg_int={self.arg_int}, prev={repr(self.prev)}, children={self.children})"
        )

# Global stacks and structures
control_stk = []
stack_stk = []
parsing_env = []
control_structures = []

def add_in_built_to_env(env: Base):
    env.children.append(Base("identifier", "Print", -1))
    env.children.append(Base("identifier", "print", -1))
    env.children.append(Base("identifier", "Isinteger", -2))
    env.children.append(Base("identifier", "Isstring", -3))
    env.children.append(Base("identifier", "Istuple", -4))
    env.children.append(Base("identifier", "Isfunction", -5))
    env.children.append(Base("identifier", "Isdummy", -6))
    env.children.append(Base("identifier", "Stem", -7))
    env.children.append(Base("identifier", "Stern", -8))
    env.children.append(Base("identifier", "Conc", -9))
    env.children.append(Base("identifier", "Order", -10))
    env.children.append(Base("identifier", "Null", -11))
    env.children.append(Base("identifier", "ItoS", -12))

def print_Base(env: Base):
    if env.type == "tuple":
        print("(", end="")
        for i, child in enumerate(env.children):
            if i > 0:
                print(", ", end="")
            print_Base(child)
        print(")", end="")
    elif env.type == "integer":
        print(env.arg_int, end="")
    elif env.type == "boolean":
        print(env.arg_str, end="")
    elif env.type == "string":
        s = env.arg_str or ""
        i = 0
        while i < len(s):
            if s[i] == '\\':
                i += 1
                if i < len(s):
                    if s[i] == 'n':
                        print("\n", end="")
                    elif s[i] == 't':
                        print("\t", end="")
                    elif s[i] == 'b':
                        print("\b", end="")
                    elif s[i] == '\\':
                        print("\\", end="")
                    elif s[i] == '"':
                        print("\"", end="")
                    elif s[i] == "'":
                        print("'", end="")
                    else:
                        print(s[i-1:i+1], end="")
                else:
                    print("\\", end="")
            else:
                print(s[i], end="")
            i += 1

def in_built_functions(func: Base, func_args: Base):
    val = func.arg_int
    if val == -1:
        print_Base(func_args)
        print()
        stack_stk.append(Base("dummy"))
    elif val == -2:
        stack_stk.append(Base("boolean", "true" if func_args.type == "integer" else "false"))
    elif val == -3:
        stack_stk.append(Base("boolean", "true" if func_args.type == "string" else "false"))
    elif val == -4:
        stack_stk.append(Base("boolean", "true" if func_args.type == "tuple" else "false"))
    elif val == -5:
        stack_stk.append(Base("boolean", "true" if func_args.type == "lambda" else "false"))
    elif val == -6:
        stack_stk.append(Base("boolean", "true" if func_args.type == "dummy" else "false"))
    elif val == -7:
        if func_args.type != "string" or not func_args.arg_str:
            raise Exception("Expect a non-empty string with Stem")
        stack_stk.append(Base("string", func_args.arg_str[0]))
    elif val == -8:
        if func_args.type != "string" or not func_args.arg_str:
            raise Exception("Expect a non-empty string with Stern")
        stack_stk.append(Base("string", func_args.arg_str[1:]))
    elif val == -9:
        if func_args.type != "string" or not stack_stk or stack_stk[-1].type != "string":
            raise Exception("Expect two strings with Conc")
        temp = stack_stk.pop()
        output = (func_args.arg_str or "") + (temp.arg_str or "")
        stack_stk.append(Base("string", output))
    elif val == -10:
        if func_args.type != "tuple":
            raise Exception("Expect a tuple with Order")
        stack_stk.append(Base("integer", arg_int=len(func_args.children)))
    elif val == -11:
        if func_args.type != "tuple":
            raise Exception("Expect a tuple with Null")
        stack_stk.append(Base("boolean", "true" if len(func_args.children) == 0 else "false"))
    elif val == -12:
        if func_args.type != "integer":
            raise Exception("Expect an integer with ItoS")
        stack_stk.append(Base("string", str(func_args.arg_int)))

def clear_stacks():
    control_stk.clear()
    stack_stk.clear()
    parsing_env.clear()
    control_structures.clear()

def print_environments():
    print("=== Environments (parsing_env) ===")
    for i, env in enumerate(parsing_env):
        print(f"Env {i}: type={env.type}, prev={id(env.prev) if env.prev else None}")
        for child in env.children:
            print(f"  Identifier: {child.arg_str}, Value: {repr(child.prev)}")

def print_control_structures():
    print("=== Control Structures ===")
    for i, cs in enumerate(control_structures):
        print(f"Control Structure {i}:")
        for item in cs:
            print(f"  {repr(item)}")