import numpy as np
import pandas as pd
import plotly.graph_objs as go
import streamlit as st
import sympy as sp

from utils.general import nm_lambdify


def ui_input_function(placeholder_function="sin(x)"):
    col1, col2 = st.columns(2)

    function_input = col1.text_input(
        "Function $f(x)$",
        value=placeholder_function,
        help="Enter a function in terms of $x$.",
    )

    if not function_input:
        st.error("**Error:** Please enter a function.")
        return None

    x = sp.symbols("x")
    function_sp = sp.sympify(function_input)
    col2.latex(f"f({x}) = {sp.latex(function_sp)}")
    return function_input


def calculate_tolerance():
    col5, col6, col7 = st.columns(3)
    with col5:
        # Ask whether the user wants to use significant figures or decimal places
        tolerance_type = st.radio(
            "Tolerance Type",
            ("Correct Decimals", "Significant Figures"),
            help="Choose whether you want to set the tolerance based on significant figures or correct decimal places.",
        )

    with col6:
        # Ask for the number of significant figures or correct decimals
        if tolerance_type == "Significant Figures":
            num_figures = st.number_input(
                "Number of Significant Figures",
                value=5,
                min_value=1,
                step=1,
                help="The number of significant figures to use for tolerance calculation.",
            )
            # Calculate tolerance based on significant figures
            tol = 5 * 10 ** (-num_figures)

        elif tolerance_type == "Correct Decimals":
            num_decimals = st.number_input(
                "Number of Correct Decimals",
                value=6,
                min_value=1,
                step=1,
                help="The number of correct decimals to use for tolerance calculation.",
            )
            # Calculate tolerance based on correct decimals
            tol = 0.5 * 10 ** (-num_decimals)

    with col7:
        niter = st.number_input(
            "Number of Iterations",
            value=1000,
            min_value=1,
            step=1,
            help="The maximum number of iterations the algorithm will perform to find the root. Higher values allow for more precision.",
        )
    return tol, niter, tolerance_type


def graph(function_input, min_value=-10, max_value=10):
    x = sp.symbols("x")

    # Create a symbolic function
    function_sp = sp.sympify(function_input)
    function = nm_lambdify(function_sp, x)

    x_vals = np.linspace(min_value, max_value, 1000)
    y_vals = function(x_vals)

    # Mask large values (possible infinity)
    with np.errstate(divide="ignore", invalid="ignore"):
        large_values = np.abs(y_vals) > 1 / 0.0000000001
        y_vals[large_values] = None

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode="lines", name=function_input))

    fig.update_layout(
        title=f"Graph of {function_input}",
        xaxis_title=str(x),
        yaxis_title=f"f({str(x)})",
        showlegend=True,
        margin=dict(l=0, r=0, t=40, b=0),
        hovermode="closest",
    )

    st.plotly_chart(fig, key=f"plotly_chart_{function_input}")


def definite_matrix_interface():
    cols_A = rows_A = st.number_input(
        "Enter number of rows:",
        min_value=2,
        max_value=7,
        value=3,
    )

    # Input for A matrix
    matrix_A = pd.DataFrame(
        np.zeros((rows_A, cols_A)),
        columns=[f"x_{i + 1}" for i in range(cols_A)],
    )
    st.write("**$A$ matrix**")
    edited_matrix = st.data_editor(
        matrix_A,
        num_rows="fixed",
        use_container_width=True,
    )
    matrix_A = edited_matrix.to_numpy()

    col1, col2, col3 = st.columns(3)
    with col1:
        norm_value = norm()
    with col2:
        # Input for b vector
        vector_b = pd.DataFrame(np.zeros((rows_A, 1)), columns=["b"])
        st.write("**$b$ vector**")
        edited_vector = st.data_editor(
            vector_b, num_rows="fixed", use_container_width=True
        )
        vector_b = edited_vector.to_numpy()
    with col3:
        # Input for x_0 vector
        vector_x0 = pd.DataFrame(np.zeros((rows_A, 1)), columns=["x_0"])
        st.write("**Initial Guess Vector ($x_0$)**")
        edited_vector_x0 = st.data_editor(
            vector_x0,
            num_rows="fixed",
            use_container_width=True,
        )
        vector_x0 = edited_vector_x0.to_numpy()

    return matrix_A, vector_b, vector_x0, norm_value


def iterative_matrix_interface():
    cols_A = rows_A = st.number_input("Enter number of rows:", min_value=1, value=3)

    col1, col2, col3 = st.columns(3)
    with col1:
        matrix_A = pd.DataFrame(
            np.zeros((rows_A, cols_A)), columns=[f"x_{i}" for i in range(cols_A)]
        )

        st.write("$A$ matrix:")
        edited_matrix = st.data_editor(matrix_A, num_rows="fixed")

        # Convert the edited matrix to a NumPy array
        matrix_A = edited_matrix.to_numpy()
    with col2:
        rows_b = rows_A
        cols_b = 1
        vector_b = pd.DataFrame(
            np.zeros((rows_b, cols_b)), columns=[f"b" for i in range(cols_b)]
        )

        st.write("$b$ vector:")
        edited_vector = st.data_editor(vector_b, num_rows="fixed")

        vector_b = edited_vector.to_numpy()
    with col3:
        rows_x0 = rows_A
        cols_x0 = 1
        vector_x0 = pd.DataFrame(
            np.zeros((rows_x0, cols_x0)), columns=[f"x_{i}" for i in range(cols_x0)]
        )

        st.write("Initial guess vector:")
        edited_vector_x0 = st.data_editor(vector_x0, num_rows="fixed")

        vector_x0 = edited_vector_x0.to_numpy()

    calculate_tolerance()

    return matrix_A, vector_b, vector_x0


def enter_points(val=2):
    # Get the number of points from user input
    num_points = st.number_input(
        "Enter the number of points:",
        min_value=val,
        max_value=8,
        value=val,
        step=1,
        help="""First, specify the number of points you want to enter.
    Once the number of points is selected, you'll be able to input the x and y coordinates.
    You can enter the coordinates in any order (not necessarily sequential).""",
    )

    # Create a DataFrame to hold the points
    points_df = pd.DataFrame(np.zeros((2, num_points)), index=["x", "y"])

    # For x values, initialize with sequential numbers starting from 0
    points_df.iloc[0] = range(num_points)

    # Allow the user to edit the DataFrame
    edited_points_df = st.data_editor(
        points_df, num_rows="fixed", use_container_width=True
    )

    # Extract x and y values
    x_values = edited_points_df.iloc[0].tolist()
    y_values = edited_points_df.iloc[1].tolist()

    return x_values, y_values


def graph_with_points(x_values, y_values, function, x_symbol=sp.symbols("x")):
    function = nm_lambdify(function, x_symbol)

    x_min = min(x_values) - 1
    x_max = max(x_values) + 1
    x_vals = np.linspace(x_min, x_max, 500)
    y_vals = [function(x_val) for x_val in x_vals]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode="lines", name="Polynomial P(x)"))
    fig.add_trace(
        go.Scatter(x=x_values, y=y_values, mode="markers", name="Data Points")
    )

    fig.update_layout(
        title=f"Graph of the Interpolation",
        xaxis_title=str(x_symbol),
        yaxis_title=f"y",
        showlegend=True,
        margin=dict(l=0, r=0, t=40, b=0),
        hovermode="closest",
    )

    st.plotly_chart(fig)

    # Add value calculator
    st.subheader("Calculate Value at Point")
    x_calc = st.number_input(
        "Enter x value",
        value=float(sum(x_vals) / len(x_vals)),
        min_value=float(min(x_vals)),
        max_value=float(max(x_vals)),
    )
    y_calc = float(function(x_calc))
    st.write(f"Q({x_calc}) = {y_calc}")


def show_table(result, deci=True, decimals=None):
    if deci:
        decimals = st.slider(
            "Select number of decimals to display on table",
            min_value=1,
            max_value=5,
            value=4,
            help="Adjust the number of decimal places for the result table.",
        )
    if deci or decimals != None:
        result = result.style.format(f"{{:.{decimals}f}}")

    st.dataframe(result, use_container_width=True)

    return decimals


def show_matrix(matrix, deci=True, decimals=None):
    if deci:
        decimals = st.slider(
            "Select number of decimals to display",
            min_value=1,
            max_value=5,
            value=4,
            help="Adjust the number of decimal places in the matrix.",
        )
    if deci or decimals != None:
        matrix = np.round(matrix, decimals)
    st.dataframe(matrix, use_container_width=True)


def gauss_matrix_result(row_echelon, vector_b, vector_x, decimals=5):
    decimals = st.slider(
        "Select number of decimals to display",
        min_value=1,
        max_value=10,
        value=4,
        help="Adjust the number of decimal places in the result.",
    )

    st.subheader("Result")

    st.write("**Row echelon form $A$ and vector $\vec{b}$**")
    col1, col2 = st.columns(2)
    with col1:
        row_echelon = sp.Matrix(np.round(row_echelon, decimals))
        st.latex(f"R = {sp.latex(row_echelon)}")
    with col2:
        vector_b = sp.Matrix(np.round(vector_b, decimals))
        st.latex(f"\\vec{{b}} = {sp.latex(vector_b)}")

    st.write("**Solution vector**")
    vector_x = sp.Matrix(np.round(vector_x, decimals))
    st.latex(f"\\vec{{x}} = {sp.latex(vector_x)}")


def show_T_and_C(T, C):
    col1, col2 = st.columns(2)

    with col1:
        T = sp.Matrix(np.round(T, 5))
        st.latex(f"T = {sp.latex(T)}")

    with col2:
        C = sp.Matrix(np.round(C, 5))
        st.latex("\\vec{C} = " + f"{sp.latex(C)}")


def norm():
    # Method to ask the user if they want 1, 2, 3 or infinity norm
    norm_value = st.radio(
        "Norm",
        ("1-norm", "2-norm", "$\infty$-norm"),
    )
    if norm_value == "1-norm":
        norm_value = 1
    elif norm_value == "2-norm":
        norm_value = 2
    elif norm_value == "$\infty$-norm":
        norm_value = "inf"
    return norm_value


def graph_Ab(A, b):
    size_A = A.shape[0]
    if size_A == 2 and np.linalg.det(A) != 0 and A[0][1] != 0 and A[1][1] != 0:
        x_values = np.linspace(-10, 10, 100)

        y1 = (b[0] - A[0][0] * x_values) / A[0][1]
        y2 = (b[1] - A[1][0] * x_values) / A[1][1]

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=x_values,
                y=y1,
                mode="lines",
                name=f"Equation 1: -{A[0][0]/A[0][1]}x + {(b[0]/A[0][1])[0]}",
            )
        )
        fig.add_trace(
            go.Scatter(
                x=x_values,
                y=y2,
                mode="lines",
                name=f"Equation 2: -{A[1][0]/A[1][1]}x + {(b[1]/A[1][1])[0]}",
            )
        )

        fig.update_layout(
            title=f"Graph of the System of Equations",
            xaxis_title="x",
            yaxis_title="y",
            showlegend=True,
            margin=dict(l=0, r=0, t=40, b=0),
            hovermode="closest",
        )

        st.plotly_chart(fig)
    else:
        st.info(
            "The matrix does not represent a function y=f(x) so it cannot be graphed"
        )
