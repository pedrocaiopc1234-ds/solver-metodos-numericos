"""Testes para interpolação"""

import unittest
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


if __name__ == "__main__":
    unittest.main()