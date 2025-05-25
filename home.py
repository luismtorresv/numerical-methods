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

# Sidebar.
if st.sidebar.button("Function input guide"):
    st.session_state.page = "home"
if st.sidebar.button("Equations in one variable"):
    st.session_state.page = "roots"
if st.sidebar.button("Linear systems of equations"):
    st.session_state.page = "systems"
if st.sidebar.button("Interpolation"):
    st.session_state.page = "interpolation"
if st.sidebar.button(label="Make it snow ☃️"):
    st.snow()

# Render the page based on session state
if st.session_state.page == "home":
    show_home()
elif st.session_state.page == "graph":
    show_graph()
elif st.session_state.page == "roots":
    st.title("Equations in one variable")

    name_function_matching = {
        "Bisection": show_bisection,
        "Newton-Raphson": show_newton,
        "Secant": show_secant,
        "False Position": show_regula_falsi,
        "Fixed Point": show_fixed_point,
        "Multiple Roots": show_multiple_roots,
    }

    root_method = st.selectbox(
        "Select a root-finding method",
        name_function_matching.keys(),
    )

    name_function_matching[root_method]()

elif st.session_state.page == "systems":
    st.title("Linear systems of equations")

    name_function_matching = {
        "Jacobi": show_Jacobi,
        "Gauss-Seidel": show_gauss_seidel,
        "SOR": show_SOR,
    }

    system_method = st.selectbox(
        "Select a system-solving method",
        name_function_matching.keys(),
    )

    name_function_matching[system_method]()

elif st.session_state.page == "interpolation":
    st.title("Interpolation")

    name_function_matching = {
        "Vandermonde Matrix": show_vandermonde,
        "Newton Divided Difference": show_newton_divided_diff,
        "Lagrange Interpolation": show_lagrange,
        "Linear Spline Interpolation": show_spline,
        "Cubic Spline Interpolation": show_cubic_spline,
    }

    interpolation_method = st.selectbox(
        "Select an interpolation method",
        name_function_matching.keys(),
    )

    name_function_matching[interpolation_method]()
