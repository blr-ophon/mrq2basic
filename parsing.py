from collections import deque
from tokens import TokenType
from nodes import NumberNode, OperationNode

class Parser:
    """Parse tokens into nodes"""
    def __init__(self, tokens):
        self.tokens_it = iter(tokens)
        self.crntToken = None
        self.advance()

    def raise_error(self):
        raise Exception("Invalid Syntax")

    def advance(self):
        """Get next token"""
        try:
            self.crntToken = next(self.tokens_it)
        except StopIteration:
            self.crntToken = None

    @staticmethod
    def getTopPreced(opStack):
        """Return precedence of token on top of the operation stack"""
        if len(opStack) == 0:
            return 0
        return opStack[-1].preced

    def parse(self):
        # breakpoint()
        """Parse expression by Shunting Yard algorithm"""
        opStack = deque()       # Stack of operation tokens
        postFix = deque()       # Tokens in postfix order 

        while self.crntToken is not None:

            if self.crntToken.type == TokenType.NUMBER:
                postFix.append(self.crntToken)

            elif self.crntToken.type == TokenType.OPERATOR:
                topPreced = self.getTopPreced(opStack)
                while topPreced > self.crntToken.preced:
                    topToken = opStack.pop()
                    postFix.append(topToken)
                    topPreced = self.getTopPreced(opStack)

                opStack.append(self.crntToken)

            self.advance()

        while len(opStack) > 0:
            postFix.append(opStack.pop())

        print(postFix)
