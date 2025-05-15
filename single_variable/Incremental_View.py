import numpy as np
import pandas as pd
import streamlit as st
import sympy as sp

from utils.interface_blocks import calculate_tolerance, enter_function, graph

from .Incremental import incremental_search


def show_incremental():
    st.markdown(
        """
    Incremental search is a numerical method used to approximate the roots of a function ${f(x)}$.
    It works by iteratively evaluating the function over a specified interval and looking for sign changes
    between consecutive evaluations. A sign change indicates the presence of a root within the interval.
    """,
        unsafe_allow_html=True,
    )

    with st.expander("📘 How Incremental Search Works"):
        st.markdown(
            """
        **1. Define the Interval and Step Size:**
        - Choose an interval $[a, b]$ where you suspect the root lies.
        - Select a step size $\Delta x$ for evaluating the function incrementally.

        **2. Evaluate the Function Incrementally:**
        - Start at the lower bound $a$.
        - Evaluate $f(x)$ at each increment:
        """
        )
        st.latex(
            r"""
        x_i = a + i \cdot \Delta x, \; i = 0, 1, 2, \dots
        """
        )
        st.markdown(
            """
            **3. Check for Sign Changes:**
            - If
        """
        )
        st.latex(
            r"""
        f(x_i) \cdot f(x_{i+1}) < 0
        """
        )
        st.markdown(
            """
            there is a root in the interval:
        """
        )
        st.latex(
            r"""
        [x_i, x_{i+1}]
        """
        )
        st.markdown(
            """
            **Advantages:**
            - Simple to implement and understand.
            - Does not require derivatives or complex calculations.

            **Disadvantages:**
            - May miss roots if the step size $\Delta x$ is too large.
            - Computationally expensive for small $\Delta x$ over large intervals.
        """,
            unsafe_allow_html=True,
        )

    try:
        st.header("Incremental Search Method")

        x, function_input = enter_function(
            placeholder_function="x**2 - 4", placeholder_variable="x"
        )

        col3, col4 = st.columns(2)
        with col3:
            x0 = st.number_input(
                "Initial point of search",
                format="%.4f",
                value=1.0,
                step=0.0001,
                help="The initial point of the search.",
            )
        with col4:
            delta_x = st.number_input(
                "Step size (delta x)",
                format="%.4f",
                value=0.001,
                step=0.0001,
                min_value=0.00009,
                help="How large the steps will be in the search.",
            )

        tol, niter, tolerance_type = calculate_tolerance()
        st.markdown(f"**Calculated Tolerance:** {tol:.10f}")

        x = sp.symbols(f"{x}")
        function = sp.sympify(function_input)

        st.subheader("Function")
        st.latex(f"f({x}) = {sp.latex(function)}")

        function = sp.lambdify(x, sp.sympify(function_input), "numpy")

        # DO CHECKS ON INPUT INTEGRITY
        # check if derivative is continuous in general

        result = incremental_search(x0, delta_x, niter, tol, tolerance_type, function)

        if result["status"] == "error":
            st.error(result["message"])
            return
        else:
            result = result["table"]

        # Add a slider to choose the number of decimals to display
        decimals = st.slider(
            "Select number of decimals to display on table",
            min_value=1,
            max_value=10,
            value=4,
            help="Adjust the number of decimal places for the result table.",
        )
        # Format the dataframe to display the selected number of decimals
        result_display = result.style.format(
            f"{{:.{decimals}f}}"
        )  # Use f-string to format dynamically

        st.subheader("Results")
        st.dataframe(result_display, use_container_width=True)

        mid = result.iloc[-1]["x_i"]
        st.success(
            f"Root found at x = {mid:.{decimals}f}: f({mid:.{decimals}f}) = {function(mid):.{decimals}f}"
        )

    except Exception as e:
        st.error("Error: Check your inputs")
        print(e)

    graph(x, function_input)
