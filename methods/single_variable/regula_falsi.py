import pandas as pd


def regula_falsi(a, b, niter, tol, tolerance_type, function):
    table = []
    row = {}
    Error = (
        "Relative Error"
        if tolerance_type == "Significant Figures"
        else "Absolute Error"
    )

    # initial call
    row["a"] = a
    row["b"] = b
    row["x_intersect"] = (function(b) * a - function(a) * b) / (
        function(b) - function(a)
    )
    row["f(a)"] = function(a)
    row["f(x_intersect)"] = function(
        (function(b) * a - function(a) * b) / (function(b) - function(a))
    )
    row["f(b)"] = function(b)
    row[Error] = None
    table.append(row)

    err = 100

    if function(a) * function(b) > 0:
        return {
            "status": "error",
            "message": "Invalid Arguments, the function does not change sign in the interval.",
        }
    else:
        x_intersect = (function(b) * a - function(a) * b) / (function(b) - function(a))
        iter = 0
        while iter < niter and err > tol:
            if function(a) == 0:
                return table
            if function(a) * function(x_intersect) < 0:
                b = x_intersect
            else:
                a = x_intersect

            iter += 1
            old_intersect = x_intersect
            x_intersect = (function(b) * a - function(a) * b) / (
                function(b) - function(a)
            )

            row = {}
            row["a"] = a
            row["x_intersect"] = x_intersect
            row["b"] = b
            row["f(a)"] = function(a)
            row["f(x_intersect)"] = function(x_intersect)
            row["f(b)"] = function(b)

            if Error == "Relative Error":
                row[Error] = abs((x_intersect - old_intersect) / x_intersect)
            else:
                row[Error] = abs(x_intersect - old_intersect)
            table.append(row)

            err = row[Error]

        df = pd.DataFrame(table)
        return {"status": "success", "table": df}
