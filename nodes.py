from dataclasses import dataclass


@dataclass
class NumberNode:
    value: float

    def __repr__(self):
        return f"{self.value}"


@dataclass
class OperationNode:
    operator: any
    node_l: any = None
    node_r: any = None

    def __repr__(self):
        return f"({self.node_l}+{self.node_r}"
