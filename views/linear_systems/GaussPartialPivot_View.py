import streamlit as st

from interface_blocks import (definite_matrix_interface, gauss_matrix_result,
                              graph_Ab)
from Methods.Gauss_partial_pivot import gauss_partial_pivot
from Methods.matrix_helpers import back_substitution


def show_gauss_jordan_partial_pivot():
    st.header("Gauss-Jordan Elimination with partial Pivoting")

    st.markdown(
        """
    **Gauss-Jordan Elimination with Partial Pivoting** is an improved version of the traditional Gauss-Jordan method. It introduces partial pivoting to enhance numerical stability and avoid issues such as division by zero or poor conditioning of matrices.

    **Key Features:**
    - **Partial Pivoting:** At each step, the algorithm swaps rows to ensure the largest absolute value in the column is selected as the pivot element. This reduces numerical errors and improves stability.
    - **Reduced Row Echelon Form (RREF):** Like the standard Gauss-Jordan method, the algorithm transforms the augmented matrix into RREF for direct extraction of solutions.
    - Solves systems of linear equations in a finite number of steps.

    """
    )

    with st.expander("📘 How Gauss-Jordan with Partial Pivoting Works"):
        st.markdown(
            """
        **Procedure:**
        1. **Initialization**: Begin with the augmented matrix $[A | b]$, where $A$ is the coefficient matrix, and $b$ is the column vector of constants.

        2. **Partial Pivoting**: At each step, identify the row with the largest absolute value in the current pivot column and swap it with the current row.

        3. **Row Reduction**: Perform row operations to eliminate all elements below and above the pivot (diagonal element).

        4. **Normalize Diagonal Elements**: Divide each row by the diagonal element to make the diagonal entries equal to 1.

        5. **Back Substitution**: Once the matrix is in reduced row echelon form, extract the solution directly from the matrix.

        **Row Operations**:
        - Swap rows to bring the row with the largest pivot element to the top:
        """
        )
        st.latex(
            r"""
        R_i \leftrightarrow R_j
        """
        )
        st.markdown(
            """
        - Eliminate elements below and above the pivot using:
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
        - More numerically stable than the standard Gauss-Jordan method.
        - Handles poorly conditioned matrices better.
        - Reduces the likelihood of division by zero.

        **Disadvantages**:
        - Slightly more computational overhead due to row swapping.
        - Still has a time complexity of $O(n^3)$.

        **Use Cases**:
        - Solving systems of linear equations where numerical stability is a concern.
        - Applications requiring exact solutions for non-singular matrices.
        """
        )

    try:
        matrix_A, vector_b = definite_matrix_interface()

        graph_Ab(matrix_A, vector_b)

        result = gauss_partial_pivot(matrix_A, vector_b)

        if result["status"] == "error":
            st.error(result["message"])
            return
        else:
            row_echelon = result["A"]
            vector_b = result["b"]

            vector_x = back_substitution(row_echelon, vector_b)

        gauss_matrix_result(row_echelon, vector_b, vector_x)
    except:
        st.error("Error: Please Check Your Inputs")
