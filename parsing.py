from collections import deque
from tokens import TokenType
from nodes import ASTNode


class Parser:
    """Parse tokens into nodes"""
    def __init__(self, tokens):
        self.tokens_it = iter(tokens)
        self.crntToken = None
        self.advance()

    def parse(self):
        """Parse infix tokens to Abstract Syntax Tree"""
        postFix = self.toPostfix()
        print(postFix)
        ASTRoot = self.toASTree(postFix)
        return ASTRoot

    def advance(self):
        """Get next token"""
        try:
            self.crntToken = next(self.tokens_it)
        except StopIteration:
            self.crntToken = None

    @staticmethod
    def getTopPreced(opStack):
        """Return precedence of token on top of the operation stack"""
        if not opStack:
            return None
        return opStack[-1].preced

    def toPostfix(self):
        """Convert infix tokens to postfix order by Shunting Yard Algorithm"""
        opStack = deque()       # Stack of operation tokens
        postFix = deque()       # Tokens in postfix order

        while self.crntToken is not None:

            if self.crntToken.type == TokenType.NUMBER:
                postFix.append(self.crntToken)

            elif self.crntToken.type == TokenType.LPAREN:
                opStack.append(self.crntToken)

            elif self.crntToken.type == TokenType.RPAREN:
                top_item = opStack.pop() if opStack else None
                # Pop from stack to output until left parenthesis is found
                while top_item and top_item.type != TokenType.LPAREN:
                    postFix.append(top_item)
                    top_item = opStack.pop() if opStack else None

            elif self.crntToken.isOperator:
                topPreced = self.getTopPreced(opStack)
                while topPreced and topPreced < self.crntToken.preced:
                    # Left parenthesis must have max precedence for this to work 
                    topToken = opStack.pop()
                    if topToken.type != TokenType.LPAREN:
                        postFix.append(topToken)
                    topPreced = self.getTopPreced(opStack)

                opStack.append(self.crntToken)

            self.advance()

        while len(opStack) > 0:
            postFix.append(opStack.pop())

        return postFix

    def parseASTNodes(self, postFixTokens, parentNode):
        """Parse nodes to AST recursively"""

        if not postFixTokens:
            return

        # Right child
        rToken = postFixTokens.pop()
        rNode = ASTNode(rToken)
        if rToken.isOperator:
            self.parseASTNodes(postFixTokens, rNode)
        parentNode.rChild = rNode

        if not postFixTokens:
            self.raise_error()
            return
        if parentNode.Token.operands_n < 2:
            # Parent node has only one child. Right one
            return

        # Left child
        lToken = postFixTokens.pop()
        lNode = ASTNode(lToken)
        if lToken.isOperator:
            self.parseASTNodes(postFixTokens, lNode)
        parentNode.lChild = lNode


    def toASTree(self, postFixTokens):
        """Postfix notation to Abstract Syntax Tree"""

        if not postFixTokens:
            return None

        topToken = postFixTokens.pop()
        rootNode = ASTNode(topToken)
        if topToken.isOperator:
            self.parseASTNodes(postFixTokens, rootNode)

        return rootNode

    def raise_error(self):
        """Generic error handling"""
        raise Exception("Invalid Syntax")
