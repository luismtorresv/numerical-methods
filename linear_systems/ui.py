import streamlit as st
import sympy as sp

from utils.interface_blocks import show_matrix, show_T_and_C


def ui_matrix_flow(mmo):
    """
    mmo → MatrixMethodOutput
    """
    st.divider()
    st.header("Result")
    if mmo.err:
        st.error(mmo.err)
        return False
    st.success(f":material/check: Method has converged to a solution.")

    st.divider()

    st.subheader("Intermediate results")
    show_T_and_C(mmo.T, mmo.C)

    st.divider()

    st.subheader("Convergence")
    st.metric("Spectral radius of $T$", mmo.spectral_radius_T)
    if mmo.spectral_radius_T < 1:
        message = "Since $\\rho(T) < 1$, the method was guaranteed to converge."
    else:
        message = (
            "Since $\\rho(T) \\geq 1$, " "the method was _not_ guaranteed to converge."
        )
    st.write(message)

    st.divider()

    st.header("Solution")
    x = sp.Matrix(mmo.x)
    st.latex("\\vec{x} = " + sp.latex(x))

    st.subheader("Table")
    show_matrix(mmo.table, deci=False)

    st.divider()

    return True
