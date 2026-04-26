"""Testes para integração numérica"""

import unittest
from core.integration import simpson, trapezoidal_repeated, three_eight_method


class TestIntegration(unittest.TestCase):
    """Testes para integração"""

    def test_simpson(self):
        """Teste Simpson: ∫₀² x² dx = 8/3 ≈ 2.667"""
        f = lambda x: x**2
        result = simpson(f, 0, 2, n=4)
        self.assertTrue(result["success"])
        self.assertAlmostEqual(result["result"], 8/3, places=3)

    def test_trapezoidal_repeated(self):
        """Teste Trapézio: ∫₀² x² dx = 8/3 ≈ 2.667"""
        f = lambda x: x**2
        result = trapezoidal_repeated(f, 0, 2, n=100)
        self.assertTrue(result["success"])
        self.assertAlmostEqual(result["result"], 8/3, places=2)

    def test_three_eight_method(self):
        """Teste 3/8: ∫₀³ x² dx = 9"""
        f = lambda x: x**2
        result = three_eight_method(f, 0, 3)
        self.assertTrue(result["success"])
        self.assertAlmostEqual(result["result"], 9.0, places=3)


if __name__ == "__main__":
    unittest.main()