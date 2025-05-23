import sympy as sp


def nm_lambdify(f, symbol):
    return sp.lambdify(symbol, sp.sympify(f), "numpy")
