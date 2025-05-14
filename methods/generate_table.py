import pandas as pd


def generate_table(x0, niter, method, function, args):
    table = []
    row = {}

    # initial call
    initial = method(args)
    row["iter"] = 0
    row["xn"] = x0
    row["f(n)"] = function(initial["result"])
    row["abs_err"] = 0
    row["rel_err"] = 0
    table.append(row)

    iter = 1
    while iter < niter:
        row = {}
        res = method(args)
        row["iter"] = iter
        row["xn"] = res["result"]
        row["f(n)"] = function(res["result"])
        row["abs_err"] = abs(row["xn"] - table[iter - 1]["xn"])
        args = res["args"]

        if res["finish"]:
            table.append(row)
            return pd.DataFrame(table)

        table.append(row)
        iter += 1

    return pd.DataFrame(table)


def generate_table2(x0, niter, method, function):
    table = []
    row = {}

    # initial call
    args = {"x0": x0, "funtion": function, "niter": 1}
    initial = method(args)
    row["iter"] = 0
    row["xn"] = x0
    row["f(n)"] = function(initial["result"])
    row["abs_err"] = 0
    row["rel_err"] = 0
    table.append(row)

    iter = 1
    while iter < niter:
        res = method(args)
        row["iter"] = iter
        row["xn"] = res["result"]
        row["f(n)"] = function(res["result"])
        row["abs_err"] = abs(row["xn"] - table[iter - 1]["xn"])
        args = res[args]
    table.append(row)

    df = pd.DataFrame(table)
