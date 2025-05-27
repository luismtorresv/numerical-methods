import streamlit as st
import sympy as sp

from utils.interface_blocks import graph


def show_graph():
    st.title("Interactive Function Grapher")

    # Input fields with tooltips
    col1, col2 = st.columns(2)
    with col1:
        x = st.text_input(
            "Enter a Variable Name",
            "x",
            max_chars=1,
            help="Enter a variable name to use in the function. Default is 'x'.",
        )
    with col2:
        function_input = st.text_input(
            "Enter a Function",
            "sin(x)",
            help="Enter a function in terms of the variable chosen.",
        )

        # Range inputs with restriction
    col3, col4 = st.columns(2)
    with col3:
        min_value = st.number_input(
            "Minimum Value",
            value=-10.0,
            help="Set the minimum value for the x-axis range.",
        )
    with col4:
        max_value = st.number_input(
            "Maximum Value",
            value=10.0,
            help="Set the maximum value for the x-axis range. Must be greater than the minimum value.",
        )

    # Validate that max_value > min_value
    if max_value <= min_value:
        st.error("Error: Maximum Value must be greater than Minimum Value.")
        return  # Stop execution if the condition isn't met

    if not x.isalpha():
        st.error("Error: Variable name must be a single alphabetic character.")
        return
    if not function_input:
        st.error("Error: Please enter a function.")
        return

    try:
        x = sp.symbols(x)  # Convert input to a sympy symbol

        # Display the parsed function in LaTeX
        st.subheader("Your Function")
        st.latex(sp.sympify(function_input))  # Render the function in LaTeX

        # Pass the validated range to the graph function
        graph(function_input, min_value, max_value)

    except Exception as e:
        st.error(f"Error: Please check your input.")
        print(e)
