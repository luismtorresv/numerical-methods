import pandas as pd
import sympy as sp


def fixed_point_method(a, b, X0, Tol, type_of_tol, Niter, Fun, Fun_g):
    #Check the G function
    
    x_sym = sp.symbols("x")
    try:
        g_expr = sp.sympify(Fun_g.replace("^", "**"))
    except (sp.SympifyError, SyntaxError) as e:
        raise ValueError(f"Invalid expression: {e}")
    g_func = sp.lambdify(x_sym, g_expr, modules=["math"])

    # Inicialización de listas para la tabla
    iteraciones = []
    xn = []
    fn = []
    errores = []

    # Primera iteración
    x = X0
    f = Fun(x)
    c = 0
    Error = 100  # Error inicial arbitrario

    iteraciones.append(c)
    xn.append(x)
    fn.append(f)
    errores.append(Error)
    while Error > Tol and f != 0 and c < Niter:
        x = g_func(x)  # Nueva aproximación usando g(x)

        # Validar que la nueva aproximación esté en el intervalo [a, b]
        if x < a or x > b:
            print(
                f"Error: La iteración {c} generó un valor fuera del intervalo [{a}, {b}]."
            )
            break

        f = Fun(x)  # Evaluamos f(x)

        c += 1
        if type_of_tol == "D.C":
            Error = abs(x - xn[-1])  # Cálculo del error absoluto
        else:
            Error = abs((x - xn[-1]) / x)  # Cálculo del error relativo

        # Guardar valores en listas
        iteraciones.append(c)
        xn.append(x)
        fn.append(f)
        errores.append(Error)

    # Mostrar resultados finales

    # Crear y mostrar la tabla de iteraciones
    tabla = pd.DataFrame(
        {"Iteración": iteraciones, "Xn": xn, "f(Xn)": fn, "Error": errores}
    )

    if f == 0:
        # print(f"{x} es raíz de f(x)")
        return tabla, x
    elif Error < Tol:
        # print(f"{x} es una aproximación de una raíz con tolerancia {Tol}")
        return tabla, x
    else:
        # print(f"Fracaso en {Niter} iteraciones")
        return None, Niter
