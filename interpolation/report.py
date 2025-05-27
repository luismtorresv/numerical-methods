import pandas as pd
import sympy as sp
import streamlit as st

from utils.interface_blocks import enter_points

def generate_report():
    st.subheader("Method comparison report")

    with st.form("report"):
        submitted = st.form_submit_button("Generate report")
        x_values, y_values = enter_points(val=4)

        decimals = st.slider(
            "Select number of decimals to display",
            min_value=1,
            max_value=10,
            value=4,
            help="Adjust the number of decimal places for the result table.",
        )
    if submitted:

        results = _run_all_methods(x_values,y_values,decimals)
        table ={
            "Method": [],
            "Polynomial" : []
            }

        for method in results:
            method_results = results[method]

            table["Method"].append(method)

            if "Spline" in method:
                polinomial,_ = method_results[0].args[0]
                table["Polynomial"].append(polinomial)
            else:
                table["Polynomial"].append(str(method_results[-1]))

        df = pd.DataFrame(table)
        st.table(df)


def _run_all_methods(
    x, 
    y, 
    decimals
):
    from interpolation.lagrange import lagrange
    from interpolation.newton_interpolation import newton_interpolation
    from interpolation.spline import linear_spline_interpolation
    from interpolation.spline_cubic import cubic_spline_interpolation
    from interpolation.vandermonde import vandermonde

    return {
        "Lagrange" : lagrange(x,y,decimals),
        "Newton Int" : newton_interpolation(x,y,decimals),
        "Linear Spline" : linear_spline_interpolation(x,y,decimals=None),
        "Cubic Spline" : cubic_spline_interpolation(x,y,decimals=None),
        "Vandermonde" : vandermonde(x,y,decimals)
    }