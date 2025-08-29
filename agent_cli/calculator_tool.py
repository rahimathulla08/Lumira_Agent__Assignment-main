import operator
from typing import Union


OPS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "x": operator.mul,
    "X": operator.mul,
    "/": operator.truediv,
}


def calculate(a: Union[int, float], op: str, b: Union[int, float]) -> Union[int, float]:
    if op not in OPS:
        raise ValueError(f"Unsupported operator: {op}")
    return OPS[op](a, b)


