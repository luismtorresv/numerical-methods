import numpy as np
import pandas as pd


def multiple_roots(x0, niter, tol, function, df, d2f, tolerance_type):
    table = []
    xi = x0
    for i in range(niter):
        fx = function(xi)
        dfx = df(xi)
        d2fx = d2f(xi)

        if dfx == 0:
            return {
                "status": "error",
                "message": "The first derivative is equal to 0. The method is not applicable.",
            }

        # Fórmula del método
        xi_next = xi - (fx * dfx) / (dfx**2 - fx * d2fx)
        error = abs(xi_next - xi)

        # Guarda resultados de la iteración
        table.append([i + 1, xi, fx, dfx, d2fx, xi_next, error])

        # Verifica si se cumple la tolerancia
        if tolerance_type == "Significant Figures":
            if error < tol:
                break
        elif tolerance_type == "Correct Decimals":
            if round(error, int(-np.log10(tol))) == 0:
                break

        xi = xi_next

    return {
        "status": "success",
        "table": pd.DataFrame(
            table,
            columns=["Iteration", "x_i", "f(x)", "f'(x)", "f''(x)", "x_(i+1)", "Error"],
        ),
    }
