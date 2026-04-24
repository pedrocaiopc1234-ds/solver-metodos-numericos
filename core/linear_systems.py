"""
Linear Systems: LU Factorization, Gaussian Elimination, Gauss-Seidel, Gauss-Jacobi
"""

import numpy as np


def lu_factorization(A, b):
    """
    LU Factorization with partial pivoting.

    Returns:
        dict with keys: success (bool), x (np.array or None), L (np.array), U (np.array), error (str or None)
    """
    try:
        A = np.array(A, dtype=float)
        b = np.array(b, dtype=float)
        n = len(A)

        U = A.copy()
        L = np.eye(n)

        for k in range(n - 1):
            # Partial pivoting
            max_val = abs(U[k:, k])
            max_idx = np.argmax(max_val) + k
            if max_val[max_idx - k] < 1e-14:
                return {"success": False, "x": None, "L": None, "U": None,
                        "error": "Matriz singular ou quase singular (pivô zero)"}
            if max_idx != k:
                U[[k, max_idx]] = U[[max_idx, k]]
                b[[k, max_idx]] = b[[max_idx, k]]
                if k > 0:
                    L[[k, max_idx], :k] = L[[max_idx, k], :k]

            for i in range(k + 1, n):
                if U[k, k] == 0:
                    return {"success": False, "x": None, "L": None, "U": None,
                            "error": "Pivô zero durante eliminação"}
                L[i, k] = U[i, k] / U[k, k]
                U[i, k:] -= L[i, k] * U[k, k:]
                b[i] -= L[i, k] * b[k]

        # Back substitution
        x = np.zeros(n)
        x[n-1] = b[n-1] / U[n-1, n-1]
        for i in range(n - 2, -1, -1):
            if U[i, i] == 0:
                return {"success": False, "x": None, "L": None, "U": None,
                        "error": "Divisão por zero na retrosubstituição"}
            x[i] = (b[i] - np.dot(U[i, i+1:], x[i+1:])) / U[i, i]

        return {"success": True, "x": x, "L": L, "U": U, "error": None}
    except Exception as e:
        return {"success": False, "x": None, "L": None, "U": None,
                "error": f"Método falhou: {str(e)}"}


def gaussian_elimination(A, b):
    """
    Gaussian Elimination with back substitution.

    Returns:
        dict with keys: success (bool), x (np.array or None), error (str or None)
    """
    try:
        A = np.array(A, dtype=float)
        b = np.array(b, dtype=float)
        n = len(A)

        # Augmented matrix
        aug = np.column_stack([A, b])

        # Forward elimination
        for k in range(n - 1):
            max_val = abs(aug[k:, k])
            max_idx = np.argmax(max_val) + k
            if max_val[max_idx - k] < 1e-14:
                return {"success": False, "x": None,
                        "error": "Matriz singular ou quase singular"}
            if max_idx != k:
                aug[[k, max_idx]] = aug[[max_idx, k]]

            for i in range(k + 1, n):
                if aug[k, k] == 0:
                    return {"success": False, "x": None,
                            "error": "Pivô zero durante eliminação"}
                factor = aug[i, k] / aug[k, k]
                aug[i] -= factor * aug[k]

        # Back substitution
        x = np.zeros(n)
        x[n-1] = aug[n-1, n-1] / aug[n-1, n-1]
        for i in range(n - 2, -1, -1):
            if aug[i, i] == 0:
                return {"success": False, "x": None,
                        "error": "Divisão por zero na retrosubstituição"}
            x[i] = (aug[i, n] - np.dot(aug[i, i+1:n], x[i+1:])) / aug[i, i]

        return {"success": True, "x": x, "error": None}
    except Exception as e:
        return {"success": False, "x": None,
                "error": f"Método falhou: {str(e)}"}


def gauss_seidel(A, b, tol=1e-10, max_iter=100):
    """
    Gauss-Seidel iterative method.

    Returns:
        dict with keys: success (bool), x (np.array or None), iterations (int), error (str or None)
    """
    try:
        A = np.array(A, dtype=float)
        b = np.array(b, dtype=float)
        n = len(A)
        x = np.zeros(n)

        for iteration in range(max_iter):
            x_old = x.copy()
            for i in range(n):
                sigma = np.dot(A[i, :i], x[:i]) + np.dot(A[i, i+1:], x_old[i+1:])
                if A[i, i] == 0:
                    return {"success": False, "x": None, "iterations": iteration,
                            "error": f"Divisão por zero: A[{i},{i}] = 0"}
                x[i] = (b[i] - sigma) / A[i, i]

            if np.linalg.norm(x - x_old) < tol:
                return {"success": True, "x": x, "iterations": iteration + 1, "error": None}

        return {"success": False, "x": x, "iterations": max_iter,
                "error": "Máximo de iterações atingido sem convergência"}
    except Exception as e:
        return {"success": False, "x": None, "iterations": 0,
                "error": f"Método falhou: {str(e)}"}


def gauss_jacobi(A, b, tol=1e-10, max_iter=100):
    """
    Gauss-Jacobi iterative method.

    Returns:
        dict with keys: success (bool), x (np.array or None), iterations (int), error (str or None)
    """
    try:
        A = np.array(A, dtype=float)
        b = np.array(b, dtype=float)
        n = len(A)
        x = np.zeros(n)

        for iteration in range(max_iter):
            x_old = x.copy()
            for i in range(n):
                sigma = np.dot(A[i, :i], x_old[:i]) + np.dot(A[i, i+1:], x_old[i+1:])
                if A[i, i] == 0:
                    return {"success": False, "x": None, "iterations": iteration,
                            "error": f"Divisão por zero: A[{i},{i}] = 0"}
                x[i] = (b[i] - sigma) / A[i, i]

            if np.linalg.norm(x - x_old) < tol:
                return {"success": True, "x": x, "iterations": iteration + 1, "error": None}

        return {"success": False, "x": x, "iterations": max_iter,
                "error": "Método não converge para este sistema"}
    except Exception as e:
        return {"success": False, "x": None, "iterations": 0,
                "error": f"Método falhou: {str(e)}"}