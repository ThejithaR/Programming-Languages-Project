# myrpal.py

from lexer import scanner, screener
from grammar import parser
from nodes import print_ast, print_tokens
import sys

tokens = []           # List of Token objects (global like in C++)
dt_bu = []            # Derivation tree (strings)
ast_stack = []        # AST bottom-up stack (list used like a stack)

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
        tokens = scanner(input_code)
        print_tokens()  # Optional for debugging
        tokens = screener(tokens)
        # print_tokens()  # Optional for debugging

        # Parser
        ast = parser(tokens)

        if tree_flag:
            print_ast()
            return
        

        # Placeholder for standardizer
        # standardizer(ast)

        # Placeholder for CSE machine
        # cse(ast)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
