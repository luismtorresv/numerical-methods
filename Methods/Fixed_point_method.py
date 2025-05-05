import pandas as pd
import sympy as sp


def fixed_point_method(a, b, X0, Tol, type_of_tol, Niter, Fun, Fun_g):
    # Check the G function
    x_sym = sp.symbols("x")
    try:
        g_expr = sp.sympify(Fun_g.replace("^", "**"))
    except (sp.SympifyError, SyntaxError) as e:
        raise ValueError(f"Invalid expression: {e}")
    g_func = sp.lambdify(x_sym, g_expr, modules=["math"])

    # Initialise lists for table
    iterations = []
    xn = []
    fn = []
    errors = []

    # First iteration
    x = X0
    f = Fun(x)
    c = 0
    error = 100  # Initial error (arbitrary)

    iterations.append(c)
    xn.append(x)
    fn.append(f)
    errors.append(error)

    while error > Tol and f != 0 and c < Niter:
        x = g_func(x)  # New approximation using g(x)

        # Validate new approximation in interval [a, b]
        if x < a or x > b:
            print(
                f"Error: Iteration #{c} resulted in a value outside of the interval [{a}, {b}]."
            )
            break

        f = Fun(x)  # We evaluate f(x)

        c += 1
        if type_of_tol == "D.C":
            error = abs(x - xn[-1])  # Absolute error
        else:
            error = abs((x - xn[-1]) / x)  # Relative error

        # Store values in lists
        iterations.append(c)
        xn.append(x)
        fn.append(f)
        errors.append(error)

    # Show final results

    # Create and show iterations and errors
    table = pd.DataFrame(
        {"Iteración": iterations, "Xn": xn, "f(Xn)": fn, "Error": errors}
    )

    if f == 0:
        # print(f"{x} is a root of f(x).")
        return table, x
    elif error < Tol:
        # print(f"{x} is an approximation of a root of f(x) with tolerance {Tol}.")
        return table, x
    else:
        # print(f"Method failed in {Niter} iterations.")
        return None, Niter
