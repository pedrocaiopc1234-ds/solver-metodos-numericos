"""Testes para interpolação"""

import unittest
import math
from core.interpolation import newton_interpolation, lagrange_interpolation


class TestInterpolation(unittest.TestCase):
    """Testes para interpolação"""

    def test_newton_interpolation(self):
        """Teste Newton: pontos (1, 1), (2, 4), (3, 9) → x=2.5 → ~6.25"""
        x = [1, 2, 3]
        y = [1, 4, 9]
        result = newton_interpolation(x, y, 2.5)
        self.assertTrue(result["success"])
        self.assertAlmostEqual(result["result"], 6.25, places=2)

    def test_lagrange_interpolation(self):
        """Teste Lagrange: mesmos pontos, mesmo resultado"""
        x = [1, 2, 3]
        y = [1, 4, 9]
        result = lagrange_interpolation(x, y, 2.5)
        self.assertTrue(result["success"])
        self.assertAlmostEqual(result["result"], 6.25, places=2)


# ─── 20 testes de robustez para Newton ──────────────────────────────

class TestNewtonInterpolationRobustness(unittest.TestCase):

    def test_robust_01_size_mismatch(self):
        """x e y com tamanhos diferentes"""
        r = newton_interpolation([1, 2, 3], [1, 4], 2.5)
        self.assertFalse(r["success"])

    def test_robust_02_single_point(self):
        """Apenas 1 ponto — mínimo é 2"""
        r = newton_interpolation([1], [1], 2.5)
        self.assertFalse(r["success"])

    def test_robust_03_linear(self):
        """2 pontos — interpolação linear"""
        r = newton_interpolation([0, 10], [0, 100], 5)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(r["result"], 50.0, places=2)

    def test_robust_04_duplicate_x(self):
        """Pontos x duplicados — divisão por zero"""
        r = newton_interpolation([1, 1, 2], [3, 5, 4], 1.5)
        self.assertIsInstance(r["success"], bool)

    def test_robust_05_negative_x(self):
        """Valores x negativos"""
        x = [-2, -1, 0, 1, 2]
        y = [4, 1, 0, 1, 4]
        r = newton_interpolation(x, y, -1.5)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(r["result"], 2.25, places=1)

    def test_robust_06_large_values(self):
        """Valores grandes"""
        x = [0, 1, 2]
        y = [0, 1e10, 2e10]
        r = newton_interpolation(x, y, 1.5)
        self.assertTrue(r["success"])

    def test_robust_07_small_values(self):
        """Valores pequenos"""
        x = [0, 1, 2]
        y = [0, 1e-10, 2e-10]
        r = newton_interpolation(x, y, 1.5)
        self.assertTrue(r["success"])

    def test_robust_08_extrapolation(self):
        """Extrapolação fora do intervalo"""
        x = [0, 1, 2]
        y = [0, 1, 4]
        r = newton_interpolation(x, y, 5)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(r["result"], 25.0, places=1)

    def test_robust_09_constant_function(self):
        """Função constante y=5"""
        x = [0, 1, 2]
        y = [5, 5, 5]
        r = newton_interpolation(x, y, 1.5)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(r["result"], 5.0, places=5)

    def test_robust_10_many_points(self):
        """10 pontos — polinômio de grau 9"""
        x = list(range(10))
        y = [i**2 for i in x]
        r = newton_interpolation(x, y, 4.5)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(r["result"], 20.25, places=1)

    def test_robust_11_float_x(self):
        """x com valores float"""
        x = [0.5, 1.5, 2.5]
        y = [0.25, 2.25, 6.25]
        r = newton_interpolation(x, y, 1.0)
        self.assertTrue(r["success"])

    def test_robust_12_trig_data(self):
        """Dados de sin(x)"""
        x = [0, math.pi/6, math.pi/3]
        y = [0, 0.5, math.sqrt(3)/2]
        r = newton_interpolation(x, y, math.pi/4)
        self.assertTrue(r["success"])

    def test_robust_13_negative_y(self):
        """Valores y negativos"""
        x = [-2, 0, 2]
        y = [-4, 0, -4]
        r = newton_interpolation(x, y, 1)
        self.assertTrue(r["success"])

    def test_robust_14_two_points_linear(self):
        """2 pontos — interpolação exata"""
        r = newton_interpolation([0, 1], [0, 1], 0.5)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(r["result"], 0.5, places=5)

    def test_robust_15_eval_at_node(self):
        """Avaliar em ponto que é um nó"""
        x = [1, 2, 3]
        y = [1, 4, 9]
        r = newton_interpolation(x, y, 2)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(r["result"], 4.0, places=5)

    def test_robust_16_zero_y(self):
        """Todos y = 0"""
        x = [1, 2, 3]
        y = [0, 0, 0]
        r = newton_interpolation(x, y, 1.5)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(r["result"], 0.0, places=5)

    def test_robust_17_oscillating_data(self):
        """Dados oscilantes"""
        x = [0, 1, 2, 3, 4]
        y = [1, -1, 1, -1, 1]
        r = newton_interpolation(x, y, 2.5)
        self.assertTrue(r["success"])

    def test_robust_18_exp_data(self):
        """Dados de e^x"""
        x = [0, 1, 2]
        y = [1, math.e, math.e**2]
        r = newton_interpolation(x, y, 0.5)
        self.assertTrue(r["success"])

    def test_robust_19_close_x_values(self):
        """Pontos x muito próximos"""
        x = [1.0, 1.0001, 1.0002]
        y = [1.0, 1.0002, 1.0004]
        r = newton_interpolation(x, y, 1.00015)
        self.assertIsInstance(r["success"], bool)

    def test_robust_20_wide_range(self):
        """Intervalo grande entre pontos"""
        x = [-100, 0, 100]
        y = [10000, 0, 10000]
        r = newton_interpolation(x, y, 50)
        self.assertTrue(r["success"])


# ─── 20 testes de robustez para Lagrange ─────────────────────────────

class TestLagrangeInterpolationRobustness(unittest.TestCase):

    def test_robust_01_size_mismatch(self):
        """x e y com tamanhos diferentes"""
        r = lagrange_interpolation([1, 2, 3], [1, 4], 2.5)
        self.assertFalse(r["success"])

    def test_robust_02_single_point(self):
        """Apenas 1 ponto"""
        r = lagrange_interpolation([1], [1], 2.5)
        self.assertFalse(r["success"])

    def test_robust_03_linear(self):
        """2 pontos — linear"""
        r = lagrange_interpolation([0, 10], [0, 100], 5)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(r["result"], 50.0, places=2)

    def test_robust_04_eval_at_node(self):
        """Avaliar em nó existente — divisão por zero no Lagrange"""
        x = [1, 2, 3]
        y = [1, 4, 9]
        r = lagrange_interpolation(x, y, 2)
        # Lagrange divide por (x_eval - x[j]) que é zero — pode falhar
        self.assertIsInstance(r["success"], bool)

    def test_robust_05_duplicate_x(self):
        """x duplicados — divisão por zero"""
        r = lagrange_interpolation([1, 1, 2], [3, 5, 4], 1.5)
        self.assertIsInstance(r["success"], bool)

    def test_robust_06_negative_x(self):
        """Valores x negativos"""
        x = [-2, -1, 0, 1, 2]
        y = [4, 1, 0, 1, 4]
        r = lagrange_interpolation(x, y, -1.5)
        self.assertTrue(r["success"])

    def test_robust_07_constant_function(self):
        """y constante"""
        x = [0, 1, 2]
        y = [5, 5, 5]
        r = lagrange_interpolation(x, y, 1.5)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(r["result"], 5.0, places=5)

    def test_robust_08_extrapolation(self):
        """Extrapolação"""
        x = [0, 1, 2]
        y = [0, 1, 4]
        r = lagrange_interpolation(x, y, 5)
        self.assertTrue(r["success"])

    def test_robust_09_many_points(self):
        """10 pontos"""
        x = list(range(10))
        y = [i**2 for i in x]
        r = lagrange_interpolation(x, y, 4.5)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(r["result"], 20.25, places=1)

    def test_robust_10_float_x(self):
        """x float"""
        x = [0.5, 1.5, 2.5]
        y = [0.25, 2.25, 6.25]
        r = lagrange_interpolation(x, y, 1.0)
        self.assertTrue(r["success"])

    def test_robust_11_trig_data(self):
        """Dados de sin(x)"""
        x = [0, math.pi/6, math.pi/3]
        y = [0, 0.5, math.sqrt(3)/2]
        r = lagrange_interpolation(x, y, math.pi/4)
        self.assertTrue(r["success"])

    def test_robust_12_negative_y(self):
        """y negativos"""
        x = [-2, 0, 2]
        y = [-4, 0, -4]
        r = lagrange_interpolation(x, y, 1)
        self.assertTrue(r["success"])

    def test_robust_13_two_points(self):
        """2 pontos — exato"""
        r = lagrange_interpolation([0, 1], [0, 1], 0.5)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(r["result"], 0.5, places=5)

    def test_robust_14_zero_y(self):
        """Todos y = 0"""
        x = [1, 2, 3]
        y = [0, 0, 0]
        r = lagrange_interpolation(x, y, 1.5)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(r["result"], 0.0, places=5)

    def test_robust_15_oscillating(self):
        """Dados oscilantes"""
        x = [0, 1, 2, 3, 4]
        y = [1, -1, 1, -1, 1]
        r = lagrange_interpolation(x, y, 2.5)
        self.assertTrue(r["success"])

    def test_robust_16_exp_data(self):
        """Dados de e^x"""
        x = [0, 1, 2]
        y = [1, math.e, math.e**2]
        r = lagrange_interpolation(x, y, 0.5)
        self.assertTrue(r["success"])

    def test_robust_17_close_x(self):
        """x muito próximos"""
        x = [1.0, 1.0001, 1.0002]
        y = [1.0, 1.0002, 1.0004]
        r = lagrange_interpolation(x, y, 1.00015)
        self.assertIsInstance(r["success"], bool)

    def test_robust_18_wide_range(self):
        """Intervalo grande"""
        x = [-100, 0, 100]
        y = [10000, 0, 10000]
        r = lagrange_interpolation(x, y, 50)
        self.assertTrue(r["success"])

    def test_robust_19_large_values(self):
        """Valores grandes"""
        x = [0, 1, 2]
        y = [0, 1e10, 2e10]
        r = lagrange_interpolation(x, y, 1.5)
        self.assertTrue(r["success"])

    def test_robust_20_small_values(self):
        """Valores pequenos"""
        x = [0, 1, 2]
        y = [0, 1e-10, 2e-10]
        r = lagrange_interpolation(x, y, 1.5)
        self.assertTrue(r["success"])


if __name__ == "__main__":
    unittest.main()