import numpy as np
import sympy as sp


def vandermonde(x, y, decimals, x_sym=sp.symbols("x")):
    A = np.vander(x, increasing=False)
    coeffs = np.linalg.solve(A, y)
    rounded_coefficients = np.round(coeffs, decimals)

    poly = 0
    poly_rounded = 0

    degree = len(coeffs) - 1
    for i, coeff in enumerate(coeffs):
        poly += coeff * x_sym ** (degree - i)
        poly_rounded += rounded_coefficients[i] * x_sym ** (degree - i)

    return coeffs, rounded_coefficients, poly, poly_rounded
