from lexer import Lexer
from parsing import Parser
import pdb

# To add new operations add the operator to the lexer symbol
# table, create the operator token type and it's handler

while True:
    text = input(">> ")
    lexer = Lexer(text)
    tokens = list(lexer.generate_tokens())

    print(tokens)

    parser = Parser(list(tokens))
    parser.parse()
