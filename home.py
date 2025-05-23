import streamlit as st

from interpolation import *
from linear_systems import *
from single_variable import *
from utils.graph import show_graph

# Initialize session state if not already initialized
if "page" not in st.session_state:
    st.session_state.page = "home"


# Function definitions for each page
def show_home():
    st.header("Function input guide")

    st.markdown(
        """
You can combine these elements to create complex expressions. Ensure
your input string follows proper Python syntax for mathematical
expressions. This way, `sympify` can parse and convert it correctly into
a SymPy expression.

1. Polynomials:

    You can input terms with powers of a variable using standard
mathematical notation.

    ```python
    x**2 + 3*x - 5
    ```

2. Trigonometric Functions:

    Use standard names for trigonometric functions: `sin`, `cos`, `tan`, etc.

    ```python
    sin(x) + cos(x)
    ```

3. Exponential Functions:

    Represent exponential functions using `exp`.

    ```python
    exp(x)
    ```

4. Hyperbolic Trigonometric Functions:

    Use `sinh`, `cosh`, and `tanh` for hyperbolic functions.

    ```python
    sinh(x) + cosh(x)
    ```

5. Logarithms:

    Use `log` for natural logarithms and `log(expr, base)` for logarithms
    with a specific base.

    ```python
    log(x) + log(x, 10)
    ```

6. Square Roots and Other Roots:

    Use `sqrt` for square roots or fractional powers for other roots.

    ```python
    sqrt(x) + x**(1/3)
    ```
"""
    )


# Sidebar navigation and categories with buttons for each method
st.sidebar.title("Numerical Methods")

if st.sidebar.button("Home"):
    st.session_state.page = "home"

# Button for "Function Graphing"
if st.sidebar.button("Show Graph"):
    st.session_state.page = "graph"

# Buttons for "Finding Roots"
if st.sidebar.button("Finding Roots"):
    st.session_state.page = "roots"

# Buttons for "Solving Systems of Equations"
if st.sidebar.button("Solving Systems of Equations"):
    st.session_state.page = "systems"


# Buttons for "Interpolation Methods"
if st.sidebar.button("Interpolation Methods"):
    st.session_state.page = "interpolation"

# Render the page based on session state
if st.session_state.page == "home":
    show_home()
elif st.session_state.page == "graph":
    show_graph()
elif st.session_state.page == "roots":
    st.title("Finding Roots of Polynomials")

    # Dropdown to select root-finding method
    root_method = st.selectbox(
        "Select a root-finding method",
        [
            "Bisection",
            "Newton-Raphson",
            "Secant",
            "False Position",
            "Fixed Point",
            "Multiple Roots",
        ],
    )

    # Display the corresponding method content based on the dropdown selection
    match root_method:
        case "Newton-Raphson":
            show_newton()
        case "Secant":
            show_secant()
        case "Bisection":
            show_bisection()
        case "False Position":
            show_regula_falsi()
        case "Fixed Point":
            show_fixed_point()
        case "Multiple Roots":
            show_multiple_roots()
elif st.session_state.page == "systems":
    st.title("Solving Systems of Equations")

    # Dropdown to select a system-solving method
    system_method = st.selectbox(
        "Select a system-solving method",
        [
            "Jacobi",
            "Gauss-Seidel",
            "SOR",
        ],
    )

    # Display the corresponding method content based on the dropdown selection
    match system_method:
        case "Jacobi":
            show_Jacobi()
        case "Gauss-Seidel":
            show_gauss_seidel()
        case "SOR":
            show_SOR()

elif st.session_state.page == "interpolation":
    st.title("Interpolation Methods")
    # Dropdown to select interpolation method
    interpolation_method = st.selectbox(
        "Select an interpolation method",
        [
            "Vandermonde Matrix",
            "Newton Divided Difference",
            "Lagrange Interpolation",
            "Linear Spline Interpolation",
            "Cubic Spline Interpolation",
        ],
    )

    # Display the corresponding method content based on the dropdown selection
    match interpolation_method:
        case "Vandermonde Matrix":
            show_vandermonde()
        case "Newton Divided Difference":
            show_newton_divided_diff()
        case "Lagrange Interpolation":
            show_lagrange()
        case "Linear Spline Interpolation":
            show_spline()
        case "Cubic Spline Interpolation":
            show_cubic_spline()
