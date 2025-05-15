import pandas as pd
import sympy as sp


def get_derivative(f):
    x = sp.symbols("x")
    f_prime = sp.diff(f, x)
    return f_prime


def check_continuity(f, x):
    try:
        f(x)
        return True
    except:
        return False


def newton(x0, niter, tol, tolerance_type, function, derivative):
    table = []
    row = {}
    Error = (
        "Relative Error"
        if tolerance_type == "Significant Figures"
        else "Absolute Error"
    )

    # initial call
    xn = x0 - function(x0) / derivative(x0)
    x_prev = x0

    row["x_n"] = x0
    row["f(x_n)"] = function(x0)
    row["f'(x_n)"] = derivative(x0)
    row[Error] = None
    table.append(row)

    err = 100
    iter = 0

    while iter < niter and err > tol:
        iter += 1
        x_prev = xn
        xn = xn - function(xn) / derivative(xn)

        row = {}
        row["x_n"] = xn
        row["f(x_n)"] = function(xn)
        row["f'(x_n)"] = derivative(xn)
        table.append(row)

        if Error == "Relative Error":
            row[Error] = abs((xn - x_prev) / xn)
        else:
            row[Error] = abs(xn - x_prev)

        err = row[Error]

    df = pd.DataFrame(table)
    return {"status": "success", "table": df}
