"""Testes para métodos de raízes"""

import unittest
from core.roots import bisection, newton, secant


class TestRootsMethods(unittest.TestCase):
    """Testes para métodos de raízes"""

    def test_bisection_simple(self):
        """Teste bisecção: x^2 - 4 = 0, raiz em x=2"""
        f = lambda x: x**2 - 4
        result = bisection(f, 0, 3)
        self.assertTrue(result["success"])
        self.assertAlmostEqual(result["root"], 2.0, places=5)

    def test_bisection_no_sign_change(self):
        """Teste bisecção com erro: sem mudança de sinal"""
        f = lambda x: x**2 + 4
        result = bisection(f, -1, 1)
        self.assertFalse(result["success"])
        self.assertIn("não muda de sinal", result["error"])

    def test_newton_derivative_zero(self):
        """Teste Newton: derivada zero deve retornar erro descritivo"""
        f = lambda x: x**3
        df = lambda x: 3 * x**2
        result = newton(f, df, 0.0)
        self.assertFalse(result["success"])
        self.assertIn("derivada igual a zero", result["error"])

    def test_newton_converges(self):
        """Teste Newton: x^3 - 8 = 0, raiz em x=2"""
        f = lambda x: x**3 - 8
        df = lambda x: 3*x**2
        result = newton(f, df, 3.0)
        self.assertTrue(result["success"])
        self.assertAlmostEqual(result["root"], 2.0, places=5)

    def test_secant_converges(self):
        """Teste secante: x^2 - 4 = 0, raiz em x=2"""
        f = lambda x: x**2 - 4
        result = secant(f, 0, 3)
        self.assertTrue(result["success"])
        self.assertAlmostEqual(result["root"], 2.0, places=5)


if __name__ == "__main__":
    unittest.main()