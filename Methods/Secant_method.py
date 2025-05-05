import math

import pandas as pd


def secant_method(x0, x1, tol, max_iter, Fun):
    data = []

    for i in range(max_iter):
        x = x0
        fx0 = eval(Fun)
        x = x1
        fx1 = eval(Fun)
        den = abs(fx1 - fx0)
        if den < 1e-10:  # Try to prevent division by zero errors
            break

        x2 = x1 - fx1 * (x1 - x0) / (fx1 - fx0)
        error = abs(x2 - x1)

        data.append([i + 1, x1, fx1, error])

        if error < tol:
            break

        x0, x1 = x1, x2

    # Create table for results
    table = pd.DataFrame(data, columns=["Iteración", "xi", "f(xi)", "Error"])
    print(table.to_string(index=False))

    if fx1 == 0:
        s = x1
        text = f"{s} is a root of f(x)"
        return table, s, text
    elif den == 0:
        text = "There's likely a multiple root"
        return table, s, text
    elif error < tol:
        s = x
        text = f"{s} is an approximation of a root of f(x) with tolerance {tol}, found in iteration #{i}"
        return table, s, text
    else:
        s = x
        print(f"Method failed in {max_iter} iterations.")
