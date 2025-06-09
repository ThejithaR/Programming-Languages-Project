# myrpal.py
'''
Group name : 44 65 62 75 67 20 6D 65 20 67 65 6E 74 6C 79
Members : 
        220008E - Abeyrathna A.H.M.R.T.
        220122X - Dilmina K.M.S.
'''

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
    standardized_flag = len(sys.argv) > 2 and sys.argv[2] == "-st"

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

        if standardized_flag:
            print_ast()
            return
        
        #CSE machine
        cse()

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()