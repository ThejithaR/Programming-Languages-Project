from lexer import scanner , screener
from nodes import tokens , print_ast , print_tokens , print_tree
from grammar import parser

code = '''let rec f n = n eq 1 -> 0 | n eq 2 -> 1 | f (n-1) + f (n-2) in
let rec fib n = n eq 0 -> nil | (fib (n-1) aug f (n)) in
Print ( fib 5 )'''
scanner(code)
screener()
# for token in tokens:
#     print(token)
parser(tokens)

# print(parser(tokens))
# print("Hello")
print_ast()
# print_tokens()
# print_tree()
# print(tokens)