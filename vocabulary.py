# ---- Character Classifications ----

def is_letter(char):
    return char.isalpha()

def is_digit(char):
    return char.isdigit()

def is_space(char):
    return char in {' ', '\t', '\n'}

def is_operator_char(char):
    return char in OPERATOR_SYMBOLS

def is_punctuation(char):
    return char in PUNCTUATION

# ---- Token-Level Classifications ----

def is_reserved(token):
    return token in RESERVED_WORDS

def is_binary_operator(token):
    return token in BINARY_OPERATORS

def is_unary_operator(token):
    return token in UNARY_OPERATORS


# ---- Symbol Sets ----

RESERVED_WORDS = {
    "dummy", "nil", "within", "and", "rec", "false", "true",
    "ne", "eq", "le", "ls", "ge", "gr", "not", "or",
    "aug", "where", "fn", "let", "in"
}

BINARY_OPERATORS = {
    "aug", "or", "&", "+", "-", "/", "**", "*",
    "gr", "ge", "le", "ls", "eq", "ne"
}

UNARY_OPERATORS = {
    "not", "neg"
}

OPERATOR_SYMBOLS = {
    '+', '-', '*', '<', '>', '&', '.', '@', '/', ':', '=', '~', '|', '$',
    '!', '#', '%', '^', '_', '[', ']', '{', '}', '"', '`', '?'
}

PUNCTUATION = {'(', ')', ';', ','}