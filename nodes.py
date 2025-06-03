# nodes.py

tokens = []           # List of Token objects (global like in C++)
dt_bu = []            # Derivation tree (strings)
ast_stack = []        # AST bottom-up stack (list used like a stack)


class Token:
    def __init__(self, type_, value):
        self.type = type_  # e.g., "identifier", "operator", etc.
        self.value = value

    def __repr__(self):
        return f"<{self.type}:{self.value}>"


class Node:
    def __init__(self, label, children=None):
        self.label = label          # String label for the AST node
        self.children = children or []  # List of child Node objects

    def __repr__(self, depth=0):
        indent = "." * depth
        s = f"{indent}{self.label}\n"
        for child in self.children:
            s += child.__repr__(depth + 1)
        return s


def build_tree(label, num_args):
    if len(ast_stack) < num_args:
        raise RuntimeError("AST stack underflow: not enough children for node")

    children = [ast_stack.pop() for _ in range(num_args)][::-1]  # Reverse to keep original order
    node = Node(label, children)
    ast_stack.append(node)


def print_ast():
    if not ast_stack:
        print("AST stack is empty!")
        return
    print("Abstract Syntax Tree (AST):")
    print(ast_stack[-1].__repr__())
    # print(ast_stack[-1])

def print_tokens():
    global tokens
    print("\nTokens:")
    for token in tokens:
        print(f"{token.type} : {token.value}")
        if token.type == "EOF":
            break
    print()


def print_tree():
    print("\nDerivation Tree Top Down:")
    for rule in dt_bu:
        print(rule)
    print()
