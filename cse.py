"""
CSE (Control Stack Evaluation) for RPAL Compiler
Converted from C++ to Python
"""

from typing import List, Optional
from cse_nodes import (
    Base, CSE_Node, control_stk, stack_stk, parsing_env, control_structures,
    add_in_built_to_env, in_built_functions, is_bop, is_uop, print_base
)

from nodes import dt_bu, ast_stack, Node

env_count = 0  # Keeps track of the number of functions created

def pre_order_traversal(root: Node, environment: int) -> None:
    """Traverse through the tree and create arrays of control structures"""
    global env_count
    
    if root.label == "lambda":
        env_count += 1
        lambda_base = Base("lambda", env_count)
        control_structures.append([])
        
        # Create the function in a separate array
        pre_order_traversal(root.children[1], env_count)
        
        # Arguments: can be a single identifier or a list of identifiers
        if root.children[0].label != ",":
            sliced = root.children[0].label[4:-1]  # Remove <ID: and >
            lambda_base.children.append(Base("identifier", sliced))
        else:
            for i in range(len(root.children[0].children)):
                sliced = root.children[0].children[i].label[4:-1]  # Remove <ID: and >
                lambda_base.children.append(Base("identifier", sliced))
        
        control_structures[environment].append(lambda_base)

    elif root.label == "->":
        env_count += 1
        control_structures[environment].append(Base("delta", env_count))
        control_structures.append([])
        pre_order_traversal(root.children[1], env_count)
        
        env_count += 1
        control_structures[environment].append(Base("delta", env_count))
        control_structures.append([])
        pre_order_traversal(root.children[2], env_count)
        
        control_structures[environment].append(Base("beta"))
        pre_order_traversal(root.children[0], environment)
    
    else:
        if root.label.startswith('<'):
            if root.label.startswith('<I'):
                if root.label.startswith('<IN'):
                    # This is a number
                    num = int(root.label[5:-1])  # Remove <INT: and >
                    control_structures[environment].append(Base("integer", num))
                else:
                    # This is an identifier
                    sliced = root.label[4:-1]  # Remove <ID: and >
                    control_structures[environment].append(Base("identifier", sliced))
            else:
                # This is a string
                sliced = root.label[6:-2]  # Remove <STR:' and '>
                control_structures[environment].append(Base("string", sliced))

        elif is_bop(root.label) or is_uop(root.label):
            control_structures[environment].append(Base("operator", root.label))

        elif root.label in ["true", "false"]:
            control_structures[environment].append(Base("boolean", root.label))

        elif root.label == "Ystar":
            control_structures[environment].append(Base("ystar"))

        elif root.label == "tau":
            control_structures[environment].append(Base("tau", len(root.children)))

        elif root.label == "gamma":
            control_structures[environment].append(Base("gamma"))

        elif root.label == "dummy":
            control_structures[environment].append(Base("dummy"))

        elif root.label == "nil":
            control_structures[environment].append(Base("tuple"))
        
        # Iterate through the children
        for child in root.children:
            pre_order_traversal(child, environment)

def add_func_to_control(prev: Base, number: int) -> None:
    """Add a saved function to the control stack"""
    temp_env = Base("environment", prev)
    control_stk.append(temp_env)
    stack_stk.append(temp_env)
    parsing_env.append(temp_env)
    
    # Add the saved function to the control stack
    for base in control_structures[number]:
        control_stk.append(base)

def rules(type_name: str) -> None:
    """Rules regarding the control stack"""
    if type_name == "integer":
        stack_stk.append(control_stk.pop())
    
    elif type_name == "boolean":
        stack_stk.append(control_stk.pop())
    
    elif type_name == "operator":
        op = control_stk[-1].arg_str
        control_stk.pop()
        
        if op == "eq":
            a = stack_stk.pop()
            b = stack_stk.pop()
            if a.type == "integer" and b.type == "integer":
                result = "true" if a.arg_int == b.arg_int else "false"
                stack_stk.append(Base("boolean", result))
            elif a.type == "boolean" and b.type == "boolean":
                result = "true" if a.arg_str == b.arg_str else "false"
                stack_stk.append(Base("boolean", result))
            elif a.type == "string" and b.type == "string":
                result = "true" if a.arg_str == b.arg_str else "false"
                stack_stk.append(Base("boolean", result))
            else:
                print(f"Expect an integer or boolean or string pairs with {op}")
                raise Exception("Error")
        
        elif op == "ne":
            a = stack_stk.pop()
            b = stack_stk.pop()
            if a.type == "integer" and b.type == "integer":
                result = "false" if a.arg_int == b.arg_int else "true"
                stack_stk.append(Base("boolean", result))
            elif a.type == "boolean" and b.type == "boolean":
                result = "false" if a.arg_str == b.arg_str else "true"
                stack_stk.append(Base("boolean", result))
            elif a.type == "string" and b.type == "string":
                result = "false" if a.arg_str == b.arg_str else "true"
                stack_stk.append(Base("boolean", result))
            else:
                print(f"Expect an integer or boolean or string pairs with {op}")
                raise Exception("Error")
        
        elif op in ["+", "-", "*", "/", "**", "gr", "ge", "ls", "le"]:
            if stack_stk[-1].type != "integer":
                print(f"Expect an integer with {op}")
                raise Exception("Error")
            a = stack_stk.pop().arg_int
            if stack_stk[-1].type != "integer":
                print(f"Expect an integer with {op}")
                raise Exception("Error")
            b = stack_stk.pop().arg_int
            
            if op == "+":
                stack_stk.append(Base("integer", a + b))
            elif op == "-":
                stack_stk.append(Base("integer", a - b))
            elif op == "*":
                stack_stk.append(Base("integer", a * b))
            elif op == "/":
                stack_stk.append(Base("integer", a // b))  # Integer division
            elif op == "**":
                stack_stk.append(Base("integer", a ** b))
            elif op == "gr":
                result = "true" if a > b else "false"
                stack_stk.append(Base("boolean", result))
            elif op == "ge":
                result = "true" if a >= b else "false"
                stack_stk.append(Base("boolean", result))
            elif op == "ls":
                result = "true" if a < b else "false"
                stack_stk.append(Base("boolean", result))
            elif op == "le":
                result = "true" if a <= b else "false"
                stack_stk.append(Base("boolean", result))
        
        elif op == "neg":
            if stack_stk[-1].type != "integer":
                print(f"Expect an integer with {op}")
                raise Exception("Error")
            a = stack_stk.pop().arg_int
            stack_stk.append(Base("integer", -a))
        
        elif op == "not":
            if stack_stk[-1].type != "boolean":
                print(f"Expect a boolean with {op}")
                raise Exception("Error")
            a = stack_stk.pop().arg_str
            result = "false" if a == "true" else "true"
            stack_stk.append(Base("boolean", result))
        
        elif op in ["or", "&"]:
            if stack_stk[-1].type != "boolean":
                print(f"Expect a boolean with {op}")
                raise Exception("Error")
            a = stack_stk.pop().arg_str
            if stack_stk[-1].type != "boolean":
                print(f"Expect a boolean with {op}")
                raise Exception("Error")
            b = stack_stk.pop().arg_str
            
            if op == "or":
                result = "true" if a == "true" or b == "true" else "false"
                stack_stk.append(Base("boolean", result))
            else:  # op == "&"
                result = "true" if a == "true" and b == "true" else "false"
                stack_stk.append(Base("boolean", result))
        
        elif op == "aug":
            if stack_stk[-1].type != "tuple":
                print(f"Cannot append to {stack_stk[-1].type}")
                raise Exception("Error")
            list_base = stack_stk.pop()
            list_base.children.append(stack_stk.pop())
            stack_stk.append(list_base)
    
    elif type_name == "lambda":
        stack_stk.append(control_stk.pop())
        stack_stk[-1].prev = parsing_env[-1]
    
    elif type_name == "gamma":
        if stack_stk[-1].type == "lambda":
            func = stack_stk[-1]
            control_stk.pop()
            stack_stk.pop()
            
            func_args = stack_stk.pop()
            
            if func.arg_int >= 0:
                add_func_to_control(func.prev, func.arg_int)
                
                if len(func.children) > 1:
                    if len(func_args.children) != len(func.children):
                        print("Insufficient arguments")
                        raise Exception("Error")
                    else:
                        for i in range(len(func_args.children)):
                            temp = Base("identifier", func.children[i].arg_str)
                            temp.prev = func_args.children[i]
                            parsing_env[-1].children.append(temp)
                else:
                    parsing_env[-1].children.append(
                        Base("identifier", func.children[0].arg_str, func_args)
                    )
            else:
                in_built_functions(func, func_args)
        
        elif stack_stk[-1].type == "tuple":
            control_stk.pop()
            list_base = stack_stk.pop()
            index = stack_stk.pop().arg_int
            if index > len(list_base.children) or index <= 0:
                print(f"Index:{index} is out of bound in {list_base}")
                raise Exception("Error")
            stack_stk.append(list_base.children[index - 1])
        
        elif stack_stk[-1].type == "ystar":
            control_stk.pop()
            stack_stk.pop()
            lambda_base = stack_stk.pop()
            
            eta = Base("eta")
            eta.prev = lambda_base.prev
            eta.children = lambda_base.children
            eta.arg_int = lambda_base.arg_int
            
            stack_stk.append(eta)
        
        elif stack_stk[-1].type == "eta":
            control_stk.append(Base("gamma"))
            lambda_base = Base("lambda")
            lambda_base.prev = stack_stk[-1].prev
            lambda_base.children = stack_stk[-1].children
            lambda_base.arg_int = stack_stk[-1].arg_int
            stack_stk.append(lambda_base)
    
    elif type_name == "environment":
        returning = stack_stk.pop()
        if stack_stk[-1] == control_stk[-1]:
            control_stk.pop()
            stack_stk.pop()
            parsing_env.pop()
            stack_stk.append(returning)
        else:
            print("Error with environment Base")
            raise Exception("Error")
    
    elif type_name == "identifier":
        env = parsing_env[-1]
        value = None
        found = False
        
        while True:
            for child in env.children:
                if child.arg_str == control_stk[-1].arg_str:
                    found = True
                    value = child.prev
                    break
            if found:
                break
            else:
                env = env.prev
                if env is None:
                    break
        
        if not found:
            print(f"Identifier {control_stk[-1].arg_str} not found")
            raise Exception("Error")
        else:
            stack_stk.append(value)
            control_stk.pop()
    
    elif type_name == "delta":
        temp = control_stk.pop()
        for base in control_structures[temp.arg_int]:
            control_stk.append(base)
    
    elif type_name == "tau":
        list_base = Base("tuple")
        for _ in range(control_stk[-1].arg_int):
            list_base.children.append(stack_stk.pop())
        stack_stk.append(list_base)
        control_stk.pop()
    
    elif type_name == "ystar":
        stack_stk.append(control_stk.pop())
    
    elif type_name == "beta":
        if stack_stk[-1].arg_str == "true":
            control_stk.pop()
            control_stk.pop()
            stack_stk.pop()
        elif stack_stk[-1].arg_str == "false":
            control_stk.pop()
            temp = control_stk.pop()
            control_stk.pop()
            control_stk.append(temp)
            stack_stk.pop()
        else:
            print("Expect a boolean")
            raise Exception("Error")
    
    elif type_name == "tuple":
        stack_stk.append(control_stk.pop())
    
    elif type_name == "string":
        stack_stk.append(control_stk.pop())
    
    else:
        print("Error with Base")
        raise Exception("Error")

def cse() -> None:
    """CSE function handles all other functions"""
    global control_structures
    
    # Create a blank array for the main function
    control_structures.append([])
    pre_order_traversal(ast_stack[-1], 0)  # Assuming ast_bu.top() equivalent
    
    # Initialize a global parsing environment
    parsing_env.append(Base("environment"))
    parsing_env[-1].prev = None
    # Add built-in identifiers
    add_in_built_to_env(parsing_env[-1])
    add_func_to_control(parsing_env[-1], 0)
    
    # Iterate through the control stack and evaluate
    while len(control_stk) > 1:
        the_type = control_stk[-1].type
        rules(the_type)
    
    temp = stack_stk.pop()
    if stack_stk[-1] != control_stk[-1]:
        print("Run time Error")
        raise Exception("Run time Error")