"""Module for evaluating str expressions.

Significantly influenced by 
https://stackoverflow.com/a/9558001/11472358.
"""

import ast
import operator as op

# Supported operators
OPERATORS = {
    "Add": op.add,
    "Sub": op.sub,
    "Mult": op.mul,
    "Div": op.truediv,
    "USub": op.neg
}

# Supported functions
FUNCTIONS = {
    "abs": op.abs
}


def eval_expr(expr):
    """Evaluate str expression consisting of constants and arithmetic.

    :param expr: AST node containing simple arithmetic and constants
    :type expr: str
    :return: Evaluated value of expr
    :rtype: str
    """
    return eval_(ast.parse(expr, mode='eval').body)


def eval_(node):
    """Parse leaf AST nodes sent from ``eval_expr``.

    :param node: AST node
    :type node: ast.AST
    :return: Evaluation of leaf node
    :rtype: str
    """
    if isinstance(node, ast.Num):
        return node.n
    elif isinstance(node, ast.BinOp):
        operator = OPERATORS[type(node.op).__name__]
        return operator(eval_(node.left), eval_(node.right))
    elif isinstance(node, ast.UnaryOp):
        operator = OPERATORS[type(node.op).__name__]
        return operator(eval_(node.operand))
    # ``func`` could be ast.Name or ast.Attribute
    elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
        fn = FUNCTIONS[node.func.id]
        return fn(*[eval_(e) for e in node.args])
    else:
        raise TypeError("Encountered value that was not a number or operator "
                        "when parsing weight expression. Did you reference a "
                        "categorical attribute?")
