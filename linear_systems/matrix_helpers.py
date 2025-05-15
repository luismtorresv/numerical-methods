import numpy as np


def back_substitution(A, b):
    n = len(A)
    x = np.zeros(n)

    for i in range(n - 1, -1, -1):
        x[i] = b[i]
        for j in range(i + 1, n):
            if j != i:
                x[i] -= A[i][j] * x[j]
        x[i] = x[i] / A[i][i]
    return x


def forward_substitution(A, b):
    n = len(A)
    x = np.zeros(n)

    for i in range(0, n):
        x[i] = b[i]
        for j in range(0, n):
            if j != i:
                x[i] -= A[i][j] * x[j]
        x[i] = x[i] / A[i][i]
    return x
