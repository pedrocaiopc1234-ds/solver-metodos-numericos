"""Validation module for ODE methods."""

import numpy as np


def validate_ode_function(f):
    """Validate if f(t, y) is a callable function."""
    if not callable(f):
        return {"valid": False, "error": "f deve ser uma função callable f(t, y)"}
    return {"valid": True, "error": None}


def validate_initial_condition(y0):
    """Validate initial condition y0."""
    try:
        float(y0)
        return {"valid": True, "error": None}
    except (TypeError, ValueError):
        return {"valid": False, "error": "y0 deve ser numérico"}


def validate_time_interval(t0, tf):
    """Validate time interval [t0, tf]."""
    try:
        t0, tf = float(t0), float(tf)
        if t0 >= tf:
            return {"valid": False, "error": "t0 deve ser menor que tf"}
        return {"valid": True, "error": None}
    except (TypeError, ValueError):
        return {"valid": False, "error": "t0 e tf devem ser numéricos"}


def validate_step_size(h):
    """Validate step size h > 0."""
    try:
        h = float(h)
        if h <= 0:
            return {"valid": False, "error": "h deve ser maior que 0"}
        return {"valid": True, "error": None}
    except (TypeError, ValueError):
        return {"valid": False, "error": "h deve ser numérico"}