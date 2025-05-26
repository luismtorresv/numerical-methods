import pandas as pd
import streamlit as st

SOR_OMEGA_1 = 1
SOR_OMEGA_2 = 0.5
SOR_OMEGA_3 = 1.5


def generate_report(matrix_A, vector_b, x_0, tol, niter, norm_value, tolerance_type):
    st.subheader("Method comparison report")

    with st.form("report"):
        submitted = st.form_submit_button("Generate report")
    if submitted:

        results = _run_all_methods(
            matrix_A, vector_b, x_0, tol, niter, norm_value, tolerance_type
        )

        table = {
            "Method": [],
            "$n_\\text{iter}$": [],
            "$E$": [],
        }

        failed_methods = []

        # Create a column for each value of the solution vector.
        n = len(x_0)
        for i in range(n):
            table[f"$x_{i+1}$"] = []

        print(f"{results=}")
        for method_name, output in results.items():
            if output.err:
                failed_methods.append(method_name)
                continue

            # Respective method
            table["Method"].append(method_name)

            # Append each value of the solution vector in general format
            # (that is, scientific notation if too big or small).
            for i in range(n):
                table[f"$x_{i+1}$"].append(f"{output.x[i][0]:g}")

            # Append the last iteration of each method.
            last_iteration = output.table.index[-1]
            table["$n_\\text{iter}$"].append(last_iteration)

            # Append the Error of the last iteration.
            error_value = output.table.tail(1)["Error"].iloc[0]
            formatted_error = f"{error_value:g}"
            table["$E$"].append(formatted_error)

        df = pd.DataFrame(table)
        st.table(df)

        # If any method fails, we print them out
        if failed_methods:
            st.write("The following methods failed to converge:")
            for method in failed_methods:
                st.write(method)

        # Find the best method
        best_iteration = min(table["$n_\\text{iter}$"])
        best_method_id = table["$n_\\text{iter}$"].index(
            min(table["$n_\\text{iter}$"])
        )  # Position of the lowest iteration
        st.write(
            f'The best method is {table["Method"][best_method_id]}, which took {best_iteration} iterations to converge.'
        )


def _run_all_methods(matrix_A, vector_b, x_0, tol, niter, norm_value, tolerance_type):
    from linear_systems.gauss_seidel import gauss_seidel_method
    from linear_systems.jacobi import jacobi_method
    from linear_systems.sor import sor_method

    return {
        "Jacobi": jacobi_method(
            matrix_A, vector_b, x_0, tol, niter, norm_value, tolerance_type
        ),
        "Gauss-Seidel": gauss_seidel_method(
            matrix_A, vector_b, x_0, tol, niter, norm_value, tolerance_type
        ),
        # Relaxation Factor = 1
        "SOR-1": sor_method(
            matrix_A, vector_b, x_0, tol, niter, SOR_OMEGA_1, norm_value, tolerance_type
        ),
        # Relaxation Factor = 0.5 (Sub-Relaxation)
        "SOR-2": sor_method(
            matrix_A, vector_b, x_0, tol, niter, SOR_OMEGA_2, norm_value, tolerance_type
        ),
        # Relaxation Factor = 1.5 (Over-Relaxation)
        "SOR-3": sor_method(
            matrix_A, vector_b, x_0, tol, niter, SOR_OMEGA_3, norm_value, tolerance_type
        ),
    }
