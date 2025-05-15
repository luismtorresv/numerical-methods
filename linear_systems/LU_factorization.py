import numpy as np

from .matrix_helpers import back_substitution, forward_substitution


def LU_factorization(A):
    A = A.copy().astype(float)
    n = len(A)
    i = 0

    L = np.eye(n)

    while i < n:
        current_value = A[i][i]
        if current_value == 0:
            return {
                "status": "error",
                "message": "The matrix cannot be decomposed without permuting rows or is singular.",
            }

        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            A[j] = A[j] - factor * A[i]
            A[j][i] = 0
            L[j][i] = factor
        i += 1
    return {"status": "success", "U": A, "L": L}


def solve_LU(L, U, b):
    y = forward_substitution(L, b)
    x = back_substitution(U, y)
    return x
