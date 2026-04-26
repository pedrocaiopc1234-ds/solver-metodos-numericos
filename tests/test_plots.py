"""Testes para funções de plot"""

import unittest
import plotly.graph_objects as go
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