from collections import deque
from tokens import TokenType
from nodes import ASTNode


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
        """Parse by Shunting Yard algorithm to Abstract Syntax Tree"""

        postFix = self.toPostfix()
        print(postFix)
        ASTRoot = self.toASTree(postFix)
        return ASTRoot

    def toPostfix(self):
        """Convert tokens to postFix order"""
        # breakpoint()
        opStack = deque()       # Stack of operation tokens
        postFix = deque()       # Tokens in postfix order

        while self.crntToken is not None:

            if self.crntToken.type == TokenType.NUMBER:
                postFix.append(self.crntToken)

            elif self.crntToken.type == TokenType.OPERATOR:
                topPreced = self.getTopPreced(opStack)
                while topPreced > self.crntToken.preced:
                    topToken = opStack.pop()
                    if topToken.type != TokenType.LPAREN:
                        postFix.append(topToken)
                    topPreced = self.getTopPreced(opStack)

                opStack.append(self.crntToken)

            elif self.crntToken.type == TokenType.LPAREN:
                opStack.append(self.crntToken)

            elif self.crntToken.type == TokenType.RPAREN:
                top_item = opStack.pop() if opStack else None
                # Pop from stack to output until left parenthesis is found
                while top_item and top_item.type != TokenType.LPAREN:
                    postFix.append(top_item)
                    top_item = opStack.pop() if opStack else None

            self.advance()

        while len(opStack) > 0:
            postFix.append(opStack.pop())

        return postFix

    def parseASTNodes(self, postFixTokens, parentNode):
        """Parse nodes to AST recursively"""

        if not postFixTokens:
            return

        rToken = postFixTokens.pop()
        rNode = ASTNode(rToken)
        if rToken.type == TokenType.OPERATOR:
            self.parseASTNodes(postFixTokens, rNode)

        lToken = postFixTokens.pop()
        lNode = ASTNode(lToken)
        if lToken.type == TokenType.OPERATOR:
            self.parseASTNodes(postFixTokens, lNode)

        parentNode.rChild = rNode
        parentNode.lChild = lNode

    def toASTree(self, postFixTokens):
        """Postfix notation to Abstract Syntax Tree"""

        if not postFixTokens:
            return None

        topToken = postFixTokens.pop()
        rootNode = ASTNode(topToken)
        if topToken.type == TokenType.OPERATOR:
            self.parseASTNodes(postFixTokens, rootNode)

        return rootNode
