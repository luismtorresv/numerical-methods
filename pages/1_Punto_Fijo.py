import streamlit as st
import sympy as sp

from Main import Numerical_Methods, Web_page
from Methods.Fixed_point_method import fixed_point_method


class Fixed_Point_Page(Numerical_Methods):
    def __init__(self, iterations, function, tolerance, interval, X0, g_function):
        super().__init__(iterations, function, tolerance, interval)
        self.X0 = X0
        self.g_funtion = g_function

    def call_method(self):
        a, b = self.interval
        X0 = self.X0
        Tol = self.tolerance
        Niter = self.N_iterations
        Fun = self.function
        Fun_g = self.g_funtion
        return fixed_point_method(
            a, b, X0, Tol, self.type_of_tolerance, Niter, Fun, Fun_g
        )


def Main():
    Web_page.intro("Fixed Point")

    with st.form("PF"):
        # Input data. The data unique to the method is passed as an arg to the method
        (
            N_iter,
            tolerance,
            f_function,
            x_0,
            type_of_tolerance,
            interval,
            g_function,
        ) = Web_page.form_questions("Function g(x)")
        button = st.form_submit_button("Run method")
    if button:
        # Check if the entered values are valid
        try:
            # Check parent values
            interval, tolerance, x_0 = Web_page.check_values(
                interval, tolerance, type_of_tolerance, x_0
            )

            # Check both functions
            x_symbol = sp.symbols("x")
            f_function = f"{sp.parse_expr(f_function,evaluate=False)}"
            g_function = f"{sp.parse_expr(g_function,evaluate=False)}"

        except:
            st.write("Input error. Check your inputs.")

        # If there are no errors with the inputs, create the class.
        pf = Fixed_Point_Page(
            N_iter,
            f_function,
            (tolerance, type_of_tolerance),
            interval,
            x_0,
            g_function,
        )

        # Display results
        st.subheader("Functions")
        st.latex(f"f({x_symbol}) = {sp.latex(f_function)}")
        st.latex(f"g({x_symbol}) = {sp.latex(g_function)}")

        table, x = pf.call_method()  # We can finally call the numerical method.
        if table is None:
            st.write("Method failed.")
            return
        else:
            pf.display_results(table, x, pf.tolerance)
            Web_page.create_graph(pf.function, pf.interval)


if __name__ == "__main__":
    Main()
