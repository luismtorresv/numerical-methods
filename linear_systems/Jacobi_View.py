import streamlit as st

from utils.interface_blocks import (
    calculate_tolerance,
    definite_matrix_interface,
    graph_Ab,
    show_matrix,
    show_T_and_C,
)

from .Jacobi import jacobi_method


def show_Jacobi():
    st.header("Jacobi Method")
    st.markdown(
        """
    **Jacobi Method** is an iterative algorithm for solving systems of linear equations $Ax = b$.
    It computes each component of the solution independently at each iteration, using only the values from .the previous iteration.
    """
    )

    with st.expander("📘 Detailed Explanation of the Jacobi Method"):
        st.markdown(
            """
            **Method Overview:**
            - The Jacobi method computes the next approximation for each variable independently, based on the formula:
            """
        )
        st.latex(
            r"""
        x_j^{(k+1)} = \frac{1}{a_{jj}} \left( b_j - \sum_{i=1, i \neq j}^{n} a_{ji} x_i^{(k)} \right)
        """
        )
        st.markdown(
            """
            where $a_{jj}$ is the diagonal element of $A$, and $k$ represents the iteration step.

            **Procedure:**
            1. **Initialization**:
            - Start with an initial guess $X^{(0)}$.
            - Decompose the matrix $A$ into diagonal ($D$), lower triangular ($L$), and upper triangular ($U$) parts.

            2. **Iteration**:
            - Compute the iteration matrix $T = D^{-1}(L + U)$ and the constant vector $C = D^{-1}b$.
            - Update the solution using $X^{(k+1)} = T X^{(k)} + C$.

            3. **Stopping Criteria**:
            - Stop the iterations if the error (norm of the difference between successive solutions) is less than the specified tolerance $\\text{tol}$.

            **Convergence:**
            - The method converges if the spectral radius $\\rho(T)$ satisfies $\\rho(T) < 1$.
            - For guaranteed convergence, $A$ should be diagonally dominant or symmetric positive definite.

            **Advantages:**
            - Straightforward implementation.
            - Each update is independent, making the method parallelizable.

            **Disadvantages:**
            - Slower convergence compared to Gauss-Seidel for diagonally dominant matrices.
            - May fail to converge if the matrix $A$ is not well-conditioned.

            **Key Formulas:**
            - Iteration matrix:
            """
        )
        st.latex(
            r"""
        T = D^{-1}(L + U)
        """
        )
        st.markdown(
            """
            - Constant vector:
            """
        )
        st.latex(
            r"""
        C = D^{-1}b
        """
        )
        st.markdown(
            """
            **Use Cases:**
            - Solving small, sparse linear systems.
            - Educational purposes to demonstrate iterative methods.
            """
        )

    try:
        matrix_A, vector_b, x_0, norm_value = definite_matrix_interface(x_0="Yes")

        tol, niter, tolerance_type = calculate_tolerance()

        st.write("Calculated Tolerance: ", tol)

        graph_Ab(matrix_A, vector_b)

        X, table, rad_esp, err, T, C = jacobi_method(
            matrix_A, vector_b, x_0, tol, niter, norm_value, tolerance_type
        )

        if err == None:
            st.success("The Jacobi method has converged successfully.")
            # Display the results
            st.write(f"**Solution Vector (x)**")
            show_matrix(X, deci=False)
            st.write(f"**Solution Table**")
            show_matrix(table)
            st.write("Spectral Radius: ", rad_esp)
            show_T_and_C(T, C)
        else:
            st.write("Spectral Radius: ", rad_esp)
            st.error(err)
    except:
        st.error("Error: Please Check Your Input")
