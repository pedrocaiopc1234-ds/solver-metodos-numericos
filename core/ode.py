"""
ODE: Euler and Runge-Kutta 4th order methods
"""

import numpy as np


def euler_method(f, y0, t0, tf, h=0.1):
    """
    Euler's method for solving ODEs.

    Args:
        f: function dy/dt = f(t, y)
        y0: initial condition
        t0, tf: initial and final time
        h: step size

    Returns:
        dict with keys: success (bool), t (np.array), y (np.array), error (str or None)
    """
    try:
        y0 = float(y0)
        t0, tf = float(t0), float(tf)
        h = float(h)

        if h <= 0:
            return {"success": False, "t": None, "y": None,
                    "error": "Passo h deve ser maior que 0"}

        if tf <= t0:
            return {"success": False, "t": None, "y": None,
                    "error": "tf deve ser maior que t0"}

        if np.isnan(y0) or np.isinf(y0):
            return {"success": False, "t": None, "y": None,
                    "error": "y0 deve ser um valor finito"}

        n = int(np.ceil((tf - t0) / h)) + 1

        if n > 1000000:
            return {"success": False, "t": None, "y": None,
                    "error": "Número de passos muito grande. Reduza o intervalo ou aumente h."}

        t = np.linspace(t0, tf, n)
        actual_h = (tf - t0) / (n - 1) if n > 1 else h
        y = np.zeros(n)
        y[0] = y0

        for i in range(n - 1):
            try:
                y[i+1] = y[i] + actual_h * f(t[i], y[i])
                if np.isnan(y[i+1]) or np.isinf(y[i+1]):
                    return {"success": False, "t": t[:i+2], "y": y[:i+2],
                            "error": f"Overflow ou NaN no passo i={i+1}, t={t[i+1]:.4f}"}
            except Exception as e:
                return {"success": False, "t": t[:i+2], "y": y[:i+2],
                        "error": f"Erro no passo i={i+1}: {str(e)}"}

        return {"success": True, "t": t, "y": y, "error": None}
    except Exception as e:
        return {"success": False, "t": None, "y": None,
                "error": f"Método falhou: {str(e)}"}


def runge_kutta_4(f, y0, t0, tf, h=0.1):
    """
    Runge-Kutta 4th order method for solving ODEs.

    Args:
        f: function dy/dt = f(t, y)
        y0: initial condition
        t0, tf: initial and final time
        h: step size

    Returns:
        dict with keys: success (bool), t (np.array), y (np.array), error (str or None)
    """
    try:
        y0 = float(y0)
        t0, tf = float(t0), float(tf)
        h = float(h)

        if h <= 0:
            return {"success": False, "t": None, "y": None,
                    "error": "Passo h deve ser maior que 0"}

        if tf <= t0:
            return {"success": False, "t": None, "y": None,
                    "error": "tf deve ser maior que t0"}

        if np.isnan(y0) or np.isinf(y0):
            return {"success": False, "t": None, "y": None,
                    "error": "y0 deve ser um valor finito"}

        n = int(np.ceil((tf - t0) / h)) + 1

        if n > 1000000:
            return {"success": False, "t": None, "y": None,
                    "error": "Número de passos muito grande. Reduza o intervalo ou aumente h."}

        t = np.linspace(t0, tf, n)
        actual_h = (tf - t0) / (n - 1) if n > 1 else h
        y = np.zeros(n)
        y[0] = y0

        for i in range(n - 1):
            try:
                k1 = f(t[i], y[i])
                k2 = f(t[i] + actual_h/2, y[i] + actual_h/2 * k1)
                k3 = f(t[i] + actual_h/2, y[i] + actual_h/2 * k2)
                k4 = f(t[i] + actual_h, y[i] + actual_h * k3)

                y[i+1] = y[i] + actual_h/6 * (k1 + 2*k2 + 2*k3 + k4)

                if np.isnan(y[i+1]) or np.isinf(y[i+1]):
                    return {"success": False, "t": t[:i+2], "y": y[:i+2],
                            "error": f"Overflow ou NaN no passo i={i+1}, t={t[i+1]:.4f}"}
            except Exception as e:
                return {"success": False, "t": t[:i+2], "y": y[:i+2],
                        "error": f"Erro no passo i={i+1}: {str(e)}"}

        return {"success": True, "t": t, "y": y, "error": None}
    except Exception as e:
        return {"success": False, "t": None, "y": None,
                "error": f"Método falhou: {str(e)}"}