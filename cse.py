from cse_structs import Base, control_stk, stack_stk, parsing_env, control_structures, add_in_built_to_env, in_built_functions, print_control_structures
from vocabulary import is_binary_operator as isBOp, is_unary_operator as isUOp
from nodes import ast_stack as ast_bu  # or wherever your AST stack is defined

env_count = 0

def add_func_to_control(prev, number):
    temp_env = Base("environment", prev=prev)
    control_stk.append(temp_env)
    stack_stk.append(temp_env)
    parsing_env.append(temp_env)
    for item in control_structures[number]:
        control_stk.append(item)

def pre_order_traversal(root, environment):
    global env_count
    if root.label == "lambda":
        env_count += 1
        lambda_base = Base("lambda", arg_int=env_count)
        control_structures.append([])
        pre_order_traversal(root.children[1], env_count)
        # Arguments: can be a single identifier or a list
        if root.children[0].label != ",":
            sliced = root.children[0].label[4:-1]
            # print(Base("identifier", sliced))
            lambda_base.children.append(Base("identifier", sliced))
        else:
            for child in root.children[0].children:
                sliced = child.label[4:-1]
                lambda_base.children.append(Base("identifier", sliced))
        control_structures[environment].append(lambda_base)
    elif root.label == "->":
        env_count += 1
        control_structures[environment].append(Base("delta", arg_int=env_count))
        control_structures.append([])
        pre_order_traversal(root.children[1], env_count)
        env_count += 1
        control_structures[environment].append(Base("delta", arg_int=env_count))
        control_structures.append([])
        pre_order_traversal(root.children[2], env_count)
        control_structures[environment].append(Base("beta"))
        pre_order_traversal(root.children[0], environment)
    else:
        if root.label.startswith("<"):
            if root.label[1] == "I":
                if root.label[2] == "N":
                    num = int(root.label[5:-1])
                    control_structures[environment].append(Base("integer", arg_int=num))
                else:
                    sliced = root.label[4:-1]
                    control_structures[environment].append(Base("identifier", sliced))
            else:
                sliced = root.label[6:-2]
                control_structures[environment].append(Base("string", sliced))
        elif isBOp(root.label) or isUOp(root.label):
            control_structures[environment].append(Base("operator", root.label))
        elif root.label in ("true", "false"):
            control_structures[environment].append(Base("boolean", root.label))
        elif root.label == "Ystar":
            control_structures[environment].append(Base("ystar"))
        elif root.label == "tau":
            control_structures[environment].append(Base("tau", arg_int=len(root.children)))
        elif root.label == "gamma":
            control_structures[environment].append(Base("gamma"))
        elif root.label == "dummy":
            control_structures[environment].append(Base("dummy"))
        elif root.label == "nil":
            control_structures[environment].append(Base("tuple"))
        for child in root.children:
            pre_order_traversal(child, environment)
print
def rules(type_):
    if type_ == "integer" or type_ == "boolean" or type_ == "string" or type_ == "tuple":
        stack_stk.append(control_stk[-1])
        control_stk.pop()
    elif type_ == "operator":
        op = control_stk[-1].arg_str
        control_stk.pop()
        if op == "eq":
            a = stack_stk[-1]
            stack_stk.pop()
            b = stack_stk[-1]
            stack_stk.pop()
            if a.type == "integer" and b.type == "integer":
                if a.arg_int == b.arg_int:
                    stack_stk.append(Base("boolean", "true"))
                else:
                    stack_stk.append(Base("boolean", "false"))
            elif a.type == "boolean" and b.type == "boolean":
                if a.arg_str == b.arg_str:
                    stack_stk.append(Base("boolean", "true"))
                else:
                    stack_stk.append(Base("boolean", "false"))
            elif a.type == "string" and b.type == "string":
                if a.arg_str == b.arg_str:
                    stack_stk.append(Base("boolean", "true"))
                else:
                    stack_stk.append(Base("boolean", "false"))
            else:
                print(f"Expect an integer or boolean or string pairs with {op}")
                raise RuntimeError("Error")
        elif op == "ne":
            a = stack_stk[-1]
            stack_stk.pop()
            b = stack_stk[-1]
            stack_stk.pop()
            if a.type == "integer" and b.type == "integer":
                if a.arg_int == b.arg_int:
                    stack_stk.append(Base("boolean", "false"))
                else:
                    stack_stk.append(Base("boolean", "true"))
            elif a.type == "boolean" and b.type == "boolean":
                if a.arg_str == b.arg_str:
                    stack_stk.append(Base("boolean", "false"))
                else:
                    stack_stk.append(Base("boolean", "true"))
            elif a.type == "string" and b.type == "string":
                if a.arg_str == b.arg_str:
                    stack_stk.append(Base("boolean", "false"))
                else:
                    stack_stk.append(Base("boolean", "true"))
            else:
                print(f"Expect an integer or boolean or string pairs with {op}")
                raise RuntimeError("Error")
        elif op in ("+", "-", "*", "/", "**", "gr", "ge", "ls", "le"):
            if stack_stk[-1].type != "integer":
                print(f"Expect an integer with {op}")
                raise RuntimeError("Error")
            a = stack_stk[-1].arg_int
            stack_stk.pop()
            if stack_stk[-1].type != "integer":
                print(f"Expect an integer with {op}")
                raise RuntimeError("Error")
            b = stack_stk[-1].arg_int
            stack_stk.pop()
            if op == "+":
                stack_stk.append(Base("integer", arg_int =  a + b))
            elif op == "-":
                stack_stk.append(Base("integer", arg_int = a - b))
            elif op == "*":
                stack_stk.append(Base("integer", arg_int = a * b))
            elif op == "/":
                stack_stk.append(Base("integer", arg_int = a // b))
            elif op == "**":
                stack_stk.append(Base("integer", arg_int = pow(a, b)))
            elif op == "gr":
                if a > b:
                    stack_stk.append(Base("boolean", "true"))
                else:
                    stack_stk.append(Base("boolean", "false"))
            elif op == "ge":
                if a >= b:
                    stack_stk.append(Base("boolean", "true"))
                else:
                    stack_stk.append(Base("boolean", "false"))
            elif op == "ls":
                if a < b:
                    stack_stk.append(Base("boolean", "true"))
                else:
                    stack_stk.append(Base("boolean", "false"))
            else:  # op == "le"
                if a <= b:
                    stack_stk.append(Base("boolean", "true"))
                else:
                    stack_stk.append(Base("boolean", "false"))
        elif op == "neg":
            if stack_stk[-1].type != "integer":
                print(f"Expect an integer with {op}")
                raise RuntimeError("Error")
            a = stack_stk[-1].arg_int
            stack_stk.pop()
            stack_stk.append(Base("integer", arg_int = -a))
        elif op == "not":
            if stack_stk[-1].type != "boolean":
                print(f"Expect a boolean with {op}")
                raise RuntimeError("Error")
            a = stack_stk[-1].arg_str
            stack_stk.pop()
            if a == "true":
                stack_stk.append(Base("boolean", "false"))
            else:
                stack_stk.append(Base("boolean", "true"))
        elif op in ("or", "&"):
            if stack_stk[-1].type != "boolean":
                print(f"Expect a boolean with {op}")
                raise RuntimeError("Error")
            a = stack_stk[-1].arg_str
            stack_stk.pop()
            if stack_stk[-1].type != "boolean":
                print(f"Expect a boolean with {op}")
                raise RuntimeError("Error")
            b = stack_stk[-1].arg_str
            stack_stk.pop()
            if op == "or":
                if a == "true" or b == "true":
                    stack_stk.append(Base("boolean", "true"))
                else:
                    stack_stk.append(Base("boolean", "false"))
            else:  # (op == "&")
                if a == "true" and b == "true":
                    stack_stk.append(Base("boolean", "true"))
                else:
                    stack_stk.append(Base("boolean", "false"))
        elif op == "aug":
            if stack_stk[-1].type != "tuple":
                print(f"Cannot append to {stack_stk[-1].type}")
                raise RuntimeError("Error")
            lst = stack_stk[-1]
            stack_stk.pop()
            lst.children.append(stack_stk[-1])
            stack_stk.pop()
            stack_stk.append(lst)
    elif type_ == "lambda":
        stack_stk.append(control_stk[-1])
        control_stk.pop()
        stack_stk[-1].prev = parsing_env[-1]
    elif type_ == "gamma":
        # print(stack_stk[-1])
        if stack_stk[-1].type == "lambda":
            # print("Lambda found")
            func = stack_stk[-1]
            control_stk.pop()
            stack_stk.pop()
            func_args = stack_stk[-1]
            stack_stk.pop()
            if func.arg_int is not None and func.arg_int >= 0:
                add_func_to_control(func.prev, func.arg_int)
                if len(func.children) > 1:
                    if len(func_args.children) != len(func.children):
                        raise RuntimeError("Insufficient arguments")
                    for i in range(len(func_args.children)):
                        temp = Base("identifier", func.children[i].arg_str)
                        temp.prev = func_args.children[i]
                        parsing_env[-1].children.append(temp)
                else:
                    parsing_env[-1].children.append(Base("identifier", func.children[0].arg_str, prev = func_args))
                    # print(Base("identifier", func.children[0].arg_str, prev = func_args))
            else:
                in_built_functions(func, func_args)
        elif stack_stk[-1].type == "tuple":
            control_stk.pop()
            lst = stack_stk[-1]
            stack_stk.pop()
            index = stack_stk[-1].arg_int
            # print(stack_stk[-1])
            stack_stk.pop()
            # print(index)
            # print("/n")
            if (index > len(lst.children)) or (index <= 0):
                print(f"Index:{index} is out of bound in ")
                # print_Base(lst)  # Assuming you have a function to print the Base structure
                raise RuntimeError("Error")
            stack_stk.append(lst.children[index - 1])
        elif stack_stk[-1].type == "ystar":
            control_stk.pop()
            stack_stk.pop()
            lambda_ = stack_stk[-1]
            stack_stk.pop()
            eta = Base("eta")
            eta.prev = lambda_.prev
            eta.children = lambda_.children
            eta.arg_int = lambda_.arg_int
            stack_stk.append(eta)
        elif stack_stk[-1].type == "eta":
            control_stk.append(Base("gamma"))
            lambda_ = Base("lambda")
            lambda_.prev = stack_stk[-1].prev
            lambda_.children = stack_stk[-1].children
            lambda_.arg_int = stack_stk[-1].arg_int
            stack_stk.append(lambda_)
            
    elif type_ == "environment":
        returning = stack_stk[-1]
        stack_stk.pop()
        if stack_stk[-1] == control_stk[-1]:
            control_stk.pop()
            stack_stk.pop()
            parsing_env.pop()
            stack_stk.append(returning)
        else:
            print("Error with environment Base")
            raise RuntimeError("Error")
    elif type_ == "identifier":
        env = parsing_env[-1]
        value = None
        found = False
        while True:
            for child in env.children:
                if child.arg_str == control_stk[-1].arg_str:
                    found = True
                    if child.prev :
                        value = child.prev
                    else:
                        child.type = "lambda"
                        value = child
                    # print(child)
                    break
            if found:
                break
            else:
                env = env.prev
                if env is None:
                    break
        if not found:
            print(f"Identifier {control_stk[-1].arg_str} not found")
            raise RuntimeError("Error")
        else:
            stack_stk.append(value)
            control_stk.pop()
    elif type_ == "delta":
        temp = control_stk[-1]
        control_stk.pop()
        for item in control_structures[temp.arg_int]:
            control_stk.append(item)
    elif type_ == "tau":
        lst = Base("tuple")
        for _ in range(control_stk[-1].arg_int):
            lst.children.append(stack_stk[-1])
            stack_stk.pop()
        stack_stk.append(lst)
        control_stk.pop()
    elif type_ == "ystar":
        stack_stk.append(control_stk[-1])
        control_stk.pop()
    elif type_ == "beta":
        if stack_stk[-1].arg_str == "true":
            control_stk.pop()
            control_stk.pop()
            stack_stk.pop()
        elif stack_stk[-1].arg_str == "false":
            control_stk.pop()
            temp = control_stk[-1]
            control_stk.pop()
            control_stk.pop()
            control_stk.append(temp)
            stack_stk.pop()
        else:
            print("Expect a boolean")
            raise RuntimeError("Error")
    else:
        print(f"Unknown type {type_}")
        raise RuntimeError("Error")

def cse():
    control_structures.append([])
    pre_order_traversal(ast_bu[-1], 0)
    parsing_env.append(Base("environment"))
    parsing_env[-1].prev = None
    add_in_built_to_env(parsing_env[-1])
    add_func_to_control(parsing_env[-1], 0)
    # print(control_stk[-1])
    while len(control_stk) > 1:
        the_type = control_stk[-1].type
        rules(the_type)
    # if stack_stk and control_stk and stack_stk[-1] != control_stk[-1]:
    #     print("Run time Error")
    #     raise Exception("Run time Error")
    # if stack_stk:
    #     temp = stack_stk.pop()
    #     print("Final result:", temp)
    # print_control_structures()
