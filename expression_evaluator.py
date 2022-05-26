"""Module for evaluating str expressions.

Significantly influenced by 
https://stackoverflow.com/a/9558001/11472358.
"""

import ast
import operator as op

# Supported operators
OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.USub: op.neg
}


def eval_expr(expr):
    """TODO"""
    return eval_(ast.parse(expr, mode='eval').body)


def eval_(node):
    """TODO"""
    if isinstance(node, ast.Num):
        return node.n
    elif isinstance(node, ast.BinOp):
        return OPERATORS[type(node.op)](eval_(node.left), eval_(node.right))
    elif isinstance(node, ast.UnaryOp):
        return OPERATORS[type(node.op)](eval_(node.operand))
    else:
        raise TypeError("Encountered value that was not a number or operator "
                        "when parsing weight expression. Did you reference a "
                        "categorical attribute?")
