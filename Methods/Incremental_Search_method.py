import math

import pandas as pd


def incremental_search_method(Xi, DeltaX, Niter, Fun):
    # Initialise lists for table
    iterations = []
    xn_vals = []
    fn_vals = []

    # Evaluate function at initial point
    x = Xi
    f = eval(Fun)
    c = 0  # Iteration counter

    # Store first iteration
    iterations.append(c)
    xn_vals.append(x)
    fn_vals.append(f)

    # Do incremental search
    while c < Niter:
        x_new = x + DeltaX
        f_new = eval(Fun)

        if f * f_new < 0:  # Change of sign => there's a root in the interval [x, x_new]
            # print(f"A change of sign was detected between {x} and {x_new}")
            break

        # Store values in lists
        c += 1
        iterations.append(c)
        xn_vals.append(x_new)
        fn_vals.append(f_new)

        # Update values
        x = x_new
        f = f_new

    # Show final results
    # Create and show iterations table
    table = pd.DataFrame(
        {
            "Iteración": iterations,
            "Xn": xn_vals,
            "f(Xn)": fn_vals,
        }
    )

    if f_new == 0:
        s = x
        text = "is a root of f(x)"
        return table, s, text
    elif f * f_new < 0:
        s = x
        text = f"There exists a root of f(x) between {x} and {x_new}"
        return table, s, text
    else:
        s = x
        text = f"Method failed in {Niter} iterations"
        return None, s, text
