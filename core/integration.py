"""
Integration: Simpson, Trapezoidal, and 3/8 methods
"""

import numpy as np


def simpson(f, a, b, n=4):
    """
    Simpson's 1/3 rule for numerical integration.

    Args:
        f: function to integrate
        a, b: integration interval [a, b]
        n: number of subintervals (must be even)

    Returns:
        dict with keys: success (bool), result (float or None), error (str or None)
    """
    try:
        a, b = float(a), float(b)
        n = int(n)

        if a == b:
            return {"success": True, "result": 0.0, "error": None}

        if n <= 0:
            return {"success": False, "result": None,
                    "error": "n deve ser maior que 0"}

        if n % 2 != 0:
            return {"success": False, "result": None,
                    "error": "n deve ser par para Simpson 1/3"}

        h = (b - a) / n
        x = np.linspace(a, b, n + 1)

        # Evaluate function
        y = np.array([f(xi) for xi in x])

        # Check for invalid values
        if np.any(np.isnan(y)) or np.any(np.isinf(y)):
            return {"success": False, "result": None,
                    "error": "Função retornou valores inválidos (NaN ou Inf)"}

        # Simpson's formula
        result = h / 3 * (y[0] + 2 * np.sum(y[2:-1:2]) + 4 * np.sum(y[1:-1:2]) + y[-1])

        return {"success": True, "result": result, "error": None}
    except Exception as e:
        return {"success": False, "result": None,
                "error": f"Método falhou: {str(e)}"}


def trapezoidal_repeated(f, a, b, n=4):
    """
    Repeated trapezoidal rule for numerical integration.

    Args:
        f: function to integrate
        a, b: integration interval [a, b]
        n: number of subintervals

    Returns:
        dict with keys: success (bool), result (float or None), error (str or None)
    """
    try:
        a, b = float(a), float(b)
        n = int(n)

        if a == b:
            return {"success": True, "result": 0.0, "error": None}

        if n <= 0:
            return {"success": False, "result": None,
                    "error": "n deve ser maior que 0"}

        h = (b - a) / n
        x = np.linspace(a, b, n + 1)
        y = np.array([f(xi) for xi in x])

        if np.any(np.isnan(y)) or np.any(np.isinf(y)):
            return {"success": False, "result": None,
                    "error": "Função retornou valores inválidos (NaN ou Inf)"}

        result = h * (y[0] / 2 + np.sum(y[1:-1]) + y[-1] / 2)

        return {"success": True, "result": result, "error": None}
    except Exception as e:
        return {"success": False, "result": None,
                "error": f"Método falhou: {str(e)}"}


def three_eight_method(f, a, b):
    """
    Simpson's 3/8 rule for numerical integration.

    Args:
        f: function to integrate
        a, b: integration interval [a, b]

    Returns:
        dict with keys: success (bool), result (float or None), error (str or None)
    """
    try:
        a, b = float(a), float(b)

        if a == b:
            return {"success": True, "result": 0.0, "error": None}

        if a >= b:
            return {"success": False, "result": None,
                    "error": "a deve ser menor que b"}

        h = (b - a) / 3

        x0 = a
        x1 = a + h
        x2 = a + 2 * h
        x3 = b

        y0 = f(x0)
        y1 = f(x1)
        y2 = f(x2)
        y3 = f(x3)

        for val in [y0, y1, y2, y3]:
            if np.isnan(val) or np.isinf(val):
                return {"success": False, "result": None,
                        "error": "Função retornou valores inválidos (NaN ou Inf)"}

        result = 3 * h / 8 * (y0 + 3 * y1 + 3 * y2 + y3)

        return {"success": True, "result": result, "error": None}
    except Exception as e:
        return {"success": False, "result": None,
                "error": f"Método falhou: {str(e)}"}