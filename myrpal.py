from lexer import scanner , screener
from nodes import tokens , print_ast , print_tokens , print_tree
from grammar import parser

# code = '''let x = 3 in print x'''

code = '''let Sum(A) = Psum (A,Order A )
where rec Psum (T,N) = N eq 0 -> 0
 | Psum(T,N-1)+T N
in Print ( Sum (1,2,3,4,5) )'''

# code = '''print x where x = 4'''

scanner(code)
screener()
# for token in tokens:
#     print(token)
parser(tokens)
# print(tokens)
# print(parser(tokens))
# print("Hello")
print_ast()
# print_tokens()
# print_tree()
# print(tokens)