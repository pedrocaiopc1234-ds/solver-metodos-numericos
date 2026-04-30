"""
Roots methods: Bisection, Newton, Secant
"""

import numpy as np


def bisection(f, a, b, tol=1e-6, max_iter=100):
    """
    Bisection method for finding roots.

    Returns:
        dict with keys: success (bool), root (float or None), iterations (int),
                        iterations_data (list), error (str or None)
    """
    try:
        a, b = float(a), float(b)

        if a >= b:
            return {"success": False, "root": None, "iterations": 0,
                    "iterations_data": [],
                    "error": "a deve ser menor que b"}
        if tol <= 0:
            return {"success": False, "root": None, "iterations": 0,
                    "iterations_data": [],
                    "error": "tolerância deve ser maior que 0"}
        if max_iter <= 0:
            return {"success": False, "root": None, "iterations": 0,
                    "iterations_data": [],
                    "error": "max_iter deve ser maior que 0"}

        fa, fb = f(a), f(b)

        if np.isnan(fa) or np.isinf(fa) or np.isnan(fb) or np.isinf(fb):
            return {"success": False, "root": None, "iterations": 0,
                    "iterations_data": [],
                    "error": "Função retornou valores inválidos (NaN ou Inf) nos extremos do intervalo"}

        if fa * fb > 0:
            return {"success": False, "root": None, "iterations": 0,
                    "iterations_data": [],
                    "error": "Função não muda de sinal no intervalo [a,b]"}

        iterations_data = []
        for i in range(max_iter):
            c = (a + b) / 2
            fc = f(c)
            if np.isnan(fc) or np.isinf(fc):
                return {"success": False, "root": None, "iterations": i+1,
                        "iterations_data": iterations_data,
                        "error": f"Função retornou valor inválido em x = {c:.6f}"}
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
        x0 = float(x0)

        if np.isnan(x0) or np.isinf(x0):
            return {"success": False, "root": None, "iterations": 0,
                    "iterations_data": [],
                    "error": "x0 deve ser um valor finito"}
        if tol <= 0:
            return {"success": False, "root": None, "iterations": 0,
                    "iterations_data": [],
                    "error": "tolerância deve ser maior que 0"}
        if max_iter <= 0:
            return {"success": False, "root": None, "iterations": 0,
                    "iterations_data": [],
                    "error": "max_iter deve ser maior que 0"}

        iterations_data = []
        for i in range(max_iter):
            fx = f(x0)
            dfx = df(x0)
            if np.isnan(fx) or np.isinf(fx):
                return {"success": False, "root": None, "iterations": i,
                        "iterations_data": iterations_data,
                        "error": f"Função retornou valor inválido em x = {x0}"}
            if np.isnan(dfx) or np.isinf(dfx):
                return {"success": False, "root": None, "iterations": i,
                        "iterations_data": iterations_data,
                        "error": f"Derivada retornou valor inválido em x = {x0}"}
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

        final_root = None if (np.isnan(x0) or np.isinf(x0)) else x0
        return {"success": False, "root": final_root, "iterations": max_iter,
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
        x0 = float(x0)
        x1 = float(x1)

        if np.isnan(x0) or np.isinf(x0):
            return {"success": False, "root": None, "iterations": 0,
                    "iterations_data": [],
                    "error": "x0 deve ser um valor finito"}
        if np.isnan(x1) or np.isinf(x1):
            return {"success": False, "root": None, "iterations": 0,
                    "iterations_data": [],
                    "error": "x1 deve ser um valor finito"}
        if tol <= 0:
            return {"success": False, "root": None, "iterations": 0,
                    "iterations_data": [],
                    "error": "tolerância deve ser maior que 0"}
        if max_iter <= 0:
            return {"success": False, "root": None, "iterations": 0,
                    "iterations_data": [],
                    "error": "max_iter deve ser maior que 0"}

        f0 = f(x0)
        if np.isnan(f0) or np.isinf(f0):
            return {"success": False, "root": None, "iterations": 0,
                    "iterations_data": [],
                    "error": "Função retornou valor inválido em x0"}

        iterations_data = []
        for i in range(max_iter):
            f1 = f(x1)
            if np.isnan(f0) or np.isinf(f0) or np.isnan(f1) or np.isinf(f1):
                return {"success": False, "root": None, "iterations": i,
                        "iterations_data": iterations_data,
                        "error": "Função retornou valores inválidos (NaN ou Inf)"}
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

        final_root = None if (np.isnan(x1) or np.isinf(x1)) else x1
        return {"success": False, "root": final_root, "iterations": max_iter,
                "iterations_data": iterations_data,
                "error": "Máximo de iterações atingido sem convergência"}
    except Exception as e:
        return {"success": False, "root": None, "iterations": 0,
                "iterations_data": [],
                "error": f"Método falhou: {str(e)}"}