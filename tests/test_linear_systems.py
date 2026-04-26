"""Testes para sistemas lineares"""

import unittest
import numpy as np
from core.linear_systems import lu_factorization, gaussian_elimination, gauss_seidel, gauss_jacobi


class TestLinearSystems(unittest.TestCase):
    """Testes para sistemas lineares"""

    def test_lu_factorization(self):
        """Teste LU: A = [[2, 1], [1, 3]], b = [3, 4] → x = [1, 1]"""
        A = [[2, 1], [1, 3]]
        b = [3, 4]
        result = lu_factorization(A, b)
        self.assertTrue(result["success"])
        self.assertTrue(np.allclose(result["x"], [1, 1]))

    def test_gaussian_elimination(self):
        """Teste Gauss: mesma matriz, mesmo resultado"""
        A = [[2, 1], [1, 3]]
        b = [3, 4]
        result = gaussian_elimination(A, b)
        self.assertTrue(result["success"])
        self.assertTrue(np.allclose(result["x"], [1, 1]))

    def test_gauss_seidel_converges(self):
        """Teste Gauss-Seidel converge para matriz diagonal dominante"""
        A = [[4, 1, 2], [1, 3, 1], [2, 1, 5]]
        b = [4, 3, 7]
        result = gauss_seidel(A, b, tol=1e-10)
        self.assertTrue(result["success"])
        x = result["x"]
        self.assertTrue(np.allclose(np.dot(A, x), b, atol=1e-6))

    def test_gauss_jacobi_converges(self):
        """Teste Gauss-Jacobi converge para matriz diagonal dominante"""
        A = [[4, 1, 2], [1, 3, 1], [2, 1, 5]]
        b = [4, 3, 7]
        result = gauss_jacobi(A, b, tol=1e-10)
        self.assertTrue(result["success"])


if __name__ == "__main__":
    unittest.main()