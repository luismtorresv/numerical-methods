import numpy as np
import streamlit as st
import sympy as sp

from utils.interface_blocks import enter_points, graph_with_points

from .Spline_cubic import cubic_spline_interpolation


def show_cubic_spline():
    st.header("Cubic Spline Method")
    st.markdown(
        """
    **Cubic Spline Interpolation** is a method for interpolating data points using piecewise cubic polynomials. Each segment of the spline is a cubic polynomial, and the method ensures that the overall function is smooth, continuous, and its first and second derivatives are also continuous across all intervals.

    **Key Features:**
    - Each piece of the spline is a cubic polynomial.
    - The spline is continuous, and both the first and second derivatives are continuous at the interior points.
    - The method provides a smooth curve without sharp turns or discontinuities.
    """
    )
    with st.expander("📘 How the False Position Method Works"):
        st.markdown(
            """

        For each interval $ [x_i, x_{i+1}] $, the cubic spline is given by:
        """
        )
        st.latex(
            r"""
        S_i(x) = a_i x^3 + b_i x^2 + c_i x + d_i
        """
        )
        st.markdown(
            """
        Where $ a_i $, $ b_i $, $ c_i $, and $ d_i $ are the coefficients to be determined.

        **Steps:**
        1. **Interpolation Constraints**: The cubic spline must pass through each data point, so we have the following conditions:
        """
        )
        st.latex(
            r"""
        S_i(x_i) = y_i \quad \text{and} \quad S_i(x_{i+1}) = y_{i+1}
        """
        )
        st.markdown(
            """
        2. **Continuity of Derivatives**: The first and second derivatives of the spline must be continuous at the interior points:
        """
        )
        st.latex(
            r"""
        S'_i(x_{i+1}) = S'_{i+1}(x_{i+1}) \quad \text{and} \quad S''_i(x_{i+1}) = S''_{i+1}(x_{i+1})
        """
        )
        st.markdown(
            """
        3. **Solve for Coefficients**: The system of equations formed by these conditions is solved to determine the coefficients $ a_i $, $ b_i $, $ c_i $, and $ d_i $.

        **Advantages:**
        - Produces a smooth, continuous curve with no abrupt changes in slope or curvature.
        - Often used for applications requiring smooth interpolations like computer graphics or numerical simulations.

        **Disadvantages:**
        - Requires solving a system of linear equations, which can be computationally intensive for large datasets.
        - May not perform well if the data is highly oscillatory or has outliers.
        """
        )

    try:
        # Input points (minimum 4 points required for cubic spline)
        x_values, y_values = enter_points(val=4)

        # Input validation
        if len(x_values) != len(set(x_values)):
            st.error(
                "Error: The points entered have an x-repeated value, which makes it impossible to be represented as a function."
            )
            return

        if len(x_values) < 4:
            st.error(
                "Error: At least 4 points are required for cubic spline interpolation."
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

            # Perform cubic spline interpolation
            try:
                (
                    piecewise_function_unrounded,
                    piecewise_function_rounded,
                ) = cubic_spline_interpolation(x_values, y_values, decimals=decimals)

                # Display results
                st.subheader("Results")
                st.write("**Cubic Spline Piecewise Function**")
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
