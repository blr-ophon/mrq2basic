from lexer import Lexer
from parsing import Parser
import pdb

while True:
    text = input(">> ")
    lexer = Lexer(text)
    tokens = list(lexer.generate_tokens())

    print(tokens)

    parser = Parser(list(tokens))
    parser.parse()
