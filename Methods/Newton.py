import pandas as pd
import sympy as sp

def Newton(X0,Tol,type_of_tol,Niter,Fun,df):
    #Checks the derivate of F
    x_sym = sp.symbols("x")
    try:
        df = sp.sympify(df.replace("^", "**"))
    except (sp.SympifyError, SyntaxError) as e:
        raise ValueError(f"Invalid expression: {e}")
    df = sp.lambdify(x_sym, df, modules=["math"])

    # Inicialización de listas para la tabla
    iteraciones = []
    xn_vals = []
    fn_vals = []
    df_vals = []
    errores = []

    # Primera iteración
    x = X0
    f = Fun(x)
    derivada = df(x)
    c = 0
    Error = 100  # Error inicial arbitrario

    iteraciones.append(c)
    xn_vals.append(x)
    fn_vals.append(f)
    df_vals.append(derivada)
    errores.append(Error)

    # Algoritmo del método de Newton-Raphson
    while Error > Tol and f != 0 and derivada != 0 and c < Niter:
        x = x - f / derivada  # Fórmula de Newton-Raphson
        derivada = df(x) # Evaluamos la derivada en el nuevo x
        f = Fun(x) # Evaluamos f(x)
        
        c += 1
        if type_of_tol == "D.C":
            Error = abs(x - xn_vals[-1])  # Cálculo del error absoluto
        else:
            Error = abs((x - xn_vals[-1])/xn_vals[-1])  # Cálculo del error relativo

        # Guardar valores en listas
        iteraciones.append(c)
        xn_vals.append(x)
        fn_vals.append(f)
        df_vals.append(derivada)
        errores.append(Error)

    # Mostrar resultados finales
    # Crear y mostrar la tabla de iteraciones
    tabla = pd.DataFrame({
        "Iteración": iteraciones,
        "Xn": xn_vals,
        "f(Xn)": fn_vals,
        "f'(Xn)": df_vals,
        "Error": errores
    })


    if f == 0:
        #print(f"{x} es raíz de f(x)")
        return tabla, x
    elif Error < Tol:
        #print(f"{x} es una aproximación de una raíz con tolerancia {Tol}")
        return tabla, x
    else:
        #print(f"Fracaso en {Niter} iteraciones")
        return None, Niter

