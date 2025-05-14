import streamlit as st

from interface_blocks import (definite_matrix_interface, gauss_matrix_result,
                              graph_Ab)
from Methods.Gauss_total_pivot import gauss_total_pivot


def show_gauss_jordan_total_pivot():
    st.header("Gauss-Jordan Elimination with Total Pivoting")
    st.markdown(
        """
    **Gauss-Jordan Elimination with Total Pivoting** is an advanced variant of the Gauss-Jordan method. It further improves numerical stability by selecting the largest possible pivot element from the entire submatrix at each step, rather than just the current column. This minimizes round-off errors and ensures the most robust solution.

    **Key Features:**
    - **Total Pivoting:** The algorithm swaps both rows and columns to position the largest absolute value from the submatrix at the current pivot position.
    - **Reduced Row Echelon Form (RREF):** The augmented matrix is transformed into RREF for direct solution extraction.
    - Offers greater stability compared to partial pivoting, especially for poorly conditioned matrices.
    """
    )

    with st.expander("📘 How Gauss-Jordan with Total Pivoting Works"):
        st.markdown(
            """
        **Procedure:**
        1. **Initialization**: Start with the augmented matrix $[A | b]$, where $A$ is the coefficient matrix and $b$ is the column vector of constants.

        2. **Total Pivoting**:
        - Identify the largest absolute value in the remaining submatrix.
        - Swap rows to bring this value into the current pivot row.
        - Swap columns to bring this value into the current pivot column.
        - Keep track of column swaps to correctly interpret the solution.

        3. **Row Reduction**: Eliminate all elements below and above the pivot using row operations.

        4. **Normalize Diagonal Elements**: Divide each row by its pivot to make the diagonal entries equal to 1.

        5. **Back Substitution**: Extract the solution directly from the matrix while accounting for any column swaps.

        **Row and Column Operations**:
        - Swap rows to bring the largest pivot element into the pivot row:
        """
        )
        st.latex(
            r"""
        R_i \leftrightarrow R_j
        """
        )
        st.markdown(
            """
        - Swap columns to bring the largest pivot element into the pivot column:
        """
        )
        st.latex(
            r"""
        C_i \leftrightarrow C_j
        """
        )
        st.markdown(
            """
        - Eliminate non-diagonal elements using:
        """
        )
        st.latex(
            r"""
        R_k \leftarrow R_k - \frac{a_{ki}}{a_{ii}} R_i
        """
        )
        st.markdown(
            """
        - Normalize the pivot row:
        """
        )
        st.latex(
            r"""
        R_i \leftarrow \frac{1}{a_{ii}} R_i
        """
        )

        st.markdown(
            """
        **Advantages**:
        - Maximizes numerical stability by reducing round-off errors.
        - Particularly effective for ill-conditioned matrices or those prone to numerical issues.

        **Disadvantages**:
        - Higher computational overhead due to the search for the largest pivot and column swaps.
        - Requires bookkeeping for column swaps to correctly interpret the final solution.

        **Use Cases**:
        - Solving systems of linear equations where precision is paramount.
        - Scenarios with matrices prone to instability or numerical inaccuracies.
        """
        )

    try:
        matrix_A, vector_b = definite_matrix_interface()

        graph_Ab(matrix_A, vector_b)

        result = gauss_total_pivot(matrix_A, vector_b)

        if result["status"] == "error":
            st.error(result["message"])
            return
        else:
            row_echelon = result["A"]
            vector_b = result["b"]

            vector_x = result["x"]

        gauss_matrix_result(row_echelon, vector_b, vector_x)
    except:
        st.error("Error: Please Check Your Inputs")
