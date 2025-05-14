import streamlit as st

from interface_blocks import (definite_matrix_interface, gauss_matrix_result,
                              graph_Ab)
from Methods.Gauss_no_pivot import gauss_no_pivot
from Methods.matrix_helpers import back_substitution


def show_gauss_jordan_no_pivot():
    st.header("Gauss-Jordan Elimination without Pivoting")

    st.markdown(
        """
        **Gauss-Jordan Elimination** is an algorithm for solving systems of linear equations. It works by transforming the augmented matrix into a reduced row echelon form (RREF), from which the solution can be easily read.

        **Key Features:**
        - The method involves transforming the augmented matrix into a diagonal matrix (with 1s on the diagonal) using row operations.
        - It is a direct method for solving linear systems, i.e., it computes the solution in a finite number of steps.
        - This version of Gauss-Jordan does not use pivoting (which can improve numerical stability), meaning it may fail for singular or poorly conditioned matrices.

    """
    )

    with st.expander("📘 How the False Position Method Works"):
        st.markdown(
            """
        **Procedure:**        
        1. **Initialization**: Begin with the augmented matrix $[A | b]$, where $A$ is the coefficient matrix and $b$ is the column vector of constants.
        
        2. **Row Reduction**: For each row $i$, ensure that the diagonal element $a_{ii}$ is non-zero. If it is zero, the algorithm swaps rows (this would be avoided in Gauss-Jordan with pivoting, but it's still possible in this method with a check).
        
        3. **Elimination**: Eliminate all elements below the pivot (diagonal element) by subtracting a multiple of the row from the other rows.
        
        4. **Normalize Diagonal Elements**: Divide each row by the diagonal element $a_{ii}$ to ensure that the diagonal element becomes 1.
        
        5. **Back Substitution**: Once the matrix is in reduced row echelon form, the solution is obtained directly from the matrix.

        **Formula for Row Operations**:
        - Subtract a multiple of one row from another to eliminate off-diagonal elements:
        """
        )
        st.latex(
            r"""         
        R_j \leftarrow R_j - \frac{a_{ji}}{a_{ii}} R_i
        """
        )
        st.markdown(
            """
        - Normalize a row by dividing it by its diagonal element:
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
        - Simple to understand and implement.
        - Direct method that provides an exact solution if the matrix is non-singular.

        **Disadvantages**:
        - Computationally expensive, with a time complexity of $O(n^3)$.
        - Not stable for matrices that are poorly conditioned or singular.
        - Without pivoting, it is vulnerable to division by zero or round-off errors.

        """
        )

    try:
        matrix_A, vector_b = definite_matrix_interface()

        # Graph the equations represented if n=2
        graph_Ab(matrix_A, vector_b)

        result = gauss_no_pivot(matrix_A, vector_b)

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
