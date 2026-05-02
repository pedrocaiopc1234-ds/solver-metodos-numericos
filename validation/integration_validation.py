"""Validation module for integration methods."""

import numpy as np


def validate_function(f):
    """Validate if f is a callable function."""
    if not callable(f):
        return {"valid": False, "error": "f deve ser uma função callable"}
    return {"valid": True, "error": None}


def validate_integration_interval(a, b):
    """Validate integration interval [a, b]."""
    try:
        a, b = float(a), float(b)
        if a >= b:
            return {"valid": False, "error": "a deve ser menor que b"}
        return {"valid": True, "error": None}
    except (TypeError, ValueError):
        return {"valid": False, "error": "a e b devem ser numéricos"}


def validate_subintervals(n, must_be_even=False, must_be_multiple_of_3=False):
    """Validate number of subintervals.

    Args:
        n: number of subintervals
        must_be_even: if True, n must be even (for Simpson 1/3)
        must_be_multiple_of_3: if True, n must be multiple of 3 (for Simpson 3/8)
    """
    try:
        n = int(n)
        if n <= 0:
            return {"valid": False, "error": "'n' deve ser maior que 0"}
        if must_be_even and n % 2 != 0:
            return {"valid": False, "error": "'n' deve ser par para Simpson 1/3"}
        if must_be_multiple_of_3 and n % 3 != 0:
            return {"valid": False, "error": "'n' deve ser múltiplo de 3 para Simpson 3/8"}
        return {"valid": True, "error": None}
    except (TypeError, ValueError):
        return {"valid": False, "error": "'n' deve ser um inteiro"}