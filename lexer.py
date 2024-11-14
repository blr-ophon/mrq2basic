from tokens import Token, TokenType
import pdb

# TODO: Accept multiple char operators

WHITESPACE = " \n\t"
DIGITS = ".0123456789"
# Special Case. Behave as unary or binary depending on the expression
SC_OPERATORS = "-+"
MAX_PRECED = 15


class Lexer:
    """Parse math operation strings"""

    opSymbolTable = {
        # (Type, precedence, number of operands)

        # Binary operators
        "*": (TokenType.OP_MULTIPLY, 3, 2),
        "/": (TokenType.OP_DIVIDE, 3, 2),
        "%": (TokenType.OP_MODULUS, 3, 2),
        "+": (TokenType.OP_ADD, 4, 2),
        "-": (TokenType.OP_MINUS, 4, 2),
        "&": (TokenType.OP_AND, 8, 2),
        "|": (TokenType.OP_OR, 9, 2),
        # Unitary operators
        "u+": (TokenType.OP_UN_ADD, 3, 1),
        "u-": (TokenType.OP_UN_MINUS, 3, 1),
        "!": (TokenType.OP_NOT, 2, 1),
    }

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

    def symbolToToken(self, key):
        """If key is in the Symbol table, returns a token, else returns None"""
        (opType, opPreced, opOperands) = self.opSymbolTable.get(key, (None, None, None))
        if opType is None:
            # Not a Symbol
            return None

        op_token = Token(opType, key, opPreced, True, opOperands)
        return op_token

    def isOperator(self, key):
        """Check if opString is an operator in the symbol table"""
        # For code clarity
        if self.symbolToToken(key):
            return True
        return False

    def generate_tokens(self):
        """Yield a generator with numbers and operators tokens"""
        while self.current_char is not None:

            if self.current_char in WHITESPACE:
                # Skip whitespaces in texts
                self.advance()

            elif self.current_char in DIGITS:
                yield self.generate_number()
            # TODO: Create generate_operator() method for symbols like ++ and --

            # Special case operators. Behave as unary or binary depending on
            # the expression. For these, unary case has higher precedence, so
            # must be checked first. The unary case is identified in the symbol
            # table by prepending 'u'
            elif self.current_char in SC_OPERATORS and self.isOperator(self.previous_char):
                op_token = self.symbolToToken("u"+self.current_char)
                self.advance()
                yield op_token

            elif self.isOperator(self.current_char):
                op_token = self.symbolToToken(self.current_char)
                self.advance()
                yield op_token

            elif self.current_char == "(":
                op_token = Token(TokenType.LPAREN, self.current_char, preced=MAX_PRECED)
                self.advance()
                yield op_token

            elif self.current_char == ")":
                op_token = Token(TokenType.RPAREN, self.current_char, 0)
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
