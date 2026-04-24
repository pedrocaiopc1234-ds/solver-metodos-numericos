"""
Roots methods: Bisection, Newton, Secant
"""

def bisection(f, a, b, tol=1e-6, max_iter=100):
    """
    Bisection method for finding roots.

    Returns:
        dict with keys: success (bool), root (float or None), iterations (int),
                        iterations_data (list), error (str or None)
    """
    try:
        fa, fb = f(a), f(b)
        if fa * fb > 0:
            return {"success": False, "root": None, "iterations": 0,
                    "iterations_data": [],
                    "error": "Função não muda de sinal no intervalo [a,b]"}

        iterations_data = []
        for i in range(max_iter):
            c = (a + b) / 2
            fc = f(c)
            iterations_data.append({"a": a, "b": b, "c": c, "fc": fc})
            if abs(fc) < tol:
                return {"success": True, "root": c, "iterations": i+1,
                        "iterations_data": iterations_data, "error": None}
            if fa * fc < 0:
                b, fb = c, fc
            else:
                a, fa = c, fc

        return {"success": False, "root": None, "iterations": max_iter,
                "iterations_data": iterations_data,
                "error": "Máximo de iterações atingido sem convergência"}
    except Exception as e:
        return {"success": False, "root": None, "iterations": 0,
                "iterations_data": [],
                "error": f"Método falhou: {str(e)}"}


def newton(f, df, x0, tol=1e-6, max_iter=100):
    """
    Newton's method for finding roots.

    Returns:
        dict with keys: success (bool), root (float or None), iterations (int),
                        iterations_data (list), error (str or None)
    """
    try:
        iterations_data = []
        for i in range(max_iter):
            fx = f(x0)
            dfx = df(x0)
            if dfx == 0:
                iterations_data.append({"x": x0, "fx": fx, "dfx": dfx, "x_next": None})
                return {"success": False, "root": x0, "iterations": i,
                        "iterations_data": iterations_data,
                        "error": f"Método falhou: derivada igual a zero no ponto x = {x0}"}
            x1 = x0 - fx / dfx
            iterations_data.append({"x": x0, "fx": fx, "dfx": dfx, "x_next": x1})
            if abs(x1 - x0) < tol:
                return {"success": True, "root": x1, "iterations": i+1,
                        "iterations_data": iterations_data, "error": None}
            x0 = x1

        return {"success": False, "root": x0, "iterations": max_iter,
                "iterations_data": iterations_data,
                "error": "Máximo de iterações atingido sem convergência"}
    except Exception as e:
        return {"success": False, "root": None, "iterations": 0,
                "iterations_data": [],
                "error": f"Método falhou: {str(e)}"}


def secant(f, x0, x1, tol=1e-6, max_iter=100):
    """
    Secant method for finding roots.

    Returns:
        dict with keys: success (bool), root (float or None), iterations (int),
                        iterations_data (list), error (str or None)
    """
    try:
        f0 = f(x0)
        iterations_data = []
        for i in range(max_iter):
            f1 = f(x1)
            if f1 - f0 == 0:
                iterations_data.append({"x0": x0, "x1": x1, "f0": f0, "f1": f1, "x2": None})
                return {"success": False, "root": x1, "iterations": i,
                        "iterations_data": iterations_data,
                        "error": "Método falhou: divisão por zero (pontos muito próximos)"}
            x2 = x1 - f1 * (x1 - x0) / (f1 - f0)
            iterations_data.append({"x0": x0, "x1": x1, "f0": f0, "f1": f1, "x2": x2})
            if abs(x2 - x1) < tol:
                return {"success": True, "root": x2, "iterations": i+1,
                        "iterations_data": iterations_data, "error": None}
            x0, f0 = x1, f1
            x1 = x2

        return {"success": False, "root": x1, "iterations": max_iter,
                "iterations_data": iterations_data,
                "error": "Máximo de iterações atingido sem convergência"}
    except Exception as e:
        return {"success": False, "root": None, "iterations": 0,
                "iterations_data": [],
                "error": f"Método falhou: {str(e)}"}