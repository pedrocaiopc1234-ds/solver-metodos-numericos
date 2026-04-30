"""Validation module for roots methods."""

import numpy as np


def validate_function(f):
    """Validate if f is a callable function."""
    if not callable(f):
        return {"valid": False, "error": "f deve ser uma função callable"}
    return {"valid": True, "error": None}


def validate_interval(a, b):
    """Validate that a < b for interval [a, b]."""
    try:
        a, b = float(a), float(b)
        if a >= b:
            return {"valid": False, "error": "a deve ser menor que b"}
        return {"valid": True, "error": None}
    except (TypeError, ValueError):
        return {"valid": False, "error": "a e b devem ser numéricos"}


def validate_tolerance(tol):
    """Validate tolerance > 0 and within reasonable bounds."""
    try:
        tol = float(tol)
        if tol <= 0:
            return {"valid": False, "error": "tolerância deve ser maior que 0"}
        if tol < 1e-15:
            return {"valid": False, "error": "tolerância muito pequena (mínimo: 1e-15). Use um valor maior para garantir convergência."}
        if tol > 1:
            return {"valid": False, "error": "tolerância muito grande (máximo: 1). Use um valor menor para resultados precisos."}
        return {"valid": True, "error": None}
    except (TypeError, ValueError):
        return {"valid": False, "error": "tolerância deve ser numérica"}


def validate_max_iterations(max_iter):
    """Validate max_iter is a positive integer within reasonable bounds."""
    try:
        max_iter = int(max_iter)
        if max_iter <= 0:
            return {"valid": False, "error": "max_iter deve ser maior que 0"}
        if max_iter > 10000:
            return {"valid": False, "error": "max_iter muito grande (máximo: 10000). Use um valor menor."}
        return {"valid": True, "error": None}
    except (TypeError, ValueError):
        return {"valid": False, "error": "max_iter deve ser um inteiro"}


def validate_initial_guess(x0):
    """Validate initial guess is a number."""
    try:
        float(x0)
        return {"valid": True, "error": None}
    except (TypeError, ValueError):
        return {"valid": False, "error": "x0 deve ser numérico"}