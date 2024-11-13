from dataclasses import dataclass


@dataclass
class ASTNode:
    Token: any
    lChild: any = None
    rChild: any = None

    def __repr__(self):
        return str(self.Token)
        # return f"{self.lChild}   {self.rChild}"
