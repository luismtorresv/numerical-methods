import streamlit as st

from views.single_variable.Bisection_View import show_bisection
from views.single_variable.FixedPoint_View import show_fixed_point
from views.linear_systems.Gauss_Seidel_View import show_gauss_seidel
from Views.Bisection_View import show_bisection
from Views.FixedPoint_View import show_fixed_point
from Views.Gauss_Seidel_View import show_gauss_seidel
from Views.GaussNoPivot_View import show_gauss_jordan_no_pivot
from Views.GaussPartialPivot_View import show_gauss_jordan_partial_pivot
from Views.GaussTotalPivot_View import show_gauss_jordan_total_pivot

# Import necessary views for each method
from Views.Graph import show_graph
from Views.Incremental_View import show_incremental
from Views.Jacobi_View import show_Jacobi
from Views.Lagrange_View import show_lagrange
from Views.LU_Factorization_View import show_LU_factorization
from Views.MultipleRoots_View import show_multiple_roots
from Views.Newton_View import show_newton
from Views.NewtonDividedDiff_View import show_newton_divided_diff
from Views.PLU_factorization_View import show_PLU_factorization
from Views.RegulaFalsi_View import show_regula_falsi
from Views.Secant_View import show_secant
from Views.SOR_View import show_SOR
from Views.Spline_Cubic_View import show_cubic_spline
from Views.Spline_Quadratic_View import show_quadratic_spline
from Views.Spline_View import show_spline
from Views.Vandermonde_View import show_vandermonde

# Initialize session state if not already initialized
if "page" not in st.session_state:
    st.session_state.page = "home"


# Function definitions for each page
def show_home():
    st.title("Numerical Methods Project")
    st.write(
        "Welcome to the project on numerical methods. Choose a category from the sidebar to explore various algorithms."
    )

    st.header("Categories and Methods")

    # Finding Roots
    st.subheader("Finding Roots")
    st.markdown("- Incremental Search")
    st.markdown("- Bisection")
    st.markdown("- False Position")
    st.markdown("- Fixed Point")
    st.markdown("- Newton Raphson")
    st.markdown("- Secant")
    st.markdown("- Multiple Roots")

    # Solving Systems of Equations
    st.subheader("Solving Systems of Equations")
    st.markdown("- Gaussian Elimination Simple")
    st.markdown("- Gaussian Elimination Partial Pivot")
    st.markdown("- Gaussian Elimination Total Pivot")
    st.markdown("- Direct Factorization (LU - PLU)")
    st.markdown("- Jacobi")
    st.markdown("- Gauss-Seidel")
    st.markdown("- SOR")

    # Interpolation
    st.subheader("Interpolation")
    st.markdown("- Vandermonde Interpolation")
    st.markdown("- Newton Interpolation")
    st.markdown("- Lagrange")
    st.markdown("- Spline Linear")
    st.markdown("- Spline Quadratic")
    st.markdown("- Spline Cubic")

    st.header("How to Input Functions in Python SymPy")
    st.write(
        """
        SymPy's `sympify(expr_str)` function allows you to convert a string representation of a mathematical expression into a SymPy-compatible format. In this proyect we use this function. Then, for a function input, you have to follow the following set of guidelines:
    """
    )

    st.subheader("1. Polynomials")
    st.write(
        """
        For polynomials, you can input terms with powers of a variable using standard mathematical notation.
    """
    )
    st.code(
        """
            x**2 + 3*x - 5
    """,
        language="python",
    )

    st.subheader("2. Trigonometric Functions")
    st.write(
        """
        Use standard names for trigonometric functions: `sin`, `cos`, `tan`, etc.
    """
    )
    st.code(
        """
        sin(x) + cos(x)
    """,
        language="python",
    )

    st.subheader("3. Exponential Functions")
    st.write(
        """
        Represent exponential functions using `exp`.
    """
    )
    st.code(
        """
            exp(x)
    """,
        language="python",
    )

    st.subheader("4. Hyperbolic Trigonometric Functions")
    st.write(
        """
        Use `sinh`, `cosh`, and `tanh` for hyperbolic functions.
    """
    )
    st.code(
        """
        sinh(x) + cosh(x)
    """,
        language="python",
    )

    st.subheader("5. Logarithms")
    st.write(
        """
        Use `log` for natural logarithms and `log(expr, base)` for logarithms with a specific base.
    """
    )
    st.code(
        """
        log(x) + log(x, 10)
    """,
        language="python",
    )

    st.subheader("6. Square Roots and Other Roots")
    st.write(
        """
        Use `sqrt` for square roots or fractional powers for other roots.
    """
    )
    st.code("""sqrt(x) + x**(1/3)""", language="python")

    st.write(
        """
        You can combine these elements to create complex expressions. Ensure your input string follows proper Python syntax for mathematical expressions. This way, `sympify` can parse and convert it correctly into a SymPy expression.
    """
    )


# Sidebar navigation and categories with buttons for each method
st.sidebar.title("Numerical Methods Menu")

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
            "Incremental Search",
            "Bisection",
            "Newton-Raphson",
            "Secant",
            "False Position",
            "Fixed Point",
            "Multiple Roots",
        ],
    )

    # Display the corresponding method content based on the dropdown selection
    if root_method == "Newton-Raphson":
        show_newton()
    elif root_method == "Secant":
        show_secant()
    elif root_method == "Bisection":
        show_bisection()
    elif root_method == "False Position":
        show_regula_falsi()
    elif root_method == "Incremental Search":
        show_incremental()
    elif root_method == "Fixed Point":
        show_fixed_point()
    elif root_method == "Multiple Roots":
        show_multiple_roots()

elif st.session_state.page == "systems":
    st.title("Solving Systems of Equations")

    # Dropdown to select a system-solving method
    system_method = st.selectbox(
        "Select a system-solving method",
        [
            "Gauss-Jordan without Pivoting",
            "Gauss-Jordan with Partial Pivoting",
            "Gauss-Jordan with Total Pivoting",
            "LU Factorization",
            "PLU Factorization",
            "Jacobi",
            "Gauss-Seidel",
            "SOR",
        ],
    )

    # Display the corresponding method content based on the dropdown selection
    if system_method == "Gauss-Jordan without Pivoting":
        show_gauss_jordan_no_pivot()
    elif system_method == "Gauss-Jordan with Partial Pivoting":
        show_gauss_jordan_partial_pivot()
    elif system_method == "Gauss-Jordan with Total Pivoting":
        show_gauss_jordan_total_pivot()
    elif system_method == "LU Factorization":
        show_LU_factorization()
    elif system_method == "PLU Factorization":
        show_PLU_factorization()
    elif system_method == "Jacobi":
        show_Jacobi()
    elif system_method == "Gauss-Seidel":
        show_gauss_seidel()
    elif system_method == "SOR":
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
            "Quadratic Spline Interpolation",
            "Cubic Spline Interpolation",
        ],
    )

    # Display the corresponding method content based on the dropdown selection
    if interpolation_method == "Vandermonde Matrix":
        show_vandermonde()
    elif interpolation_method == "Newton Divided Difference":
        show_newton_divided_diff()
    elif interpolation_method == "Lagrange Interpolation":
        show_lagrange()
    elif interpolation_method == "Linear Spline Interpolation":
        show_spline()
    elif interpolation_method == "Quadratic Spline Interpolation":
        show_quadratic_spline()
    elif interpolation_method == "Cubic Spline Interpolation":
        show_cubic_spline()
