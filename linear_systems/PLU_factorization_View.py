import streamlit as st

from utils.interface_blocks import (LU_result, definite_matrix_interface,
                                    graph_Ab)

from .PLU_factorization import PLU_factorization, solve_PLU


def show_PLU_factorization():
    st.header("LU Factorization with pivoting")

    st.markdown(
        """
    **PLU Factorization** is an extension of LU factorization that incorporates row permutations to handle matrices that require pivoting. This method decomposes a square matrix $A$ into the product of a permutation matrix $P$, a lower triangular matrix $L$, and an upper triangular matrix $U$, such that $P \cdot A = L \cdot U$.

    **Key Features:**
    - **Permutation Matrix ($P$):** Handles row swaps to ensure numerical stability and avoid division by zero.
    - **Lower Triangular Matrix ($L$):** Contains the multipliers used during row reduction.
    - **Upper Triangular Matrix ($U$):** Contains the transformed matrix after row reduction.
    - Ensures the factorization is possible for all non-singular matrices.
    """
    )

    with st.expander("📘 How PLU Factorization Works"):
        st.markdown(
            """
        **Procedure**
        1. **Initialization**:
        - Start with a square matrix $A$.
        - Create identity matrices $L$ and $P$.
        - Copy $A$ to begin the decomposition.

        2. **Pivoting**:
        - At each step, identify the largest absolute value in the current column (below or at the diagonal).
        - Swap rows in $A$ to bring this element to the pivot position.
        - Update the permutation matrix $P$ to reflect the row swap.

        3. **Decomposition**:
        - Perform Gaussian elimination to create zeros below the diagonal in $U$.
        - Store the multipliers in the corresponding positions of $L$.

        4. **Validation**:
        - If any pivot element is zero, the matrix is singular and cannot be decomposed.

        **Forward and Backward Substitution**:
        - Solve $Ax = b$ by rewriting it as $P \cdot A \cdot x = P \cdot b$:
        1. Solve $L \cdot y = P \cdot b$ using forward substitution.
        2. Solve $U \cdot x = y$ using backward substitution.

        **Mathematical Formulas**:
        - Row swapping (pivoting):
        """
        )
        st.latex(
            r"""
        P_{\text{new}} \cdot A
        """
        )
        st.markdown(
            """
        - Eliminate elements below the pivot:
        """
        )
        st.latex(
            r"""
        A_{j} = A_{j} - \frac{A_{j,i}}{A_{i,i}} A_{i}, \quad \text{for } j > i
        """
        )
        st.markdown(
            """
        - Store the multipliers in $L$:
        """
        )
        st.latex(
            r"""
        L_{j,i} = \frac{A_{j,i}}{A_{i,i}}, \quad \text{for } j > i
        """
        )

        st.markdown(
            """
        **Advantages**:
        - Ensures numerical stability through row pivoting.
        - Handles all non-singular matrices, even those with zero elements on the diagonal.

        **Disadvantages**:
        - Requires additional computations for pivoting and updating the permutation matrix.
        - Slightly more complex implementation compared to LU factorization.

        **Use Cases**:
        - Solving systems of linear equations with ill-conditioned matrices.
        - Matrix inversion and computation of determinants (as the product of $P$, $L$, and $U$).
        - Applications requiring stable numerical solutions.
        """
        )

    try:
        matrix_A, vector_b = definite_matrix_interface()
        graph_Ab(matrix_A, vector_b)

        result = PLU_factorization(matrix_A)

        if result["status"] == "error":
            st.error(result["message"])
            return
        else:
            L = result["L"]
            U = result["U"]
            P = result["P"]

            vector_x = solve_PLU(P, L, U, vector_b)

        LU_result(P=P, L=L, U=U, vector_x=vector_x)
    except:
        st.error("Error: Please Check Your Input")
