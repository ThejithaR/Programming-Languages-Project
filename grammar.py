# grammar.py
from typing import List
from nodes import Token, Node, ast_stack, build_tree, dt_bu
from vocabulary import is_reserved


def parser(tokens : List[Token]) -> Node:
    global _tokens
    _tokens = tokens[:]
    E()
    if _tokens and _tokens[0].type != "EOF":
        raise SyntaxError("Unexpected tokens after parsing")
    return ast_stack[-1]


def read(expected_type, expected_value=""):
    if not _tokens:
        raise SyntaxError(f"Expected {expected_type} '{expected_value}', got EOF")

    token = _tokens.pop(0)

    if expected_value:
        if token.type != expected_type or token.value != expected_value:
            raise SyntaxError(f"Expected {expected_type} '{expected_value}', got {token.type} '{token.value}'")
    else:
        if token.type != expected_type or (token.type == "identifier" and is_reserved(token.value)):
            raise SyntaxError(f"Expected {expected_type}, got {token.type} '{token.value}'")

    if token.type == "identifier":
        build_tree(f"<ID:{token.value}>", 0)
    elif token.type == "integer":
        build_tree(f"<INT:{token.value}>", 0)
    elif token.type == "string":
        build_tree(f"<STR:{token.value}>", 0)


def next_token(expected_type, expected_value=""):
    if not _tokens:
        return False
    token = _tokens[0]
    if expected_value:
        return token.type == expected_type and token.value == expected_value
    else:
        return token.type == expected_type and not (token.type == "identifier" and is_reserved(token.value))


# Grammar Functions

def E():
    if next_token("identifier", "let"):
        read("identifier", "let")
        D()
        read("identifier", "in")
        E()
        dt_bu.append("E -> 'let' D 'in' E")
        build_tree("let", 2)
    elif next_token("identifier", "fn"):
        read("identifier", "fn")
        n = 1
        while next_token("identifier", "") or next_token("(", "("):
            Vb()
            n += 1
        read("operator", ".")
        E()
        dt_bu.append("E -> 'fn' Vb+ '.' E")
        build_tree("lambda", n)
    else:
        Ew()
        dt_bu.append("E -> Ew")


def Ew():
    T()
    if next_token("identifier", "where"):
        read("identifier", "where")
        Dr()
        dt_bu.append("Ew -> T 'where' Dr")
        build_tree("where", 2)
    else:
        dt_bu.append("Ew -> T")


def T():
    Ta()
    if next_token(",", ","):
        n = 1
        while next_token(",", ","):
            read(",", ",")
            Ta()
            n += 1
        dt_bu.append("T -> Ta ( ',' Ta )+")
        build_tree("tau", n)
    else:
        dt_bu.append("T -> Ta")


def Ta():
    Tc()
    dt_bu.append("Ta -> Tc")
    while next_token("identifier", "aug"):
        read("identifier", "aug")
        Tc()
        dt_bu.append("Ta -> Ta 'aug' Tc")
        build_tree("aug", 2)


def Tc():
    B()
    if next_token("operator", "->"):
        read("operator", "->")
        Tc()
        read("operator", "|")
        Tc()
        dt_bu.append("Tc -> B '->' Tc '|' Tc")
        build_tree("->", 3)
    else:
        dt_bu.append("Tc -> B")


def B():
    Bt()
    dt_bu.append("B -> Bt")
    while next_token("identifier", "or"):
        read("identifier", "or")
        Bt()
        dt_bu.append("B -> B 'or' Bt")
        build_tree("or", 2)


def Bt():
    Bs()
    dt_bu.append("Bt -> Bs")
    while next_token("operator", "&"):
        read("operator", "&")
        Bs()
        dt_bu.append("Bt -> Bt '&' Bs")
        build_tree("&", 2)


def Bs():
    if next_token("identifier", "not"):
        read("identifier", "not")
        Bp()
        dt_bu.append("Bs -> 'not' Bp")
        build_tree("not", 1)
    else:
        Bp()
        dt_bu.append("Bs -> Bp")


def Bp():
    A()
    ops = ["gr", ">", "ge", ">=", "ls", "<", "le", "<=", "eq", "ne"]
    for op in ops:
        if next_token("identifier", op) or next_token("operator", op):
            read("identifier" if op.isalpha() else "operator", op)
            A()
            build_tree(op if op.isalpha() else {">": "gr", ">=": "ge", "<": "ls", "<=": "le"}[op], 2)
            return
    dt_bu.append("Bp -> A")


def A():
    if next_token("operator", "+"):
        read("operator", "+")
        At()
        dt_bu.append("A -> '+' At")
    elif next_token("operator", "-"):
        read("operator", "-")
        At()
        dt_bu.append("A -> '-' At")
        build_tree("neg", 1)
    else:
        At()
        dt_bu.append("A -> At")
        while next_token("operator", "+") or next_token("operator", "-"):
            op = _tokens.pop(0).value
            At()
            dt_bu.append(f"A -> A '{op}' At")
            build_tree(op, 2)


def At():
    Af()
    dt_bu.append("At -> Af")
    while next_token("operator", "*") or next_token("operator", "/"):
        op = _tokens.pop(0).value
        Af()
        dt_bu.append(f"At -> At '{op}' Af")
        build_tree(op, 2)


def Af():
    Ap()
    if next_token("operator", "**"):
        read("operator", "**")
        Af()
        dt_bu.append("Af -> Ap '**' Af")
        build_tree("**", 2)
    else:
        dt_bu.append("Af -> Ap")


def Ap():
    R()
    dt_bu.append("Ap -> R")
    while next_token("operator", "@"):
        read("operator", "@")
        read("identifier", "")
        R()
        dt_bu.append("Ap -> Ap '@' '<identifier>' R")
        build_tree("@", 3)


def R():
    Rn()
    dt_bu.append("R -> Rn")
    while any(next_token(t, v) for t, v in [("identifier", ""), ("integer", ""), ("string", ""), ("identifier", "true"), ("identifier", "false"), ("identifier", "nil"), ("(", "("), ("identifier", "dummy")]):
        Rn()
        dt_bu.append("R -> R Rn")
        build_tree("gamma", 2)


def Rn():
    literals = ["true", "false", "nil", "dummy"]
    for val in literals:
        if next_token("identifier", val):
            read("identifier", val)
            dt_bu.append(f"Rn -> '{val}'")
            build_tree(val, 0)
            return
    if next_token("(", "("):
        read("(", "(")
        E()
        read(")", ")")
        dt_bu.append("Rn -> '(' E ')'")
        return
    for t in ["identifier", "integer", "string"]:
        if next_token(t, ""):
            read(t, "")
            dt_bu.append(f"Rn -> '<{t}>'")
            return


def D():
    Da()
    if next_token("identifier", "within"):
        read("identifier", "within")
        D()
        dt_bu.append("D -> Da 'within' D")
        build_tree("within", 2)
    else:
        dt_bu.append("D -> Da")


def Da():
    Dr()
    if next_token("identifier", "and"):
        n = 1
        while next_token("identifier", "and"):
            read("identifier", "and")
            Dr()
            n += 1
        dt_bu.append("Da -> Dr ( 'and' Dr )+")
        build_tree("and", n)
    else:
        dt_bu.append("Da -> Dr")


def Dr():
    if next_token("identifier", "rec"):
        read("identifier", "rec")
        Db()
        dt_bu.append("Dr -> 'rec' Db")
        build_tree("rec", 1)
    else:
        Db()
        dt_bu.append("Dr -> Db")


def Db():
    if next_token("(", "("):
        read("(", "(")
        D()
        read(")", ")")
        dt_bu.append("Db -> '(' D ')'")
    elif len(_tokens) > 1 and _tokens[1].value in {",", "="}:
        Vl()
        read("operator", "=")
        E()
        dt_bu.append("Db -> Vl '=' E")
        build_tree("=", 2)
    else:
        read("identifier", "")
        n = 2
        while next_token("identifier", "") or next_token("(", "("):
            Vb()
            n += 1
        read("operator", "=")
        E()
        dt_bu.append("Db -> '<identifier>' Vb+ '=' E")
        build_tree("fcn_form", n)


def Vb():
    if next_token("identifier", ""):
        read("identifier", "")
        dt_bu.append("Vb -> '<identifier>'")
    elif next_token("(", "("):
        read("(", "(")
        if next_token("identifier", ""):
            Vl()
            read(")", ")")
        else:
            read(")", ")")
            dt_bu.append("Vb -> '(' ')'")
            build_tree("()", 0)


def Vl():
    read("identifier", "")
    n = 1
    while next_token(",", ","):
        read(",", ",")
        read("identifier", "")
        n += 1
    dt_bu.append("Vl -> '<identifier>' list ','")
    if n > 1:
        build_tree(",", n)
