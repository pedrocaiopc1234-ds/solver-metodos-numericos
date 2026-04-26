"""Testes para EDO"""

import unittest
import math
import numpy as np
from core.ode import euler_method, runge_kutta_4


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


# ─── 20 testes de robustez para Euler ────────────────────────────────

class TestEulerRobustness(unittest.TestCase):

    def test_robust_01_zero_step(self):
        """h = 0 — deve falhar"""
        f = lambda t, y: y
        r = euler_method(f, y0=1.0, t0=0, tf=1, h=0)
        self.assertFalse(r["success"])

    def test_robust_02_negative_step(self):
        """h negativo — deve falhar"""
        f = lambda t, y: y
        r = euler_method(f, y0=1.0, t0=0, tf=1, h=-0.1)
        self.assertFalse(r["success"])

    def test_robust_03_constant_rhs(self):
        """dy/dt = 1 → y = t + 1"""
        f = lambda t, y: 1
        r = euler_method(f, y0=1.0, t0=0, tf=2, h=0.1)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(r["y"][-1], 3.0, places=1)

    def test_robust_04_zero_rhs(self):
        """dy/dt = 0 → y = y0 constante"""
        f = lambda t, y: 0
        r = euler_method(f, y0=5.0, t0=0, tf=2, h=0.1)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(r["y"][-1], 5.0, places=5)

    def test_robust_05_negative_t0(self):
        """t0 negativo"""
        f = lambda t, y: y
        r = euler_method(f, y0=1.0, t0=-2, tf=0, h=0.1)
        self.assertTrue(r["success"])

    def test_robust_06_negative_y0(self):
        """y0 negativo"""
        f = lambda t, y: -y
        r = euler_method(f, y0=-1.0, t0=0, tf=1, h=0.1)
        self.assertTrue(r["success"])

    def test_robust_07_large_step(self):
        """Passo grande — impreciso mas não crasha"""
        f = lambda t, y: y
        r = euler_method(f, y0=1.0, t0=0, tf=1, h=0.5)
        self.assertTrue(r["success"])

    def test_robust_08_small_step(self):
        """Passo pequeno"""
        f = lambda t, y: y
        r = euler_method(f, y0=1.0, t0=0, tf=0.1, h=0.001)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(r["y"][-1], math.exp(0.1), places=2)

    def test_robust_09_t0_equals_tf(self):
        """t0 == tf — deve falhar"""
        f = lambda t, y: y
        r = euler_method(f, y0=1.0, t0=1, tf=1, h=0.1)
        self.assertFalse(r["success"])

    def test_robust_10_sin_rhs(self):
        """dy/dt = sin(t) → y = 1 - cos(t) + y0"""
        f = lambda t, y: math.sin(t)
        r = euler_method(f, y0=0.0, t0=0, tf=math.pi, h=0.01)
        self.assertTrue(r["success"])

    def test_robust_11_linear_decay(self):
        """dy/dt = -y → y = e^(-t)"""
        f = lambda t, y: -y
        r = euler_method(f, y0=1.0, t0=0, tf=1, h=0.01)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(r["y"][-1], math.exp(-1), places=2)

    def test_robust_12_quadratic_rhs(self):
        """dy/dt = t² → y = t³/3 + y0"""
        f = lambda t, y: t**2
        r = euler_method(f, y0=0.0, t0=0, tf=3, h=0.01)
        self.assertTrue(r["success"])

    def test_robust_13_function_exception(self):
        """Função que lança exceção"""
        def f(t, y):
            if t > 0.5:
                raise ValueError("undefined")
            return y
        r = euler_method(f, y0=1.0, t0=0, tf=1, h=0.1)
        self.assertFalse(r["success"])

    def test_robust_14_overflow_rhs(self):
        """dy/dt = y com y0 grande — pode overflow"""
        f = lambda t, y: y
        r = euler_method(f, y0=1e10, t0=0, tf=5, h=0.01)
        self.assertIsInstance(r["success"], bool)

    def test_robust_15_rhs_depends_on_t_only(self):
        """dy/dt = t → y = t²/2 + y0"""
        f = lambda t, y: t
        r = euler_method(f, y0=0.0, t0=0, tf=2, h=0.01)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(r["y"][-1], 2.0, places=1)

    def test_robust_16_y0_zero(self):
        """y0 = 0"""
        f = lambda t, y: y
        r = euler_method(f, y0=0.0, t0=0, tf=1, h=0.1)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(r["y"][-1], 0.0, places=10)

    def test_robust_17_stiff_rhs(self):
        """EDO stiff: dy/dt = -1000*y"""
        f = lambda t, y: -1000*y
        r = euler_method(f, y0=1.0, t0=0, tf=0.01, h=0.0001)
        self.assertIsInstance(r["success"], bool)

    def test_robust_18_tangent_rhs(self):
        """dy/dt = tan(t) — singular em π/2"""
        f = lambda t, y: math.tan(t)
        r = euler_method(f, y0=0.0, t0=0.1, tf=1.0, h=0.01)
        self.assertIsInstance(r["success"], bool)

    def test_robust_19_rhs_returns_nan(self):
        """Função que retorna NaN"""
        f = lambda t, y: float('nan')
        r = euler_method(f, y0=1.0, t0=0, tf=1, h=0.1)
        self.assertFalse(r["success"])

    def test_robust_20_rhs_returns_inf(self):
        """Função que retorna infinito"""
        f = lambda t, y: float('inf')
        r = euler_method(f, y0=1.0, t0=0, tf=1, h=0.1)
        self.assertFalse(r["success"])


# ─── 20 testes de robustez para RK4 ─────────────────────────────────

class TestRK4Robustness(unittest.TestCase):

    def test_robust_01_zero_step(self):
        """h = 0 — deve falhar"""
        f = lambda t, y: y
        r = runge_kutta_4(f, y0=1.0, t0=0, tf=1, h=0)
        self.assertFalse(r["success"])

    def test_robust_02_negative_step(self):
        """h negativo"""
        f = lambda t, y: y
        r = runge_kutta_4(f, y0=1.0, t0=0, tf=1, h=-0.1)
        self.assertFalse(r["success"])

    def test_robust_03_constant_rhs(self):
        """dy/dt = 1 → y = t + 1"""
        f = lambda t, y: 1
        r = runge_kutta_4(f, y0=1.0, t0=0, tf=2, h=0.1)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(r["y"][-1], 3.0, places=4)

    def test_robust_04_zero_rhs(self):
        """dy/dt = 0 → y constante"""
        f = lambda t, y: 0
        r = runge_kutta_4(f, y0=5.0, t0=0, tf=2, h=0.1)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(r["y"][-1], 5.0, places=5)

    def test_robust_05_negative_t0(self):
        """t0 negativo"""
        f = lambda t, y: y
        r = runge_kutta_4(f, y0=1.0, t0=-2, tf=0, h=0.1)
        self.assertTrue(r["success"])

    def test_robust_06_negative_y0(self):
        """y0 negativo"""
        f = lambda t, y: -y
        r = runge_kutta_4(f, y0=-1.0, t0=0, tf=1, h=0.01)
        self.assertTrue(r["success"])

    def test_robust_07_large_step(self):
        """Passo grande"""
        f = lambda t, y: y
        r = runge_kutta_4(f, y0=1.0, t0=0, tf=1, h=0.5)
        self.assertTrue(r["success"])

    def test_robust_08_small_step(self):
        """Passo pequeno — alta precisão"""
        f = lambda t, y: y
        r = runge_kutta_4(f, y0=1.0, t0=0, tf=0.5, h=0.001)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(r["y"][-1], math.exp(0.5), places=5)

    def test_robust_09_sin_rhs(self):
        """dy/dt = sin(t)"""
        f = lambda t, y: math.sin(t)
        r = runge_kutta_4(f, y0=0.0, t0=0, tf=math.pi, h=0.01)
        self.assertTrue(r["success"])

    def test_robust_10_linear_decay(self):
        """dy/dt = -y → y = e^(-t)"""
        f = lambda t, y: -y
        r = runge_kutta_4(f, y0=1.0, t0=0, tf=1, h=0.01)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(r["y"][-1], math.exp(-1), places=4)

    def test_robust_11_quadratic_rhs(self):
        """dy/dt = t²"""
        f = lambda t, y: t**2
        r = runge_kutta_4(f, y0=0.0, t0=0, tf=3, h=0.01)
        self.assertTrue(r["success"])

    def test_robust_12_function_exception(self):
        """Função que lança exceção"""
        def f(t, y):
            if t > 0.5:
                raise ValueError("undefined")
            return y
        r = runge_kutta_4(f, y0=1.0, t0=0, tf=1, h=0.1)
        self.assertFalse(r["success"])

    def test_robust_13_y0_zero(self):
        """y0 = 0"""
        f = lambda t, y: y
        r = runge_kutta_4(f, y0=0.0, t0=0, tf=1, h=0.1)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(r["y"][-1], 0.0, places=10)

    def test_robust_14_stiff_rhs(self):
        """EDO stiff: dy/dt = -1000*y"""
        f = lambda t, y: -1000*y
        r = runge_kutta_4(f, y0=1.0, t0=0, tf=0.01, h=0.0001)
        self.assertIsInstance(r["success"], bool)

    def test_robust_15_rhs_depends_t_only(self):
        """dy/dt = t"""
        f = lambda t, y: t
        r = runge_kutta_4(f, y0=0.0, t0=0, tf=2, h=0.01)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(r["y"][-1], 2.0, places=3)

    def test_robust_16_tangent_rhs(self):
        """dy/dt = tan(t) — singular em π/2"""
        f = lambda t, y: math.tan(t)
        r = runge_kutta_4(f, y0=0.0, t0=0.1, tf=1.0, h=0.01)
        self.assertIsInstance(r["success"], bool)

    def test_robust_17_exp_growth(self):
        """dy/dt = 2y → crescimento exponencial"""
        f = lambda t, y: 2*y
        r = runge_kutta_4(f, y0=1.0, t0=0, tf=1, h=0.01)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(r["y"][-1], math.exp(2), places=3)

    def test_robust_18_cos_rhs(self):
        """dy/dt = cos(t) → y = sin(t) + y0"""
        f = lambda t, y: math.cos(t)
        r = runge_kutta_4(f, y0=0.0, t0=0, tf=math.pi/2, h=0.01)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(r["y"][-1], 1.0, places=1)

    def test_robust_19_rhs_returns_nan(self):
        """Função que retorna NaN"""
        f = lambda t, y: float('nan')
        r = runge_kutta_4(f, y0=1.0, t0=0, tf=1, h=0.1)
        self.assertFalse(r["success"])

    def test_robust_20_rhs_returns_inf(self):
        """Função que retorna infinito"""
        f = lambda t, y: float('inf')
        r = runge_kutta_4(f, y0=1.0, t0=0, tf=1, h=0.1)
        self.assertFalse(r["success"])


if __name__ == "__main__":
    unittest.main()