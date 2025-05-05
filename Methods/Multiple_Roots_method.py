import pandas as pd
import sympy as sp


def Newton_method(X0, Tol, type_of_tol, Niter, Fun, df):
    # Check the derivative of the function
    x_sym = sp.symbols("x")
    try:
        df = sp.sympify(df.replace("^", "**"))
    except (sp.SympifyError, SyntaxError) as e:
        raise ValueError(f"Invalid expression: {e}")
    df = sp.lambdify(x_sym, df, modules=["math"])

    # Initialise lists for table
    iterations = []
    xn_vals = []
    fn_vals = []
    df_vals = []
    errors = []

    # First iteration
    x = X0
    f = Fun(x)
    derivative = df(x)
    c = 0
    Error = 100  # Initial arbitrary error

    iterations.append(c)
    xn_vals.append(x)
    fn_vals.append(f)
    df_vals.append(derivative)
    errors.append(Error)

    # Newton-Raphson algorithm
    while Error > Tol and f != 0 and derivative != 0 and c < Niter:
        x = x - m * f / derivative
        derivative = df(x)
        f = Fun(x)

        c += 1
        if type_of_tol == "D.C":
            Error = abs(x - xn_vals[-1])  # Absolute error
        else:
            Error = abs((x - xn_vals[-1]) / xn_vals[-1])  # Relative error

        # Store values in lists
        iterations.append(c)
        xn_vals.append(x)
        fn_vals.append(f)
        df_vals.append(derivative)
        errors.append(Error)

    # Show final results
    # Create and show iterations table
    table = pd.DataFrame(
        {
            "Iteración": iterations,
            "Xn": xn_vals,
            "f(Xn)": fn_vals,
            "f'(Xn)": df_vals,
            "Error": errors,
        }
    )

    if f == 0:
        # print(f"{x} is a root of f(x)")
        return table, x
    elif Error < Tol:
        # print(f"{x} is an approximation of a root of f(x) with tolerance {Tol}.")
        return table, x
    else:
        # print(f"Method failed in {Niter} iterations.")
        return None, Niter
