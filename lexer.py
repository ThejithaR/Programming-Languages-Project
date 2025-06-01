import re

# class Token:
#     def __init__(self, type_, value):
#         self.type = type_
#         self.value = value
#     def __repr__(self):
#         return f"Token({self.type}, {repr(self.value)})"
#
# tokens = []

from nodes import Token , tokens

def is_letter(c):
    return c.isalpha()

def is_digit(c):
    return c.isdigit()

def is_space(c):
    return c in ' \t\n'

def is_operator(c):
    operators = {'+', '-', '*', '<', '>', '&', '.', '@', '/', ':', '=', '~', '|',
                 '$', '!', '#', '%', '^', '_', '[', ']', '{', '}', '"', '`', '?'}
    return c in operators



def is_punction(c):
    return c in "();:,"

def add_space(buffer, c):
    if c == ' ':
        return buffer + "\\s"
    elif c == '\t':
        return buffer + "\\t"
    elif c == '\n':
        return buffer + "\\n"
    return buffer


def screener():
    global tokens
    new_tokens = []
    for token in tokens:
        if token.type == "EOF":
            new_tokens.append(token)
            break
        elif token.type != "comment" and token.type != "space":
            new_tokens.append(token)
    tokens.clear()
    tokens.extend(new_tokens)


def scanner(input_string):
    global tokens
    input_string += '\n'
    index = 0
    length = len(input_string)

    while index < length:
        c = input_string[index]
        index += 1

        # Identifier
        if is_letter(c):
            buffer = c
            while index < length and (is_letter(input_string[index]) or is_digit(input_string[index]) or input_string[index] == '_'):
                buffer += input_string[index]
                index += 1
            tokens.append(Token("identifier", buffer))

        # Integer
        elif is_digit(c):
            buffer = c
            while index < length and is_digit(input_string[index]):
                buffer += input_string[index]
                index += 1
            tokens.append(Token("integer", buffer))

        # String
        elif c == '\'':
            buffer = c
            while index < length:
                c = input_string[index]
                index += 1
                if c == '\\':
                    buffer += c
                    c = input_string[index]
                    index += 1
                    if c in ('t', 'n', '\\'):
                        buffer += c
                    elif c == '\'' and index < length and input_string[index] == '\'':
                        buffer += "''"
                        index += 1
                    else:
                        raise Exception(f"Unknown escape sequence: \\{c}")
                elif c == '\'':
                    buffer += c
                    tokens.append(Token("string", buffer))
                    break
                elif c in (' ',) or is_digit(c) or is_letter(c) or is_operator(c) or is_punction(c):
                    buffer += c

        # Space
        elif is_space(c):
            buffer = add_space("", c)
            while index < length and is_space(input_string[index]):
                buffer = add_space(buffer, input_string[index])
                index += 1
            tokens.append(Token("space", buffer))

        # Comment or Operator
        elif is_operator(c):
            if c == '/' and index < length and input_string[index] == '/':
                index += 1
                buffer = "//"
                while index < length and input_string[index] != '\n':
                    buffer += input_string[index]
                    index += 1
                buffer += "\\n"
                index += 1
                tokens.append(Token("comment", buffer))
            else:
                buffer = c
                while index < length and is_operator(input_string[index]):
                    buffer += input_string[index]
                    index += 1
                tokens.append(Token("operator", buffer))

        # Punctuation
        elif is_punction(c):
            tokens.append(Token(c, c))

    tokens.append(Token("EOF", "EOF"))

# code = '''let check_pos (y) = Print((fn f. f (y)) (fn x. x ls 0 -> 'negative' | 'positive'))
# in check_pos (-3)'''
# scanner(code)
# for token in tokens:
#     print(token)

# screener()
# print("After Screener")
# for token in tokens:
#     print(token)