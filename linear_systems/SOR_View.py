import streamlit as st

from utils.interface_blocks import (calculate_tolerance,
                                    definite_matrix_interface, graph_Ab,
                                    show_matrix, show_T_and_C)

from .SOR import \
    sor_method  # Asegúrate de que el método SOR esté implementado en el módulo correspondiente


def show_SOR():
    st.header("Successive Over-Relaxation (SOR) Method")
    st.markdown(
        """
    **Successive Over-Relaxation (SOR) Method** is an iterative technique for solving linear systems of equations,
    extending the Gauss-Seidel method by introducing a relaxation factor, $\\omega$, to accelerate convergence.
    """
    )

    with st.expander("📘 Detailed Explanation of the SOR Method"):
        st.markdown(
            """
            **Method Overview:**
            - The SOR method is derived from splitting the matrix $A$ into its diagonal ($D$), lower triangular ($L$),
            and upper triangular ($U$) components, similar to the Gauss-Seidel method, but with an over-relaxation factor $\\omega$.
            - The formula for the iteration is:
            """
        )
        st.latex(
            r"""
        x^{(k+1)} = (D - \omega L)^{-1} \left[ \omega b + \left( (1 - \omega) D + \omega U \right) x^{(k)} \right]
        """
        )
        st.markdown(
            """
            where:
            - $\\omega$ is the relaxation factor ($0 < \\omega < 2$).
            - If $\\omega = 1$, the method reduces to the Gauss-Seidel method.

            **Procedure:**
            1. **Initialization**:
            - Start with an initial guess $X^{(0)}$ and choose a relaxation factor $\\omega$.
            - Decompose $A$ into $D$, $L$, and $U$.

            2. **Iteration**:
            - Compute matrices:
                - $T = (D - \\omega L)^{-1}((1 - \\omega) D + \\omega U)$
                - $C = \\omega (D - \\omega L)^{-1} b$
            - Update the solution using:
                - $X^{(k+1)} = T X^{(k)} + C$

            3. **Stopping Criteria**:
            - Stop if the error norm $||X^{(k+1)} - X^{(k)}||$ is below a given tolerance.

            **Convergence:**
            - The SOR method converges faster than Gauss-Seidel for well-chosen values of $\\omega$.
            - For optimal $\\omega$, the method achieves the fastest convergence.

            **Advantages:**
            - Improves convergence speed over Gauss-Seidel for certain systems.
            - Simple to implement once $\\omega$ is determined.

            **Disadvantages:**
            - Choosing the optimal $\\omega$ is not straightforward.
            - May not converge for poorly conditioned matrices.

            **Key Parameters:**
            - **Relaxation Factor** ($\\omega$):
            - $0 < \\omega < 1$: Under-relaxation (slower convergence but safer).
            - $\\omega = 1$: Equivalent to Gauss-Seidel.
            - $1 < \\omega < 2$: Over-relaxation (faster convergence for diagonally dominant matrices).

            """
        )
    try:
        # Interfaz para definir la matriz, el vector b y otros parámetros iniciales
        matrix_A, vector_b, x_0, norm_value = definite_matrix_interface(x_0="Yes")

        # Parámetros adicionales: tolerancia, iteraciones y tipo de error
        tol, niter, tolerance_type = calculate_tolerance()

        # Factor de relajación ω
        omega = st.number_input(
            "Relaxation Factor (ω):", min_value=0.0, max_value=2.0, step=0.1, value=1.0
        )

        st.write("Calculated Tolerance: ", tol)

        graph_Ab(matrix_A, vector_b)

        # Ejecutar el método SOR
        X, table, rad_esp, err, T, C = sor_method(
            matrix_A, vector_b, x_0, tol, niter, omega, norm_value, tolerance_type
        )

        if err is None:
            st.success("The SOR method has converged successfully.")

            # Mostrar los resultados
            st.write(f"**Solution Vector (x)**")
            show_matrix(X, deci=False)

            st.write(f"**Solution Table**")
            show_matrix(table)

            st.write("Spectral Radius: ", rad_esp)
            show_T_and_C(T, C)
        else:
            st.error(err)
    except Exception as e:
        st.error("Error: Please Check The Input")
        print(e)
