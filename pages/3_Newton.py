import streamlit as st
import sympy as sp
from Main import Numerical_Methods
from Methods.Newton import Nt


class Newton(Numerical_Methods):
    def __init__(self, iteraciones, function, tolerance, X0, intervalo, f_derivate):
        super().__init__(iteraciones, function, tolerance, intervalo)
        self.X0 = X0
        self.f_derivate = f_derivate

    def Newton(self):
        X0 = self.X0
        Tol = self.tolerance
        Niter = self.N_iteraciones
        Fun = self.function
        Fun_derivate = self.f_derivate
        return Nt(X0, Tol, self.type_of_tolerance, Niter, Fun, Fun_derivate)


def Main():
    st.set_page_config(page_title="Newton")
    st.markdown("# Newton")
    st.markdown(
        " ### NOTA: La funcion ingresada debe de ser una funcion valida y continua. Solo ingresar el numero deseado de D.C/C.S en la tolerancia."
    )

    with st.form("PF"):
        N_iter = st.slider("Numero de Iteraciones:", 0, 100)
        tolerancia = st.slider("Tolerancia: ", 0, 100)
        f_function = st.text_input("Funcion:")
        f_derivate = st.text_input("Derivada de la Funcion:")
        x_0 = st.text_input("Valor inicial X0:")

        tipo_tolerancia = st.selectbox(
            "Escoge un tipo de tolerancia:",
            ["C.S", "D.C"],
        )

        st.write("Intervalo:")
        intervalo = (
            st.text_input("Limite inferior (a):"),
            st.text_input("Limite superior (b):"),
        )

        button = st.form_submit_button("Ejecutar Metodo")
    if button:

        # Check if the entered values are valid
        try:
            a, b = intervalo
            intervalo = (
                float(a),
                float(b),
            )

            tolerancia = (
                float(f"5e-{tolerancia}")
                if tipo_tolerancia == "C.S"
                else float(f"0.5e-{tolerancia}")
            )

            x_0 = float(x_0)
            x_symbol = sp.symbols(f"x")

            # Evaluate leaves the function intact
            f_function = f"{sp.parse_expr(f_function,evaluate=False)}"
            f_derivate = f"{sp.parse_expr(f_derivate,evaluate=False)}"

        except:
            st.write("Hubo un error con los datos ingresados. ¡Intenta de nuevo!")

        st.subheader("Functions")
        st.latex(f"f({x_symbol}) = {sp.latex(f_function)}")
        st.latex(f"f'({x_symbol}) = {sp.latex(f_derivate)}")

        # Check if the functions are valid
        Nt = Newton(
            N_iter,
            f_function,
            (tolerancia, tipo_tolerancia),
            x_0,
            intervalo,
            f_derivate,
        )
        table, x = Nt.Newton()  # We can finally call the numerical method.
        if table is None:
            st.write("Fracaso")
            return
        else:
            Nt.display_results(table, x, Nt.tolerance)


if __name__ == "__main__":
    Main()
