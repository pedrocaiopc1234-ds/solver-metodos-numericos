"""Validation module for linear systems methods."""

import numpy as np


def validate_matrix(A):
    """Validate that A is a square numerical matrix."""
    try:
        A = np.array(A, dtype=float)
        if A.ndim != 2:
            return {"valid": False, "error": "A deve ser uma matriz 2D"}
        if A.shape[0] != A.shape[1]:
            return {"valid": False, "error": "A deve ser uma matriz quadrada"}
        return {"valid": True, "error": None}
    except Exception:
        return {"valid": False, "error": "A deve ser uma matriz numérica"}


def validate_vector(b, n=None):
    """Validate that b is a numerical vector of size n."""
    try:
        b = np.array(b, dtype=float)
        if b.ndim != 1:
            return {"valid": False, "error": "b deve ser um vetor 1D"}
        if n is not None and len(b) != n:
            return {"valid": False, "error": f"b deve ter tamanho {n}"}
        return {"valid": True, "error": None}
    except Exception:
        return {"valid": False, "error": "b deve ser um vetor numérico"}


def validate_matrix_vector_dimensions(A, b):
    """Validate that A and b have compatible dimensions."""
    try:
        A = np.array(A, dtype=float)
        b = np.array(b, dtype=float)
        n = A.shape[0]
        if A.shape[1] != n:
            return {"valid": False, "error": "A deve ser quadrada"}
        if len(b) != n:
            return {"valid": False, "error": f"Dimensões incompatíveis: A({n}x{n}), b({len(b)})"}
        return {"valid": True, "error": None}
    except Exception:
        return {"valid": False, "error": "Matriz e vetor devem ser numéricos"}