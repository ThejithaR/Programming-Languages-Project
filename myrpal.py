
# # myrpal.py


from lexer import scanner, screener
from grammar import parser
from nodes import print_ast, print_tokens, tokens
from standardizse import standardizer
from cse import cse
import sys


# # tokens = []           # List of Token objects (global like in C++)
# # dt_bu = []            # Derivation tree (strings)
# # ast_stack = []        # AST bottom-up stack (list used like a stack)

def read_file_to_string(filename: str) -> str:
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

def main():
    if len(sys.argv) < 2:
        print("Please provide an input file.")
        return

    input_file = sys.argv[1]
    tree_flag = len(sys.argv) > 2 and sys.argv[2] == "-ast"

    try:
        input_code = read_file_to_string(input_file)

        # Lexical Analyzer
        scanner(input_code)
        print_tokens()  # Optional for debugging
        # tokens = screener(tokens)
        screener()
        # print_tokens()  # Optional for debugging


#      Parser
        ast = parser(tokens)


        if tree_flag:
            print_ast()
            return
        
        standardizer()


#      Placeholder for CSE machine
        cse()

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

# from lexer import scanner , screener
# from nodes import tokens , print_ast , print_tokens , print_tree
# from grammar import parser
# from standardizse import standardizer
# from cse_structs import control_stk

# # code = '''let rec f n = n eq 1 -> 0 | n eq 2 -> 1 | f (n-1) + f (n-2) in
# # let rec fib n = n eq 0 -> nil | (fib (n-1) aug f (n)) in
# # Print ( fib 5 )'''

# # code = '''let Sum(A) = Psum (A,Order A )
# # where rec Psum (T,N) = N eq 0 -> 0
# # | Psum(T,N-1)+T N
# # in Print ( Sum (1,2,3,4,5) )'''

# # code = '''let f x y z = x + y + z in f 1 2 3'''
# code = '''let x = 2 in print x'''

# scanner(code)
# screener()
# # for token in tokens:
# #     print(token)
# S = parser(tokens)

# standardizer()
# cse()
# print(control_stk[1].print_element())
# #print(S)


# # print(parser(tokens))
# # print("Hello")
# # print_ast()
# # print_tokens()
# # print_tree()
# # print(tokens)



# from lexer import scanner, screener
# from grammar import parser
# from nodes import print_ast, print_tokens
# import sys
# from standardizse import standardizer
# from cse import cse


# def read_file_to_string(filename: str) -> str:
#     with open(filename, 'r', encoding='utf-8') as f:
#         return f.read()

# def main():
#     if len(sys.argv) < 2:
#         print("Please provide an input file.")
#         return

#     input_file = sys.argv[1]
#     tree_flag = len(sys.argv) > 2 and sys.argv[2] == "-ast"

#     try:
#         input_code = read_file_to_string(input_file)

#         # Lexical Analyzer
#         tokens = scanner(input_code)
#         print_tokens()  # Optional for debugging
#         tokens = screener(tokens)

#         # Parser
#         ast = parser(tokens)

#         if tree_flag:
#             print_ast()
#             return

#         # Standardize the AST
#         standardizer()

#         # Run the CSE machine
#         cse()

#     except Exception as e:
#         print(f"Error: {e}")

# if __name__ == "__main__":
#     main()


# from lexer import scanner , screener
# from nodes import tokens , print_ast , print_tokens , print_tree
# from grammar import parser
# from standardizse import standardizer
# from cse import cse


# code = '''let rec f n = n eq 1 -> 0 | n eq 2 -> 1 | f (n-1) + f (n-2) in
# let rec fib n = n eq 0 -> nil | (fib (n-1) aug f (n)) in
# Print ( fib 6 )'''

# code = '''let Sum(A) = Psum (A,Order A )
# where rec Psum (T,N) = N eq 0 -> 0
# | Psum(T,N-1)+T N
# in Print ( Sum (1,2,3,4,5) )'''


# code = '''let f x y z = x + y + z in f 1 2 3'''

# scanner(code)
# screener()


# code = '''let X=3
#      in
#    Print(X,X**2)
#    //  Prints (3,9)
# '''

# code = '''let Abs N =
#         N ls 0 -> -N | N
#    in
#    Print(Abs -3)
#    // Prints 3
# '''

# code = '''let Name = 'Dolly'
#     in Print ('Hello', Name)
# '''

# code = '''let rec f(a)= a eq 1 -> 1 |
#                         a le 0 -> 0 | 
#                                   f(a-1) + f(a-2) 
# in let rec range (a,  b) = a gr b -> 'Error' | 
#                                   a eq b -> (nil) | 
#                                             (range (a, b-1)) aug f(b)
# in let Fib_rang(a,b) = Print(range (5 ,13))
# in Fib_rang(5,13)
# '''



# code = '''let f x y z = x + y + z in f 1 2 3'''
# code = '''let x = 2 in print x'''
# code = '''(fn x. print x) 3'''


# for token in tokens:
#     print(token)



# S = parser(tokens)

# standardizer()


# standardizer()
# cse()

#print(S)


# print(parser(tokens))
# print("Hello")



# print_ast()
# cse()


# print_base()

# print_ast()

# print_tokens()
# print_tree()
# print(tokens)