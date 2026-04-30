"""
Interpolation: Newton and Lagrange methods
"""

import numpy as np


def _divided_differences(x, y):
    """Calculate divided differences table for Newton interpolation."""
    n = len(x)
    table = np.zeros((n, n))
    table[:, 0] = y

    for j in range(1, n):
        for i in range(n - j):
            table[i][j] = (table[i+1][j-1] - table[i][j-1]) / (x[i+j] - x[i])

    return table


def newton_interpolation(x, y, x_eval):
    """
    Newton interpolation using divided differences.

    Args:
        x: array of x values (nodes)
        y: array of f(x) values
        x_eval: x value to evaluate the polynomial

    Returns:
        dict with keys: success (bool), result (float or None), coefficients (np.array), error (str or None)
    """
    try:
        x = np.array(x, dtype=float)
        y = np.array(y, dtype=float)
        x_eval = float(x_eval)

        if len(x) != len(y):
            return {"success": False, "result": None, "coefficients": None,
                    "error": "x e y devem ter o mesmo tamanho"}

        if len(x) < 2:
            return {"success": False, "result": None, "coefficients": None,
                    "error": "Mínimo de 2 pontos necessários"}

        if len(np.unique(x)) != len(x):
            return {"success": False, "result": None, "coefficients": None,
                    "error": "Valores de x devem ser únicos (sem duplicatas)"}

        if np.any(np.isnan(x)) or np.any(np.isinf(x)) or np.any(np.isnan(y)) or np.any(np.isinf(y)):
            return {"success": False, "result": None, "coefficients": None,
                    "error": "Valores de x ou y contêm NaN ou Inf"}

        n = len(x)
        table = _divided_differences(x, y)
        coefficients = [table[0, i] for i in range(n)]

        # Evaluate polynomial using Horner's method
        result = coefficients[-1]
        for i in range(n - 2, -1, -1):
            result = result * (x_eval - x[i]) + coefficients[i]

        return {"success": True, "result": result, "coefficients": np.array(coefficients), "error": None}
    except Exception as e:
        return {"success": False, "result": None, "coefficients": None,
                "error": f"Método falhou: {str(e)}"}


def lagrange_interpolation(x, y, x_eval):
    """
    Lagrange interpolation polynomial.

    Args:
        x: array of x values (nodes)
        y: array of f(x) values
        x_eval: x value to evaluate the polynomial

    Returns:
        dict with keys: success (bool), result (float or None), error (str or None)
    """
    try:
        x = np.array(x, dtype=float)
        y = np.array(y, dtype=float)
        x_eval = float(x_eval)

        if len(x) != len(y):
            return {"success": False, "result": None,
                    "error": "x e y devem ter o mesmo tamanho"}

        if len(x) < 2:
            return {"success": False, "result": None,
                    "error": "Mínimo de 2 pontos necessários"}

        if len(np.unique(x)) != len(x):
            return {"success": False, "result": None,
                    "error": "Valores de x devem ser únicos (sem duplicatas)"}

        if np.any(np.isnan(x)) or np.any(np.isinf(x)) or np.any(np.isnan(y)) or np.any(np.isinf(y)):
            return {"success": False, "result": None,
                    "error": "Valores de x ou y contêm NaN ou Inf"}

        # Shortcut: if x_eval equals a node, return the corresponding y value
        for i in range(len(x)):
            if x_eval == x[i]:
                return {"success": True, "result": float(y[i]), "error": None}

        n = len(x)
        result = 0.0

        for i in range(n):
            term = y[i]
            for j in range(n):
                if i != j:
                    term *= (x_eval - x[j]) / (x[i] - x[j])
            result += term

        return {"success": True, "result": result, "error": None}
    except Exception as e:
        return {"success": False, "result": None,
                "error": f"Método falhou: {str(e)}"}