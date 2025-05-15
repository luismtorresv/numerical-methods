import pandas as pd


def bisection(a, b, niter, tol, tolerance_type, function):
    if b < a:
        return {
            "status": "error",
            "message": "Invalid Arguments, b must be greater than a.",
        }

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
    row["mid"] = (a + b) / 2
    row["f(a)"] = function(a)
    row["f(mid)"] = function((a + b) / 2)
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
        mid = (a + b) / 2
        iter = 0
        while iter < niter and err > tol:
            if function(a) * function(mid) <= 0:
                b = mid
            else:
                a = mid
            iter += 1
            prev_mid = mid
            mid = (a + b) / 2

            row = {}
            row["a"] = a
            row["b"] = b
            row["mid"] = mid
            row["f(a)"] = function(a)
            row["f(mid)"] = function(mid)
            row["f(b)"] = function(b)
            if Error == "Relative Error":
                row[Error] = abs((mid - prev_mid) / mid)
            else:
                row[Error] = abs(mid - prev_mid)
            err = row[Error]
            table.append(row)

        df = pd.DataFrame(table)
        return {"status": "success", "table": df}
