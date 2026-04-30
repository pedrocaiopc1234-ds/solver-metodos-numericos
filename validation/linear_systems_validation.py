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
        if A.shape[0] < 1:
            return {"valid": False, "error": "A deve ter pelo menos 1 linha"}
        if A.shape[0] > 100:
            return {"valid": False, "error": "Matriz muito grande (máximo: 100x100)"}
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


def validate_iterative_params(tol, max_iter):
    """Validate tolerance and max iterations for iterative methods."""
    errors = []
    try:
        tol = float(tol)
        if tol <= 0:
            errors.append("Tolerância deve ser maior que 0")
        elif tol < 1e-15:
            errors.append("Tolerância muito pequena (mínimo: 1e-15)")
        elif tol > 1:
            errors.append("Tolerância muito grande (máximo: 1)")
    except (TypeError, ValueError):
        errors.append("Tolerância deve ser numérica")

    try:
        max_iter = int(max_iter)
        if max_iter <= 0:
            errors.append("Máximo de iterações deve ser maior que 0")
        elif max_iter > 10000:
            errors.append("Máximo de iterações muito grande (máximo: 10000)")
    except (TypeError, ValueError):
        errors.append("Máximo de iterações deve ser um inteiro")

    return errors