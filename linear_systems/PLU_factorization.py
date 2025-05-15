import numpy as np
import pandas as pd
import sympy as sp

from .matrix_helpers import back_substitution, forward_substitution


def PLU_factorization(A):
    A = A.copy().astype(float)
    n = len(A)
    i = 0

    L = np.eye(n).astype(float)
    P = np.eye(n).astype(float)

    while i < n:
        P_new = np.eye(n)
        swap_index = np.argmax(np.abs(A[i:, i])) + i

        if A[swap_index][i] == 0:
            return {
                "status": "error",
                "message": "The matrix cannot be decomposed as it is singular.",
            }

        if swap_index != i:
            swap_row = A[i].copy()
            A[i] = A[swap_index]
            A[swap_index] = swap_row

            P_new[i][i] = 0
            P_new[swap_index][swap_index] = 0
            P_new[swap_index][i] = 1
            P_new[i][swap_index] = 1

            P = P_new @ P

        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            A[j] = A[j] - factor * A[i]
            A[j][i] = 0
            L[j][i] = factor
        i += 1

    return {"status": "success", "U": A, "L": L, "P": P}


def solve_PLU(P, L, U, b):
    y = forward_substitution(L, np.dot(P, b))
    x = back_substitution(U, y)
    return x
