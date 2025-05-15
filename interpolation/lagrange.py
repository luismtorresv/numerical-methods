import numpy as np
import sympy as sp


def lagrange(x, y, decimals, x_sym=sp.symbols("x")):
    n = len(x)
    pol = 0
    pol_rounded = 0

    for i in range(n):
        Li = 1
        den = 1

        for j in range(n):
            if j != i:
                Li *= x_sym - x[j]
                den *= x[i] - x[j]

        # Add to the unrounded polynomial
        pol += y[i] * Li / den

    # Simplifying the rounded polynomial and maintaining decimals
    pol_rounded_decimal = sp.N(pol, decimals)

    # Expand the polynomial expressions
    newton_poly_expr_unrounded = sp.expand(pol)
    newton_poly_expr_rounded = sp.N(sp.expand(pol), decimals)

    return (
        pol,
        pol_rounded_decimal,
        newton_poly_expr_unrounded,
        newton_poly_expr_rounded,
    )
