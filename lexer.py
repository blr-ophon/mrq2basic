from tokens import Token, TokenType
import pdb

WHITESPACE = " \n\t"
DIGITS = ".0123456789"
OPERATORS_1 = "+-"
OPERATORS_2 = "*/"
PARENTHESIS = "()"


class Lexer:
    """Parse math operation strings"""

    def __init__(self, text):
        self.text = iter(text)      # Text Iterator
        self.current_char = None
        # Get first char
        self.advance()

    def advance(self):
        """Save current char and advance iterator to next one"""
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

            elif self.current_char in OPERATORS_1:
                op_token = Token(TokenType.OPERATOR, self.current_char, preced=1)
                self.advance()
                yield op_token

            elif self.current_char in OPERATORS_2:
                op_token = Token(TokenType.OPERATOR, self.current_char, preced=2)
                self.advance()
                yield op_token

            elif self.current_char in PARENTHESIS:
                op_token = Token(TokenType.PAREN, self.current_char, preced=3)
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
            # breakpoint()
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
