# class Node:
#     def __init__(self, token):
#         self.token = token
#         self.children = []
#
# # Global AST stack
# ast_bu = []

from nodes import Node , ast_stack as ast_bu

def standardizer():
    standardize_tree(ast_bu[-1])

def standardize_tree(node):
    for child in node.children:
        standardize_tree(child)
    standardize(node)


def standardize(node):
    if node.label == "let":
        if node.children[0].label == "=":
            X = node.children[0].children[0]
            E = node.children[0].children[1]
            P = node.children[1]
            new_node = Node("gamma")
            lam = Node("lambda")
            lam.children.extend([X, P])
            new_node.children.extend([lam, E])
            copy_node(node, new_node)
        else:
            raise SyntaxError("Syntax error during standardizing")

    elif node.label == "fcn_form":
        size = len(node.children)
        temp_head = node.children[-1]
        for i in range(size - 2, 0, -1):
            lam = Node("lambda")
            lam.children.extend([node.children[i], temp_head])
            temp_head = lam
        equal = Node("=")
        equal.children.extend([node.children[0], temp_head])
        copy_node(node, equal)

    elif node.label == "where":
        if node.children[1].label == "=":
            P = node.children[0]
            X = node.children[1].children[0]
            E = node.children[1].children[1]
            new_node = Node("gamma")
            lam = Node("lambda")
            lam.children.extend([X, P])
            new_node.children.extend([lam, E])
            copy_node(node, new_node)
        else:
            raise SyntaxError("Syntax error during standardizing")

    elif node.label == "within":
        if node.children[0].label == "=" and node.children[1].label == "=":
            X1 = node.children[0].children[0]
            E1 = node.children[0].children[1]
            X2 = node.children[1].children[0]
            E2 = node.children[1].children[1]

            new_node = Node("=")
            new_node.children.append(X2)

            gamma_node = Node("gamma")
            lam = Node("lambda")
            lam.children.extend([X1, E2])
            gamma_node.children.extend([lam, E1])

            new_node.children.append(gamma_node)
            copy_node(node, new_node)
        else:
            raise SyntaxError("Syntax error during standardizing")

    elif node.label == "@":
        E1, N, E2 = node.children
        new_node = Node("gamma")
        inner_gamma = Node("gamma")
        inner_gamma.children.extend([N, E1])
        new_node.children.extend([inner_gamma, E2])
        copy_node(node, new_node)

    elif node.label == "rec":
        if node.children[0].label == "=":
            X = node.children[0].children[0]
            E = node.children[0].children[1]
            equal = Node("=")
            equal.children.append(X)

            gamma_node = Node("gamma")
            gamma_node.children.append(Node("Ystar"))
            lam = Node("lambda")
            lam.children.extend([X, E])
            gamma_node.children.append(lam)

            equal.children.append(gamma_node)
            copy_node(node, equal)
        else:
            raise SyntaxError("Syntax error during standardizing")

    elif node.label == "lambda":
        size = len(node.children)
        temp_head = node.children[-1]
        for i in range(size - 1):
            lam = Node("lambda")
            lam.children.extend([node.children[i], temp_head])
            temp_head = lam
        copy_node(node, temp_head)

    elif node.label == "and":
        size = len(node.children)
        equal = Node("=")
        comma = Node(",")
        tau = Node("tau")
        for i in range(size):
            comma.children.append(node.children[i].children[0])
            tau.children.append(node.children[i].children[1])
        standardize_tree(tau)
        equal.children.extend([comma, tau])
        copy_node(node, equal)

def standardize_tree_list(node):
    for child in node.children:
        standardize_tree_list(child)
    if node.children and node.children[0].label == ",":
        standardize_list(node)

def standardize_list(node):
    temp_head = node.children[1]
    for i, child in enumerate(node.children[0].children):
        gamma = Node("gamma")
        lam = Node("lambda")
        inner_gamma = Node("gamma")

        lam.children.extend([Node(str(i + 1)), temp_head])
        inner_gamma.children.extend([Node("Temp"), child])
        gamma.children.extend([lam, inner_gamma])
        temp_head = gamma

    lam = Node("lambda")
    lam.children.extend([Node("Temp"), temp_head])
    copy_node(node, lam)

def copy_node(dest, src):
    dest.label = src.label
    dest.children = src.children