import pandas as pd


def incremental_search(xi, delta_x, niter, tol, tolerance_type, function):
    """
    Perform incremental search to find roots of a function.

    Parameters:
    xi (float): Initial guess
    delta_x (float): Step size
    niter (int): Maximum number of iterations
    tol (float): Tolerance for error
    tolerance_type (str): Type of error calculation ('Significant Figures' or 'Absolute')
    function (callable): Function to evaluate

    Returns:
    dict: Results containing status and iteration table
    """
    table = []
    row = {}
    error_type = (
        "Relative Error (%)"
        if tolerance_type == "Significant Figures"
        else "Absolute Error"
    )

    # Initial evaluation
    row["x_i"] = xi
    row["f(x_i - delta_x)"] = None
    row["f(x_i)"] = function(xi)
    row[error_type] = None
    table.append(row)

    iter = 0
    err = 100  # Initial error greater than tolerance

    while iter < niter and err > tol:
        old_xi = xi
        xi = xi + delta_x
        iter += 1

        row = {
            "x_i": xi,
            "f(x_i)": function(xi),
            "f(x_i - delta_x)": function(xi - delta_x),
        }

        # Error calculation
        if error_type == "Relative Error":
            # Prevent division by zero
            row[error_type] = abs((xi - old_xi) / (xi or 1e-10))
        else:
            row[error_type] = abs(xi - old_xi)

        table.append(row)

        err = row[error_type]

        # Check for sign change (potential root)
        if function(xi) * function(xi - delta_x) <= 0:
            break

    df = pd.DataFrame(table)

    return {
        "status": "success" if iter < niter else "maximum iterations reached",
        "table": df,
        "root_found": function(xi) * function(xi - delta_x) <= 0,
    }
