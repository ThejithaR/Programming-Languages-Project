# myrpal.py

from lexer import scanner, screener
from grammar import parser
from nodes import print_ast, print_tokens, tokens
from standardizse import standardizer
from cse import cse
import sys

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
        # print_tokens()  # for debugging
        screener()

        #Parser
        ast = parser(tokens)

        if tree_flag:
            print_ast()
            return
    
        #Standardization
        standardizer()

        #CSE machine
        cse()

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()