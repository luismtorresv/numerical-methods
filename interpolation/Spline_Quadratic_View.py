import numpy as np
import streamlit as st
import sympy as sp

from utils.interface_blocks import enter_points, graph_with_points

from .Spline_quadratic import quadratic_spline_interpolation


def show_quadratic_spline():
    st.header("Quadratic Spline Method")

    st.markdown(
        """
        **Quadratic Spline Interpolation** is a method that uses piecewise quadratic functions to interpolate between data points. Unlike linear splines, which are piecewise linear, quadratic splines provide a smoother interpolation by using quadratic functions for each interval.

        **Key Features:**
        - Each piece of the spline is a quadratic function.
        - The spline is continuous, and its first derivative is continuous at the interior points.
        - The second derivative is continuous at the second interior point, ensuring smoothness.

    """
    )
    with st.expander("📘 How the Cuadratic Spline Method Works"):
        st.markdown(
            """
        For each interval $ [x_i, x_{i+1}] $, the quadratic spline is given by:
        """
        )
        st.latex(
            r"""
        S_i(x) = a_i x^2 + b_i x + c_i
        """
        )
        st.markdown(
            """
        Where $ a_i $, $ b_i $, and $ c_i $ are the coefficients to be determined.

        **Steps:**
        1. **Interpolation Constraints**: The quadratic spline must pass through each data point, so we have the following conditions:
        """
        )
        st.latex(
            r"""
        S_i(x_i) = y_i \quad \text{and} \quad S_i(x_{i+1}) = y_{i+1}
        """
        )
        st.markdown(
            """
        2. **Continuity of Derivatives**: The first derivative of the spline must be continuous at the interior points:
        """
        )
        st.latex(
            r"""
        S'_i(x_{i+1}) = S'_{i+1}(x_{i+1})
        """
        )
        st.markdown(
            """
        3. **Second Derivative Continuity**: The second derivative is continuous at the second interior point to ensure smoothness:
        """
        )
        st.latex(
            r"""
        S''_0(x_1) = S''_1(x_1)
        """
        )
        st.markdown(
            """
        4. **Solve for Coefficients**: Using the system of equations formed by these constraints, we solve for the coefficients $ a_i $, $ b_i $, and $ c_i $.

        **Advantages:**
        - Provides a smoother interpolation compared to linear splines.
        - Ensures continuity of the first derivative.

        **Disadvantages:**
        - Requires solving a system of equations, which can be computationally intensive for large datasets.
        """
        )
    try:
        # Input points (minimum 3 points required for quadratic spline)
        x_values, y_values = enter_points(val=3)

        # Input validation
        if len(x_values) != len(set(x_values)):
            st.error(
                "Error: The points entered have an x-repeated value, which makes it impossible to be represented as a function."
            )
            return

        if len(x_values) < 3:
            st.error(
                "Error: At least 3 points are required for quadratic spline interpolation."
            )
            return

        try:
            # Sort points by x-values
            points = sorted(zip(x_values, y_values))
            x_values, y_values = zip(*points)
            x_values = list(x_values)
            y_values = list(y_values)

            # Slider for decimal precision
            decimals = st.slider(
                "Select number of decimals to display",
                min_value=1,
                max_value=10,
                value=4,
                help="Adjust the number of decimal places for the result.",
            )

            # Perform quadratic spline interpolation
            try:
                (
                    piecewise_function_unrounded,
                    piecewise_function_rounded,
                ) = quadratic_spline_interpolation(
                    x_values, y_values, decimals=decimals
                )

                # Display results
                st.subheader("Results")
                st.write("**Quadratic Spline Piecewise Function**")
                st.latex(sp.latex(piecewise_function_rounded))

                # Convert the symbolic function to a numerical function
                spline_function = sp.lambdify(
                    sp.symbols("x"), piecewise_function_unrounded
                )

                # Generate numerical values for plotting
                x_plot = np.linspace(min(x_values), max(x_values), 500)
                try:
                    # Graph the interpolation
                    st.subheader("Graph of Spline Interpolation")
                    graph_with_points(x_values, y_values, piecewise_function_unrounded)

                except Exception as e:
                    st.error(f"Error calculating function values: {str(e)}")

            except ValueError as e:
                st.error(f"Error during interpolation: {str(e)}")

        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")

    except:
        st.error("Error: Please Check Your Inputs")
