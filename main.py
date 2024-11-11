from lexer import Lexer
import pdb

while True:
    text = input(">> ")
    lexer = Lexer(text)
    tokens = lexer.generate_tokens()
    print(list(tokens))
