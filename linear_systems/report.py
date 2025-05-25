import pandas as pd
import streamlit as st

SOR_OMEGA_1 = 1
SOR_OMEGA_2 = 0.5
SOR_OMEGA_3 = 1.5


def generate_report(matrix_A, vector_b, x_0, tol, niter, norm_value, tolerance_type):
    st.subheader("Method comparison report")

    from linear_systems.gauss_seidel import gauss_seidel_method
    from linear_systems.jacobi import jacobi_method
    from linear_systems.sor import sor_method

    with st.form("report"):
        submitted = st.form_submit_button("Generate report")
    if submitted:
        results = {
            "Jacobi": jacobi_method(
                matrix_A,
                vector_b,
                x_0,
                tol,
                niter,
                norm_value,
                tolerance_type,
            ),
            "Gauss-Seidel": gauss_seidel_method(
                matrix_A,
                vector_b,
                x_0,
                tol,
                niter,
                norm_value,
                tolerance_type,
            ),
            # Relaxation Factor = 1
            "SOR-1": sor_method(
                matrix_A,
                vector_b,
                x_0,
                tol,
                niter,
                SOR_OMEGA_1,
                norm_value,
                tolerance_type,
            ),
            # Relaxation Factor = 0.5 (Sub-Relaxation)
            "SOR-2": sor_method(
                matrix_A,
                vector_b,
                x_0,
                tol,
                niter,
                SOR_OMEGA_2,
                norm_value,
                tolerance_type,
            ),
            # Relaxation Factor = 1.5 (Over-Relaxation)
            "SOR-3": sor_method(
                matrix_A,
                vector_b,
                x_0,
                tol,
                niter,
                SOR_OMEGA_3,
                norm_value,
                tolerance_type,
            ),
        }

        table = {
            "Método": [],
            "$n_\\text{iter}$": [],
            "$E$": [],
        }

        # Create a column for each value of the solution vector.
        n = len(x_0)
        for i in range(n):
            table[f"$x_{i+1}$"] = []

        for method in results:
            X, results_table, _, _, _, _ = results[method]

            # Respective method
            table["Método"].append(method)

            # Append each value of the solution vector in general format
            # (that is, scientific notation if too big or small).
            for i in range(n):
                table[f"$x_{i+1}$"].append(f"{X[i][0]:g}")

            # Append the last iteration of each method.
            table["$n_\\text{iter}$"].append(results_table.index[-1])

            # Append the Error of the last iteration.
            error_value = results_table.tail(1)["Error"].iloc[0]
            formatted_error = f"{error_value:g}"
            table["$E$"].append(formatted_error)

        df = pd.DataFrame(table)
        st.table(df)
