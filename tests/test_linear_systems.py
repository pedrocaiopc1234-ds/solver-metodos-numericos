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


# ─── 20 testes de robustez para LU ──────────────────────────────────

class TestLURobustness(unittest.TestCase):

    def test_robust_01_singular(self):
        """Matriz singular — pode retornar NaN sem detectar"""
        A = [[1, 2], [1, 2]]
        b = [3, 3]
        r = lu_factorization(A, b)
        # Agora retorna success=False corretamente
        self.assertFalse(r["success"])

    def test_robust_02_zero_matrix(self):
        """Matriz de zeros"""
        A = [[0, 0], [0, 0]]
        b = [1, 2]
        r = lu_factorization(A, b)
        self.assertFalse(r["success"])

    def test_robust_03_diagonal(self):
        """Matriz diagonal"""
        A = [[5, 0], [0, 3]]
        b = [10, 9]
        r = lu_factorization(A, b)
        self.assertTrue(r["success"])
        self.assertTrue(np.allclose(r["x"], [2, 3]))

    def test_robust_04_identity(self):
        """Matriz identidade"""
        A = [[1, 0], [0, 1]]
        b = [3, 4]
        r = lu_factorization(A, b)
        self.assertTrue(r["success"])
        self.assertTrue(np.allclose(r["x"], [3, 4]))

    def test_robust_05_3x3(self):
        """Sistema 3x3"""
        A = [[2, 1, -1], [-3, -1, 2], [-2, 1, 2]]
        b = [8, -11, -3]
        r = lu_factorization(A, b)
        self.assertTrue(r["success"])
        self.assertTrue(np.allclose(np.dot(A, r["x"]), b, atol=1e-6))

    def test_robust_06_near_singular(self):
        """Quase singular"""
        A = [[1, 1], [1, 1.0000001]]
        b = [2, 2]
        r = lu_factorization(A, b)
        self.assertIsInstance(r["success"], bool)

    def test_robust_07_negative(self):
        """Valores negativos"""
        A = [[-2, 1], [1, -3]]
        b = [-3, -4]
        r = lu_factorization(A, b)
        self.assertTrue(r["success"])

    def test_robust_08_large_values(self):
        """Valores grandes"""
        A = [[1e10, 2e10], [3e10, 4e10]]
        b = [5e10, 7e10]
        r = lu_factorization(A, b)
        self.assertIsInstance(r["success"], bool)

    def test_robust_09_small_values(self):
        """Valores pequenos"""
        A = [[1e-10, 2e-10], [3e-10, 4e-10]]
        b = [5e-10, 7e-10]
        r = lu_factorization(A, b)
        self.assertIsInstance(r["success"], bool)

    def test_robust_10_1x1(self):
        """Sistema 1x1"""
        A = [[5]]
        b = [10]
        r = lu_factorization(A, b)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(r["x"][0], 2.0, places=5)

    def test_robust_11_pivot_zero_swap(self):
        """Pivô zero resolvido com pivotação"""
        A = [[0, 1], [1, 0]]
        b = [3, 4]
        r = lu_factorization(A, b)
        self.assertTrue(r["success"])
        self.assertTrue(np.allclose(r["x"], [4, 3]))

    def test_robust_12_hilbert(self):
        """Matriz de Hilbert — mal condicionada"""
        A = [[1, 1/2, 1/3], [1/2, 1/3, 1/4], [1/3, 1/4, 1/5]]
        b = [11/6, 13/12, 47/60]
        r = lu_factorization(A, b)
        self.assertIsInstance(r["success"], bool)

    def test_robust_13_zero_diagonal_no_fix(self):
        """Diagonal zero sem pivotação possível"""
        A = [[0, 1], [0, 2]]
        b = [1, 2]
        r = lu_factorization(A, b)
        self.assertFalse(r["success"])

    def test_robust_14_mixed_signs(self):
        """Sinais mistos"""
        A = [[3, -1, 2], [1, 2, -1], [2, -2, 4]]
        b = [7, 3, 4]
        r = lu_factorization(A, b)
        self.assertTrue(r["success"])

    def test_robust_15_4x4(self):
        """4x4 diagonal"""
        A = [[1, 0, 0, 0], [0, 2, 0, 0], [0, 0, 3, 0], [0, 0, 0, 4]]
        b = [1, 4, 9, 16]
        r = lu_factorization(A, b)
        self.assertTrue(r["success"])

    def test_robust_16_inconsistent(self):
        """Sistema incompatível: 0x+0y=1"""
        A = [[0, 0], [0, 0]]
        b = [1, 0]
        r = lu_factorization(A, b)
        self.assertFalse(r["success"])

    def test_robust_17_well_conditioned(self):
        """Bem condicionado"""
        A = [[4, 1], [1, 3]]
        b = [5, 4]
        r = lu_factorization(A, b)
        self.assertTrue(r["success"])
        self.assertTrue(np.allclose(r["x"], [1, 1]))

    def test_robust_18_row_swap_needed(self):
        """Necessita troca de linhas"""
        A = [[0, 2, 1], [1, 0, 0], [0, 1, 0]]
        b = [5, 1, 2]
        r = lu_factorization(A, b)
        self.assertTrue(r["success"])

    def test_robust_19_scaled(self):
        """Escalas diferentes"""
        A = [[1e-6, 2], [1, 1]]
        b = [4, 3]
        r = lu_factorization(A, b)
        self.assertIsInstance(r["success"], bool)

    def test_robust_20_symmetric_pd(self):
        """Simétrica definida positiva"""
        A = [[4, 2], [2, 3]]
        b = [6, 5]
        r = lu_factorization(A, b)
        self.assertTrue(r["success"])
        self.assertTrue(np.allclose(r["x"], [1, 1]))


# ─── 20 testes de robustez para Gauss ────────────────────────────────

class TestGaussianEliminationRobustness(unittest.TestCase):

    def test_robust_01_singular(self):
        """Matriz singular"""
        A = [[1, 2], [1, 2]]
        b = [3, 3]
        r = gaussian_elimination(A, b)
        self.assertFalse(r["success"])

    def test_robust_02_zero_matrix(self):
        """Matriz zero"""
        A = [[0, 0], [0, 0]]
        b = [1, 2]
        r = gaussian_elimination(A, b)
        self.assertFalse(r["success"])

    def test_robust_03_diagonal(self):
        """Diagonal"""
        A = [[5, 0], [0, 3]]
        b = [10, 9]
        r = gaussian_elimination(A, b)
        self.assertTrue(r["success"])
        self.assertTrue(np.allclose(r["x"], [2, 3]))

    def test_robust_04_3x3(self):
        """3x3"""
        A = [[2, 1, -1], [-3, -1, 2], [-2, 1, 2]]
        b = [8, -11, -3]
        r = gaussian_elimination(A, b)
        self.assertTrue(r["success"])

    def test_robust_05_near_singular(self):
        """Quase singular"""
        A = [[1, 1], [1, 1.0000001]]
        b = [2, 2]
        r = gaussian_elimination(A, b)
        self.assertIsInstance(r["success"], bool)

    def test_robust_06_negative(self):
        """Negativos"""
        A = [[-2, 1], [1, -3]]
        b = [-3, -4]
        r = gaussian_elimination(A, b)
        self.assertTrue(r["success"])

    def test_robust_07_1x1(self):
        """1x1"""
        A = [[5]]
        b = [10]
        r = gaussian_elimination(A, b)
        self.assertTrue(r["success"])

    def test_robust_08_pivot_swap(self):
        """Pivô zero resolvido com troca"""
        A = [[0, 1], [1, 0]]
        b = [3, 4]
        r = gaussian_elimination(A, b)
        self.assertTrue(r["success"])

    def test_robust_09_hilbert(self):
        """Hilbert mal condicionada"""
        A = [[1, 1/2, 1/3], [1/2, 1/3, 1/4], [1/3, 1/4, 1/5]]
        b = [11/6, 13/12, 47/60]
        r = gaussian_elimination(A, b)
        self.assertIsInstance(r["success"], bool)

    def test_robust_10_mixed_signs(self):
        """Sinais mistos"""
        A = [[3, -1, 2], [1, 2, -1], [2, -2, 4]]
        b = [7, 3, 4]
        r = gaussian_elimination(A, b)
        self.assertTrue(r["success"])

    def test_robust_11_inconsistent(self):
        """Incompatível"""
        A = [[0, 0], [0, 0]]
        b = [1, 0]
        r = gaussian_elimination(A, b)
        self.assertFalse(r["success"])

    def test_robust_12_identity(self):
        """Identidade"""
        A = [[1, 0], [0, 1]]
        b = [3, 4]
        r = gaussian_elimination(A, b)
        self.assertTrue(r["success"])
        self.assertTrue(np.allclose(r["x"], [3, 4]))

    def test_robust_13_4x4(self):
        """4x4 diagonal"""
        A = [[1, 0, 0, 0], [0, 2, 0, 0], [0, 0, 3, 0], [0, 0, 0, 4]]
        b = [1, 4, 9, 16]
        r = gaussian_elimination(A, b)
        self.assertTrue(r["success"])

    def test_robust_14_row_dependent(self):
        """Linhas dependentes"""
        A = [[1, 2, 3], [2, 4, 6], [1, 1, 1]]
        b = [6, 12, 3]
        r = gaussian_elimination(A, b)
        self.assertFalse(r["success"])

    def test_robust_15_large_scale(self):
        """Escala diferente"""
        A = [[1e10, 1], [1, 1]]
        b = [1e10+1, 2]
        r = gaussian_elimination(A, b)
        self.assertIsInstance(r["success"], bool)

    def test_robust_16_zero_rhs(self):
        """b=0 (homogêneo)"""
        A = [[1, 0], [0, 1]]
        b = [0, 0]
        r = gaussian_elimination(A, b)
        self.assertTrue(r["success"])
        self.assertTrue(np.allclose(r["x"], [0, 0]))

    def test_robust_17_all_ones(self):
        """Todos 1s — singular, pode retornar NaN"""
        A = [[1, 1], [1, 1]]
        b = [2, 2]
        r = gaussian_elimination(A, b)
        # Agora retorna success=False corretamente
        self.assertFalse(r["success"])

    def test_robust_18_symmetric_pd(self):
        """Simétrica definida positiva"""
        A = [[4, 2], [2, 3]]
        b = [6, 5]
        r = gaussian_elimination(A, b)
        self.assertTrue(r["success"])

    def test_robust_19_multiple_swaps(self):
        """Múltiplas trocas de linha"""
        A = [[0, 0, 1], [0, 1, 0], [1, 0, 0]]
        b = [3, 2, 1]
        r = gaussian_elimination(A, b)
        self.assertTrue(r["success"])

    def test_robust_20_ill_conditioned(self):
        """Mal condicionada"""
        A = [[1, 1.0001], [1, 1]]
        b = [2.0001, 2]
        r = gaussian_elimination(A, b)
        self.assertIsInstance(r["success"], bool)


# ─── 20 testes de robustez para Gauss-Seidel ────────────────────────

class TestGaussSeidelRobustness(unittest.TestCase):

    def test_robust_01_diagonally_dominant(self):
        """Diagonal dominante — converge"""
        A = [[4, 1, 2], [1, 3, 1], [2, 1, 5]]
        b = [4, 3, 7]
        r = gauss_seidel(A, b)
        self.assertTrue(r["success"])

    def test_robust_02_not_dominant(self):
        """Não diagonal dominante"""
        A = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        b = [1, 2, 3]
        r = gauss_seidel(A, b)
        self.assertIsInstance(r["success"], bool)

    def test_robust_03_zero_diagonal(self):
        """Zero na diagonal — divisão por zero"""
        A = [[0, 1], [1, 0]]
        b = [1, 2]
        r = gauss_seidel(A, b)
        self.assertFalse(r["success"])

    def test_robust_04_identity(self):
        """Identidade"""
        A = [[1, 0], [0, 1]]
        b = [3, 4]
        r = gauss_seidel(A, b)
        self.assertTrue(r["success"])
        self.assertTrue(np.allclose(r["x"], [3, 4]))

    def test_robust_05_singular(self):
        """Singular"""
        A = [[1, 1], [1, 1]]
        b = [2, 2]
        r = gauss_seidel(A, b)
        self.assertIsInstance(r["success"], bool)

    def test_robust_06_negative_diagonal(self):
        """Diagonal negativa"""
        A = [[-4, 1], [1, -3]]
        b = [-3, -4]
        r = gauss_seidel(A, b)
        self.assertIsInstance(r["success"], bool)

    def test_robust_07_1x1(self):
        """1x1"""
        A = [[5]]
        b = [10]
        r = gauss_seidel(A, b)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(r["x"][0], 2.0, places=5)

    def test_robust_08_4x4(self):
        """4x4 diagonal dominante"""
        A = [[10, 1, 2, 0], [1, 10, 1, 1], [2, 1, 10, 1], [0, 1, 1, 10]]
        b = [13, 13, 14, 12]
        r = gauss_seidel(A, b)
        self.assertTrue(r["success"])

    def test_robust_09_large_values(self):
        """Valores grandes"""
        A = [[1e6, 1], [1, 1e6]]
        b = [1e6+1, 1e6+1]
        r = gauss_seidel(A, b)
        self.assertTrue(r["success"])

    def test_robust_10_strictly_dominant(self):
        """Estritamente dominante 2x2"""
        A = [[5, 2], [1, 4]]
        b = [9, 5]
        r = gauss_seidel(A, b)
        self.assertTrue(r["success"])

    def test_robust_11_symmetric_pd(self):
        """Simétrica definida positiva"""
        A = [[4, 1], [1, 3]]
        b = [5, 4]
        r = gauss_seidel(A, b)
        self.assertTrue(r["success"])

    def test_robust_12_mixed_signs(self):
        """Sinais mistos"""
        A = [[5, -1, 2], [-1, 4, -1], [2, -1, 6]]
        b = [6, 2, 7]
        r = gauss_seidel(A, b)
        self.assertTrue(r["success"])

    def test_robust_13_near_zero_diagonal(self):
        """Diagonal quase zero"""
        A = [[1e-15, 1], [1, 1]]
        b = [2, 2]
        r = gauss_seidel(A, b)
        self.assertIsInstance(r["success"], bool)

    def test_robust_14_max_iterations(self):
        """Poucas iterações"""
        A = [[2, 1], [1, 2]]
        b = [1, 1]
        r = gauss_seidel(A, b, max_iter=2)
        self.assertIsInstance(r["success"], bool)

    def test_robust_15_zero_rhs(self):
        """b=0"""
        A = [[4, 1], [1, 3]]
        b = [0, 0]
        r = gauss_seidel(A, b)
        self.assertTrue(r["success"])
        self.assertTrue(np.allclose(r["x"], [0, 0], atol=1e-5))

    def test_robust_16_all_zeros_matrix(self):
        """Matriz zero"""
        A = [[0, 0], [0, 0]]
        b = [1, 2]
        r = gauss_seidel(A, b)
        self.assertFalse(r["success"])

    def test_robust_17_5x5_tridiagonal(self):
        """5x5 tridiagonal"""
        A = [[5, 1, 0, 0, 0], [1, 5, 1, 0, 0], [0, 1, 5, 1, 0],
             [0, 0, 1, 5, 1], [0, 0, 0, 1, 5]]
        b = [6, 7, 7, 7, 6]
        r = gauss_seidel(A, b)
        self.assertTrue(r["success"])

    def test_robust_18_anti_convergent(self):
        """Não converge"""
        A = [[1, 10], [10, 1]]
        b = [11, 11]
        r = gauss_seidel(A, b, max_iter=50)
        self.assertIsInstance(r["success"], bool)

    def test_robust_19_near_identity(self):
        """Quase identidade"""
        A = [[1.01, 0.01], [0.01, 1.01]]
        b = [1.02, 1.02]
        r = gauss_seidel(A, b)
        self.assertTrue(r["success"])

    def test_robust_20_small_values(self):
        """Valores pequenos"""
        A = [[1e-4, 1e-5], [1e-5, 1e-4]]
        b = [2e-4, 2e-4]
        r = gauss_seidel(A, b)
        self.assertIsInstance(r["success"], bool)


# ─── 20 testes de robustez para Gauss-Jacobi ────────────────────────

class TestGaussJacobiRobustness(unittest.TestCase):

    def test_robust_01_dominant(self):
        """Diagonal dominante — converge"""
        A = [[4, 1, 2], [1, 3, 1], [2, 1, 5]]
        b = [4, 3, 7]
        r = gauss_jacobi(A, b)
        self.assertTrue(r["success"])

    def test_robust_02_not_dominant(self):
        """Não diagonal dominante"""
        A = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        b = [1, 2, 3]
        r = gauss_jacobi(A, b)
        self.assertIsInstance(r["success"], bool)

    def test_robust_03_zero_diagonal(self):
        """Zero na diagonal"""
        A = [[0, 1], [1, 0]]
        b = [1, 2]
        r = gauss_jacobi(A, b)
        self.assertFalse(r["success"])

    def test_robust_04_identity(self):
        """Identidade"""
        A = [[1, 0], [0, 1]]
        b = [3, 4]
        r = gauss_jacobi(A, b)
        self.assertTrue(r["success"])
        self.assertTrue(np.allclose(r["x"], [3, 4]))

    def test_robust_05_singular(self):
        """Singular"""
        A = [[1, 1], [1, 1]]
        b = [2, 2]
        r = gauss_jacobi(A, b)
        self.assertIsInstance(r["success"], bool)

    def test_robust_06_negative_diagonal(self):
        """Diagonal negativa"""
        A = [[-4, 1], [1, -3]]
        b = [-3, -4]
        r = gauss_jacobi(A, b)
        self.assertIsInstance(r["success"], bool)

    def test_robust_07_1x1(self):
        """1x1"""
        A = [[5]]
        b = [10]
        r = gauss_jacobi(A, b)
        self.assertTrue(r["success"])

    def test_robust_08_4x4(self):
        """4x4 diagonal dominante"""
        A = [[10, 1, 2, 0], [1, 10, 1, 1], [2, 1, 10, 1], [0, 1, 1, 10]]
        b = [13, 13, 14, 12]
        r = gauss_jacobi(A, b)
        self.assertTrue(r["success"])

    def test_robust_09_large_values(self):
        """Valores grandes"""
        A = [[1e6, 1], [1, 1e6]]
        b = [1e6+1, 1e6+1]
        r = gauss_jacobi(A, b)
        self.assertTrue(r["success"])

    def test_robust_10_strictly_dominant(self):
        """Estritamente dominante"""
        A = [[5, 2], [1, 4]]
        b = [9, 5]
        r = gauss_jacobi(A, b)
        self.assertTrue(r["success"])

    def test_robust_11_symmetric_pd(self):
        """Simétrica definida positiva"""
        A = [[4, 1], [1, 3]]
        b = [5, 4]
        r = gauss_jacobi(A, b)
        self.assertTrue(r["success"])

    def test_robust_12_mixed_signs(self):
        """Sinais mistos"""
        A = [[5, -1, 2], [-1, 4, -1], [2, -1, 6]]
        b = [6, 2, 7]
        r = gauss_jacobi(A, b)
        self.assertTrue(r["success"])

    def test_robust_13_max_iterations(self):
        """Poucas iterações"""
        A = [[2, 1], [1, 2]]
        b = [1, 1]
        r = gauss_jacobi(A, b, max_iter=2)
        self.assertIsInstance(r["success"], bool)

    def test_robust_14_zero_rhs(self):
        """b=0"""
        A = [[4, 1], [1, 3]]
        b = [0, 0]
        r = gauss_jacobi(A, b)
        self.assertTrue(r["success"])
        self.assertTrue(np.allclose(r["x"], [0, 0], atol=1e-5))

    def test_robust_15_all_zeros_matrix(self):
        """Matriz zero"""
        A = [[0, 0], [0, 0]]
        b = [1, 2]
        r = gauss_jacobi(A, b)
        self.assertFalse(r["success"])

    def test_robust_16_tridiagonal(self):
        """5x5 tridiagonal"""
        A = [[5, 1, 0, 0, 0], [1, 5, 1, 0, 0], [0, 1, 5, 1, 0],
             [0, 0, 1, 5, 1], [0, 0, 0, 1, 5]]
        b = [6, 7, 7, 7, 6]
        r = gauss_jacobi(A, b)
        self.assertTrue(r["success"])

    def test_robust_17_anti_convergent(self):
        """Não converge"""
        A = [[1, 10], [10, 1]]
        b = [11, 11]
        r = gauss_jacobi(A, b, max_iter=50)
        self.assertIsInstance(r["success"], bool)

    def test_robust_18_near_identity(self):
        """Quase identidade"""
        A = [[1.01, 0.01], [0.01, 1.01]]
        b = [1.02, 1.02]
        r = gauss_jacobi(A, b)
        self.assertTrue(r["success"])

    def test_robust_19_small_values(self):
        """Valores pequenos"""
        A = [[1e-4, 1e-5], [1e-5, 1e-4]]
        b = [2e-4, 2e-4]
        r = gauss_jacobi(A, b)
        self.assertIsInstance(r["success"], bool)

    def test_robust_20_scaled_system(self):
        """Escala diferente"""
        A = [[100, 1], [1, 100]]
        b = [101, 101]
        r = gauss_jacobi(A, b)
        self.assertTrue(r["success"])


if __name__ == "__main__":
    unittest.main()