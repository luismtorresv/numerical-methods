import numpy as np
import sympy as sp


def string_to_function(expr_str, variables):
    expr = sp.sympify(expr_str)
    return expr


def string_to_lambda(
    variables,
    expr,
):
    func = sp.lambdify(variables, expr, "numpy")
    return func


def function_input(var="x"):
    expression = input("Expression: ")
    variables = sp.symbols(var)
    f = string_to_function(expression, variables)
    print(sp.latex(f))


function_input()
