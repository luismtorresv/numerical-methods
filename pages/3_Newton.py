import streamlit as st
import sympy as sp

from Main import Numerical_Methods, Web_page
from Methods.Newton_method import Newton_method


class Newton_page(Numerical_Methods):
    def __init__(self, iterations, function, tolerance, interval, X0, f_derivative):
        super().__init__(iterations, function, tolerance, interval)
        self.X0 = X0
        self.f_derivative = f_derivative

    def call_method(self):
        X0 = self.X0
        Tol = self.tolerance
        Niter = self.N_iterations
        Fun = self.function
        Fun_derivative = self.f_derivative
        return Newton_method(
            X0, Tol, self.type_of_tolerance, Niter, Fun, Fun_derivative
        )


def Main():
    Web_page.intro("Newton")

    with st.form("NT"):
        (
            N_iter,
            tolerance,
            f_function,
            x_0,
            type_of_tolerance,
            interval,
            f_derivative,
        ) = Web_page.form_questions("Derivative of function F")

        button = st.form_submit_button("Run method")
    if button:
        # Check if the entered values are valid
        try:
            # Check parent values
            interval, tolerance, x_0 = Web_page.check_values(
                interval, tolerance, type_of_tolerance, x_0
            )
            x_symbol = sp.symbols(f"x")

            # Check both functions
            x_symbol = sp.symbols("x")
            f_function = f"{sp.parse_expr(f_function,evaluate=False)}"
            f_derivative = f"{sp.parse_expr(f_derivative,evaluate=False)}"

        except:
            st.write("Input error. Check your inputs.")

        st.subheader("Functions")
        st.latex(f"f({x_symbol}) = {sp.latex(f_function)}")
        st.latex(f"f'({x_symbol}) = {sp.latex(f_derivative)}")

        # Check if the functions are valid
        Newton = Newton_page(
            N_iter,
            f_function,
            (tolerance, type_of_tolerance),
            interval,
            x_0,
            f_derivative,
        )
        table, x = Newton.call_method()  # We can finally call the numerical method.
        if table is None:
            st.write("Method failed.")
            return
        else:
            Newton.display_results(table, x, Newton.tolerance)
            Web_page.create_graph(Newton.function, Newton.interval)


if __name__ == "__main__":
    Main()
