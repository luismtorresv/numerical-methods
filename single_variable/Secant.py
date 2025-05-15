import pandas as pd


def secant(x0, x1, niter, tol, function, tolerance_type):
    table = []

    # Initial setup
    xn = x1 - function(x1) * (x1 - x0) / (function(x1) - function(x0))
    x_prev = x1
    x_prev2 = x0
    err = 100
    iter = 0

    Error = (
        "Relative Error"
        if tolerance_type == "Significant Figures"
        else "Absolute Error"
    )

    # First iteration (iteration 0)
    row = {"x_{n-1}": x0, "x_n": x1, "f(x_n)": function(x1), f"{Error}": None}
    table.append(row)

    # Secant method iterations
    while iter < niter and err >= tol:
        # Update xn
        xn = x_prev - function(x_prev) * (x_prev - x_prev2) / (
            function(x_prev) - function(x_prev2)
        )

        # Calculate error based on tolerance type
        if tolerance_type == "Significant Figures":
            # Calculate relative error
            err = abs((xn - x_prev) / xn)
        elif tolerance_type == "Correct Decimals":
            # Calculate absolute error
            err = abs(xn - x_prev)

        # Append row for current iteration
        row = {"x_{n-1}": x_prev, "x_n": xn, "f(x_n)": function(xn), f"{Error}": err}
        table.append(row)

        iter += 1
        x_prev2 = x_prev
        x_prev = xn

    # Convert table to DataFrame and return
    df = pd.DataFrame(table)
    return {"status": "success", "table": df}
