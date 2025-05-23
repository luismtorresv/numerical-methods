import sympy as sp


def string_to_function(expr_str, variables):
    expr = sp.sympify(expr_str)
    return expr


def function_input(var="x"):
    expression = input("Expression: ")
    variables = sp.symbols(var)
    f = string_to_function(expression, variables)
    print(sp.latex(f))


function_input()
