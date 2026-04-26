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


if __name__ == "__main__":
    unittest.main()