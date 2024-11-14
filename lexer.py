from tokens import Token, TokenType
import pdb

WHITESPACE = " \n\t"
DIGITS = ".0123456789"
OPERATORS = "-+*/%"
MAX_PRECED = 9

opSymbolTable = {
    "+": (TokenType.OP_ADD, 1),
    "-": (TokenType.OP_SUBTRACT, 1),
    "*": (TokenType.OP_MULTIPLY, 2),
    "/": (TokenType.OP_DIVIDE, 2),
    "%": (TokenType.OP_MODULUS, 2),
}



class Lexer:
    """Parse math operation strings"""

    def __init__(self, text: str):
        self.text = iter(text)      # Text Iterator
        self.previous_char = None
        self.current_char = None
        # Get first char
        self.advance()

    def advance(self):
        """Save current char and advance iterator to next one"""
        self.previous_char = self.current_char
        try:
            self.current_char = next(self.text)
        except StopIteration:
            self.current_char = None

    def generate_tokens(self):
        """Yield a generator with numbers and operators tokens"""
        while self.current_char is not None:

            if self.current_char in WHITESPACE:
                # Skip whitespaces in texts
                self.advance()

            elif self.current_char in DIGITS:
                yield self.generate_number()
            # TODO: Create generate_operator() method for symbols like ++ and --

            # Special Case. '-' represents 2 operations. This is unary case
            elif self.current_char == "-" and self.previous_char in OPERATORS:
                tokenType = TokenType.OP_NEG
                op_token = Token(tokenType, "neg", MAX_PRECED, True, 1)
                self.advance()
                yield op_token

            elif self.current_char in OPERATORS:
                tokenType, tokenPreced = opSymbolTable.get(self.current_char, (None, None))
                op_token = Token(tokenType, self.current_char, tokenPreced, True, 2)
                self.advance()
                yield op_token

            elif self.current_char == "(":
                op_token = Token(TokenType.LPAREN, self.current_char, preced=0)
                self.advance()
                yield op_token

            elif self.current_char == ")":
                op_token = Token(TokenType.RPAREN, self.current_char, MAX_PRECED)
                self.advance()
                yield op_token

            else:
                raise Exception(f"Invalid character: {self.current_char}")

    def generate_number(self):
        """Parse digit sequence into full number token"""
        number_str = ""

        # Count decimal points.
        dpoint_count = 0

        while self.current_char is not None and self.current_char in DIGITS:
            # Prevents parsing of 1.1.1 or 1..2
            if self.current_char == '.':
                dpoint_count += 1
                if dpoint_count > 1:
                    break

            number_str += self.current_char
            self.advance()

        if number_str.startswith('.'):
            number_str = '0' + number_str
        elif number_str.endswith('.'):
            number_str += '0'

        return Token(TokenType.NUMBER, float(number_str))
