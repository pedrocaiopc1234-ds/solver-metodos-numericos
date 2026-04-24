"""Validation module for interpolation methods."""

import numpy as np


def validate_interpolation_points(x, y):
    """Validate x and y arrays for interpolation."""
    try:
        x = np.array(x, dtype=float)
        y = np.array(y, dtype=float)

        if len(x) != len(y):
            return {"valid": False, "error": "x e y devem ter o mesmo tamanho"}

        if len(x) < 2:
            return {"valid": False, "error": "Mínimo de 2 pontos necessários"}

        if len(np.unique(x)) != len(x):
            return {"valid": False, "error": "Valores de x devem ser únicos"}

        return {"valid": True, "error": None}
    except Exception:
        return {"valid": False, "error": "x e y devem ser arrays numéricos"}


def validate_evaluation_point(x_eval, x_range=None):
    """Validate evaluation point."""
    try:
        x_eval = float(x_eval)
        if x_range is not None:
            if x_eval < x_range[0] or x_eval > x_range[1]:
                return {"valid": True, "error": "Aviso: x_eval fora do intervalo de x"}
        return {"valid": True, "error": None}
    except (TypeError, ValueError):
        return {"valid": False, "error": "x_eval deve ser numérico"}