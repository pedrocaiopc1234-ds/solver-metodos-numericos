"""
Testes para os métodos numéricos implementados em core/ e validation/
Executar com: PYTHONPATH=. python tests/test.py -v
"""

import unittest
import math
import numpy as np
from core.roots import bisection, newton, secant
from core.linear_systems import lu_factorization, gaussian_elimination, gauss_seidel, gauss_jacobi
from core.interpolation import newton_interpolation, lagrange_interpolation
from core.integration import simpson, trapezoidal_repeated, three_eight_method
from core.ode import euler_method, runge_kutta_4
from core.plot import (
    plot_bisection,
    plot_newton,
    plot_secant,
    plot_newton_interpolation,
    plot_lagrange_interpolation,
    plot_simpson,
    plot_trapezoidal,
    plot_three_eight,
)

import plotly.graph_objects as go


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
        # Verify solution by checking Ax ≈ b
        x = result["x"]
        self.assertTrue(np.allclose(np.dot(A, x), b, atol=1e-6))

    def test_gauss_jacobi_converges(self):
        """Teste Gauss-Jacobi converge para matriz diagonal dominante"""
        A = [[4, 1, 2], [1, 3, 1], [2, 1, 5]]
        b = [4, 3, 7]
        result = gauss_jacobi(A, b, tol=1e-10)
        self.assertTrue(result["success"])


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


class TestODE(unittest.TestCase):
    """Testes para EDO"""

    def test_euler_method(self):
        """Teste Euler: dy/dt = y, y(0)=1 → y(t) = e^t"""
        f = lambda t, y: y
        result = euler_method(f, y0=1.0, t0=0, tf=0.5, h=0.1)
        self.assertTrue(result["success"])
        self.assertTrue(np.isclose(result["y"][-1], math.exp(0.5), atol=0.1))

    def test_runge_kutta_4(self):
        """Teste RK4: dy/dt = y, y(0)=1 → y(t) = e^t"""
        f = lambda t, y: y
        result = runge_kutta_4(f, y0=1.0, t0=0, tf=0.5, h=0.1)
        self.assertTrue(result["success"])
        self.assertTrue(np.isclose(result["y"][-1], math.exp(0.5), atol=0.01))


class TestPlots(unittest.TestCase):
    """Testes para funções de plot"""

    def test_plot_bisection(self):
        f = lambda x: x**2 - 4
        fig = plot_bisection(f, 0, 3, root=2.0, iterations=10)
        self.assertIsInstance(fig, go.Figure)

    def test_plot_newton(self):
        f = lambda x: x**2 - 4
        df = lambda x: 2*x
        iterations_data = [
            {"x": 3.0, "fx": f(3.0), "dfx": df(3.0), "x_next": 2.1667},
            {"x": 2.1667, "fx": f(2.1667), "dfx": df(2.1667), "x_next": 2.0064},
        ]
        fig = plot_newton(f, df, 3.0, root=2.0, iterations_data=iterations_data)
        self.assertIsInstance(fig, go.Figure)

    def test_plot_secant(self):
        f = lambda x: x**2 - 4
        iterations_data = [
            {"x0": 0.0, "x1": 3.0, "f0": f(0.0), "f1": f(3.0), "x2": 1.3333},
        ]
        fig = plot_secant(f, 0.0, 3.0, root=2.0, iterations_data=iterations_data)
        self.assertIsInstance(fig, go.Figure)

    def test_plot_newton_interpolation(self):
        x_nodes = [1, 2, 3]
        y_nodes = [1, 4, 9]
        coefficients = [1.0, 3.0, 1.0]
        fig, info = plot_newton_interpolation(x_nodes, y_nodes, coefficients, x_eval=2.5, y_eval=6.25)
        self.assertIsInstance(fig, go.Figure)
        self.assertIn("polynomial_string", info)
        self.assertIn("coefficients", info)
        self.assertEqual(info["degree"], 2)

    def test_plot_lagrange_interpolation(self):
        x_nodes = [1, 2, 3]
        y_nodes = [1, 4, 9]
        fig, info = plot_lagrange_interpolation(x_nodes, y_nodes, x_eval=2.5, y_eval=6.25)
        self.assertIsInstance(fig, go.Figure)
        self.assertIn("polynomial_string", info)
        self.assertIn("basis_strings", info)
        self.assertEqual(info["degree"], 2)

    def test_plot_simpson(self):
        f = lambda x: x**2
        fig = plot_simpson(f, 0, 2, n=4, result=8/3)
        self.assertIsInstance(fig, go.Figure)

    def test_plot_trapezoidal(self):
        f = lambda x: x**2
        fig = plot_trapezoidal(f, 0, 2, n=4, result=8/3)
        self.assertIsInstance(fig, go.Figure)

    def test_plot_three_eight(self):
        f = lambda x: x**2
        fig = plot_three_eight(f, 0, 3, result=9.0)
        self.assertIsInstance(fig, go.Figure)


if __name__ == "__main__":
    unittest.main()