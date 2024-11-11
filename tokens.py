from enum import Enum
from dataclasses import dataclass
import pdb

class TokenType(Enum):
    NUMBER      =   0
    # PLUS        =   1
    # MINUS       =   2
    # MULTIPLY    =   3
    # DIVIDE      =   4
    OPERATOR    =   1
    PAREN      =   2


@dataclass
class Token:
    type: TokenType
    value: any = None

    def __repr__(self):
        return self.type.name + (f": {self.value}"
                            if self.value is not None else "")
