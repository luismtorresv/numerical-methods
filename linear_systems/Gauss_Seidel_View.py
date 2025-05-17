import streamlit as st

from utils.interface_blocks import (
    calculate_tolerance,
    definite_matrix_interface,
    graph_Ab,
    show_matrix,
    show_T_and_C,
)

from .Gauss_seidel import gauss_seidel_method


def show_gauss_seidel():
    st.header("Gauss Seidel Method")
    st.markdown(
        """
    **Gauss-Seidel Method** is an iterative algorithm for solving systems of linear equations of the form $Ax = b$.
    It refines an initial guess by repeatedly updating the solution components, using the most recent values for faster convergence.
    """
    )

    with st.expander("📘 Detailed Explanation of the Gauss-Seidel Method"):
        st.markdown(
            """
            **Method Overview:**
            - The Gauss-Seidel method updates the solution iteratively using the formula:
            """
        )
        st.latex(
            r"""
        x_j^{(k+1)} = \frac{1}{a_{jj}} \left( b_j - \sum_{i=1}^{j-1} a_{ji}x_i^{(k+1)} - \sum_{i=j+1}^{n} a_{ji}x_i^{(k)} \right)
        """
        )
        st.markdown(
            """
            where $a_{jj}$ is the diagonal element of $A$, and $k$ represents the iteration step.

            **Procedure:**
            1. **Initialization**:
            - Start with an initial guess $X^{(0)}$.
            - Compute the diagonal matrix $D$, lower triangular part $L$, and upper triangular part $U$ from $A$.

            2. **Iteration**:
            - Compute the iteration matrix $T = (D - L)^{-1}U$ and constant vector $C = (D - L)^{-1}b$.
            - Update the solution iteratively using the Gauss-Seidel formula.

            3. **Stopping Criteria**:
            - Stop the iterations if the error (norm of the difference between successive solutions) is less than the specified tolerance $\\text{tol}$.

            **Convergence:**
            - For guaranteed convergence, the matrix $A$ should be diagonally dominant or symmetric positive definite.
            - The spectral radius of the iteration matrix $T$, denoted $\\rho(T)$, must satisfy $\\rho(T) < 1$.

            **Advantages:**
            - Faster convergence compared to Jacobi for diagonally dominant matrices.
            - Memory-efficient since it updates the solution vector in place.

            **Disadvantages:**
            - May not converge for non-diagonally dominant matrices.
            - Sensitive to the initial guess.

            **Key Formulas:**
            - Iteration matrix:
            """
        )
        st.latex(
            r"""
        T = (D - L)^{-1}U
        """
        )
        st.markdown(
            """
            - Constant vector:
            """
        )
        st.latex(
            r"""
        C = (D - L)^{-1}b
        """
        )
        st.markdown(
            """
            **Use Cases:**
            - Solving large, sparse systems in numerical simulations.
            - Applications in engineering and computational science where direct methods are impractical.
            """
        )

    try:
        matrix_A, vector_b, x_0, norm_value = definite_matrix_interface(x_0="Yes")

        tol, niter, tolerance_type = calculate_tolerance()

        st.write("Calculated Tolerance: ", tol)

        graph_Ab(matrix_A, vector_b)

        X, table, rad_esp, err, T, C = gauss_seidel_method(
            matrix_A, vector_b, x_0, tol, niter, norm_value, tolerance_type
        )

        if err == None:
            st.success("The Gauss Seidel method has converged successfully.")
            # Display the results
            st.write(f"**Solution Vector (x)**")
            show_matrix(X, deci=False)
            st.write(f"**Solution Table**")
            show_matrix(table)
            st.write("Spectral Radius: ", rad_esp)
            show_T_and_C(T, C)

        else:
            st.write("Spectral Radius: ", rad_esp)
            st.error(f"Error: Please Check Your Input. {err}")
    except Exception as e:
        st.error(f"Error: Please Check Your Input")
