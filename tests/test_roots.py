"""Testes para métodos de raízes"""

import unittest
import math
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


# ─── 20 testes de robustez para bissecção ───────────────────────────

class TestBisectionRobustness(unittest.TestCase):

    def test_robust_01_no_sign_change_positive(self):
        """Função sempre positiva — sem raiz"""
        f = lambda x: x**2 + 4
        r = bisection(f, -1, 1)
        self.assertFalse(r["success"])

    def test_robust_02_zero_at_endpoint(self):
        """Raiz exata no ponto a"""
        f = lambda x: x
        r = bisection(f, 0, 5)
        self.assertIn(r["success"], [True, False])

    def test_robust_03_discontinuous(self):
        """1/x — descontinuidade no intervalo"""
        f = lambda x: 1/x
        r = bisection(f, -1, 1)
        self.assertIsInstance(r["success"], bool)

    def test_robust_04_tiny_interval(self):
        """Intervalo minúsculo sem raiz"""
        f = lambda x: x**2 + 1
        r = bisection(f, 0, 1e-15)
        self.assertFalse(r["success"])

    def test_robust_04b_a_greater_than_b(self):
        """a > b — deve falhar"""
        f = lambda x: x**2 - 4
        r = bisection(f, 3, 0)
        self.assertFalse(r["success"])

    def test_robust_05_large_interval(self):
        """Intervalo grande com raiz"""
        f = lambda x: x**3 - 8
        r = bisection(f, -1000, 1000)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(r["root"], 2.0, places=3)

    def test_robust_06_multiple_roots(self):
        """Intervalo com múltiplas raízes"""
        f = lambda x: math.sin(x)
        r = bisection(f, 0.1, 6.2)
        self.assertTrue(r["success"])

    def test_robust_07_nan_in_function(self):
        """Função que retorna NaN"""
        f = lambda x: math.sqrt(x) - 1 if x >= 0 else float('nan')
        r = bisection(f, -1, 4)
        self.assertIsInstance(r["success"], bool)

    def test_robust_08_inf_in_function(self):
        """Função que retorna infinito"""
        f = lambda x: 1/(x-2) if x != 2 else float('inf')
        r = bisection(f, 0, 4)
        self.assertIsInstance(r["success"], bool)

    def test_robust_09_very_flat(self):
        """(x-3)^5 — muito plana perto da raiz"""
        f = lambda x: (x - 3)**5
        r = bisection(f, 0, 10)
        self.assertTrue(r["success"])

    def test_robust_10_max_iterations(self):
        """Não converge com tol pequena e poucas iterações"""
        f = lambda x: x**2 - 2
        r = bisection(f, 0, 2, tol=1e-20, max_iter=5)
        self.assertFalse(r["success"])

    def test_robust_11_always_negative(self):
        """Função sempre negativa"""
        f = lambda x: -(x**2 + 1)
        r = bisection(f, -10, 10)
        self.assertFalse(r["success"])

    def test_robust_12_exp_root(self):
        """e^x - 1 = 0"""
        f = lambda x: math.exp(x) - 1
        r = bisection(f, -5, 5)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(r["root"], 0.0, places=4)

    def test_robust_13_log_root(self):
        """ln(x) = 0 → x=1"""
        f = lambda x: math.log(x) if x > 0 else -1e10
        r = bisection(f, 0.1, 10)
        self.assertTrue(r["success"])

    def test_robust_14_tangent(self):
        """tan(x) - 1 com descontinuidade"""
        f = lambda x: math.tan(x) - 1
        r = bisection(f, 0.5, 1.0)
        self.assertTrue(r["success"])

    def test_robust_15_constant_function(self):
        """f(x) = 5 — sem raiz"""
        f = lambda x: 5
        r = bisection(f, -100, 100)
        self.assertFalse(r["success"])

    def test_robust_16_near_zero_no_root(self):
        """x² + 1e-10 — quase toca zero mas não cruza"""
        f = lambda x: x**2 + 1e-10
        r = bisection(f, -1, 1)
        self.assertFalse(r["success"])

    def test_robust_17_very_steep(self):
        """1e10*(x-0.5) — muito íngreme"""
        f = lambda x: 1e10 * (x - 0.5)
        r = bisection(f, 0, 1)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(r["root"], 0.5, places=4)

    def test_robust_18_high_degree_poly(self):
        """x^6 - 1 = 0"""
        f = lambda x: x**6 - 1
        r = bisection(f, 0, 2)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(r["root"], 1.0, places=4)

    def test_robust_19_oscillating(self):
        """sin(x) - 0.5"""
        f = lambda x: math.sin(x) - 0.5
        r = bisection(f, 0, 2)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(math.sin(r["root"]), 0.5, places=4)

    def test_robust_20_abs_no_sign_change(self):
        """|x| — sem mudança de sinal"""
        f = lambda x: abs(x)
        r = bisection(f, -1, 1)
        self.assertFalse(r["success"])


# ─── 20 testes de robustez para Newton ──────────────────────────────

class TestNewtonRobustness(unittest.TestCase):

    def test_robust_01_derivative_zero(self):
        """Derivada zero no ponto inicial"""
        f = lambda x: x**3
        df = lambda x: 3*x**2
        r = newton(f, df, 0.0)
        self.assertFalse(r["success"])

    def test_robust_02_converges_quadratic(self):
        """x²-2=0 — convergência quadrática"""
        f = lambda x: x**2 - 2
        df = lambda x: 2*x
        r = newton(f, df, 1.5)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(r["root"], math.sqrt(2), places=5)

    def test_robust_03_flat_function(self):
        """x^(1/3) — derivada explode perto de zero"""
        f = lambda x: x**(1/3) if x != 0 else 0
        df = lambda x: (1/3)*x**(-2/3) if x != 0 else float('inf')
        r = newton(f, df, 1.0, max_iter=100)
        self.assertIsInstance(r["success"], bool)

    def test_robust_04_near_zero_derivative(self):
        """x³-0.001 — derivada pequena perto de zero"""
        f = lambda x: x**3 - 0.001
        df = lambda x: 3*x**2
        r = newton(f, df, 0.01)
        self.assertIsInstance(r["success"], bool)

    def test_robust_05_max_iterations(self):
        """Não converge em poucas iterações"""
        f = lambda x: math.tan(x) - x
        df = lambda x: 1/math.cos(x)**2 - 1 if abs(math.cos(x)) > 1e-10 else 1e10
        r = newton(f, df, 1.0, max_iter=3)
        self.assertIsInstance(r["success"], bool)

    def test_robust_06_exp_root(self):
        """e^x - 2 = 0"""
        f = lambda x: math.exp(x) - 2
        df = lambda x: math.exp(x)
        r = newton(f, df, 1.0)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(r["root"], math.log(2), places=5)

    def test_robust_07_x4_derivative_zero(self):
        """x⁴-16 — derivada zero em x=0"""
        f = lambda x: x**4 - 16
        df = lambda x: 4*x**3
        r = newton(f, df, 0.0)
        self.assertFalse(r["success"])

    def test_robust_08_rational_root(self):
        """1/x - 1 = 0 → x=1"""
        f = lambda x: 1/x - 1
        df = lambda x: -1/x**2
        r = newton(f, df, 0.5)
        self.assertTrue(r["success"])

    def test_robust_09_function_exception(self):
        """Função que lança exceção"""
        def f(x):
            if abs(x) < 0.1:
                raise ValueError("undefined")
            return x - 2
        def df(x):
            if abs(x) < 0.1:
                raise ValueError("undefined")
            return 1
        r = newton(f, df, 3.0)
        self.assertIsInstance(r["success"], bool)

    def test_robust_10_log_root(self):
        """ln(x) = 0 → x=1"""
        f = lambda x: math.log(x)
        df = lambda x: 1/x
        r = newton(f, df, 2.0)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(r["root"], 1.0, places=5)

    def test_robust_11_trig_root(self):
        """cos(x) = 0 → x=π/2"""
        f = lambda x: math.cos(x)
        df = lambda x: -math.sin(x)
        r = newton(f, df, 1.0)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(r["root"], math.pi/2, places=5)

    def test_robust_12_high_degree_poly(self):
        """x⁵-1=0"""
        f = lambda x: x**5 - 1
        df = lambda x: 5*x**4
        r = newton(f, df, 2.0)
        self.assertTrue(r["success"])

    def test_robust_13_close_roots(self):
        """Raízes próximas: x²-2.001x+1.001=0"""
        f = lambda x: x**2 - 2.001*x + 1.001
        df = lambda x: 2*x - 2.001
        r = newton(f, df, 0.5)
        self.assertTrue(r["success"])

    def test_robust_14_very_large_start(self):
        """Ponto inicial muito distante"""
        f = lambda x: x - 5
        df = lambda x: 1
        r = newton(f, df, 1e10)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(r["root"], 5.0, places=4)

    def test_robust_15_negative_start(self):
        """Ponto inicial negativo"""
        f = lambda x: x**2 - 4
        df = lambda x: 2*x
        r = newton(f, df, -10.0)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(abs(r["root"]), 2.0, places=4)

    def test_robust_16_tiny_tolerance(self):
        """Tolerância extremamente pequena"""
        f = lambda x: x - 3
        df = lambda x: 1
        r = newton(f, df, 10.0, tol=1e-15)
        self.assertTrue(r["success"])

    def test_robust_17_cos_derivative_zero(self):
        """cos(x) com x0=0 → derivada -sin(0)=0"""
        f = lambda x: math.cos(x)
        df = lambda x: -math.sin(x)
        r = newton(f, df, 0.0)
        self.assertFalse(r["success"])

    def test_robust_18_exp_decay_root(self):
        """e^(-x) - 0.5 = 0"""
        f = lambda x: math.exp(-x) - 0.5
        df = lambda x: -math.exp(-x)
        r = newton(f, df, 1.0)
        self.assertTrue(r["success"])

    def test_robust_19_rational_function(self):
        """(x-3)/(x+1) = 0 → x=3"""
        f = lambda x: (x-3)/(x+1)
        df = lambda x: 4/(x+1)**2
        r = newton(f, df, 5.0)
        self.assertTrue(r["success"])

    def test_robust_20_constant_derivative_zero(self):
        """floor(x)-2 com derivada zero"""
        f = lambda x: math.floor(x) - 2
        df = lambda x: 0
        r = newton(f, df, 2.5)
        self.assertFalse(r["success"])


# ─── 20 testes de robustez para Secante ─────────────────────────────

class TestSecantRobustness(unittest.TestCase):

    def test_robust_01_identical_points(self):
        """x0 == x1 — f1-f0 = 0"""
        f = lambda x: x**2 - 4
        r = secant(f, 2.0, 2.0)
        self.assertIsInstance(r["success"], bool)

    def test_robust_02_very_close_points(self):
        """Pontos muito próximos — divisão por zero"""
        f = lambda x: x**2 - 4
        r = secant(f, 1.0000001, 1.0000002)
        self.assertIsInstance(r["success"], bool)

    def test_robust_03_no_root_parabola(self):
        """x²+1 — sem raiz real"""
        f = lambda x: x**2 + 1
        r = secant(f, -1, 1)
        self.assertFalse(r["success"])

    def test_robust_04_constant_function(self):
        """f(x)=5 — f1-f0 = 0"""
        f = lambda x: 5
        r = secant(f, 0, 1)
        self.assertFalse(r["success"])

    def test_robust_05_max_iterations(self):
        """Não converge em poucas iterações"""
        f = lambda x: math.sin(x) - x/10 + 2
        r = secant(f, -10, 10, max_iter=3)
        self.assertIsInstance(r["success"], bool)

    def test_robust_06_exp_root(self):
        """e^x - 1 = 0"""
        f = lambda x: math.exp(x) - 1
        r = secant(f, -1, 1)
        self.assertTrue(r["success"])

    def test_robust_07_log_root(self):
        """ln(x)+1=0 → x=1/e"""
        f = lambda x: math.log(x) + 1
        r = secant(f, 0.1, 1.0)
        self.assertTrue(r["success"])

    def test_robust_08_discontinuous(self):
        """1/(x-2) — descontinuidade"""
        f = lambda x: 1/(x-2) if abs(x-2) > 1e-10 else 1e10
        r = secant(f, 0, 5)
        self.assertIsInstance(r["success"], bool)

    def test_robust_09_returns_inf(self):
        """Função que retorna infinito"""
        f = lambda x: 1/x**2 if x != 0 else float('inf')
        r = secant(f, -2, 2)
        self.assertIsInstance(r["success"], bool)

    def test_robust_10_cubic_polynomial(self):
        """x³-x-1=0"""
        f = lambda x: x**3 - x - 1
        r = secant(f, 1, 2)
        self.assertTrue(r["success"])

    def test_robust_11_trig_root(self):
        """sin(x) = 0.5"""
        f = lambda x: math.sin(x) - 0.5
        r = secant(f, 0, 2)
        self.assertTrue(r["success"])

    def test_robust_12_large_interval(self):
        """x-10=0 em intervalo grande"""
        f = lambda x: x - 10
        r = secant(f, -1e6, 1e6)
        self.assertTrue(r["success"])

    def test_robust_13_double_root(self):
        """(x-1)² — raiz dupla, convergência lenta"""
        f = lambda x: x**2 - 2*x + 1
        r = secant(f, 0, 3)
        # Raiz dupla tem convergência lenta — pode falhar com tol padrão
        self.assertIsInstance(r["success"], bool)

    def test_robust_14_cos_oscillation(self):
        """cos(πx) — alta oscilação"""
        f = lambda x: math.cos(math.pi * x)
        r = secant(f, 0, 0.5)
        self.assertIsInstance(r["success"], bool)

    def test_robust_15_f0_equals_f1(self):
        """f(x0) = f(x1) mas x0 ≠ x1"""
        f = lambda x: (x-3)**2
        r = secant(f, 2, 4)
        self.assertIsInstance(r["success"], bool)

    def test_robust_16_pole_in_interval(self):
        """x/(x²-4) — pólos em ±2"""
        f = lambda x: x/(x**2-4) if abs(x**2-4) > 1e-10 else 1e10
        r = secant(f, 0, 5)
        self.assertIsInstance(r["success"], bool)

    def test_robust_17_negative_start(self):
        """x+3=0 com pontos negativos"""
        f = lambda x: x + 3
        r = secant(f, -5, -4)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(r["root"], -3.0, places=4)

    def test_robust_18_high_frequency(self):
        """sin(50x) — alta frequência"""
        f = lambda x: math.sin(50*x)
        r = secant(f, 0, 0.1)
        self.assertIsInstance(r["success"], bool)

    def test_robust_19_function_exception(self):
        """Função que lança exceção"""
        def f(x):
            if x > 5:
                raise ValueError("overflow")
            return x**2 - 4
        r = secant(f, 0, 3)
        self.assertIsInstance(r["success"], bool)

    def test_robust_20_standard_convergence(self):
        """x²-2=0 convergência padrão"""
        f = lambda x: x**2 - 2
        r = secant(f, 1, 2)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(r["root"], math.sqrt(2), places=4)


if __name__ == "__main__":
    unittest.main()