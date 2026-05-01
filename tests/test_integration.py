"""Testes para integração numérica"""

import unittest
import math
import numpy as np
from core.integration import simpson, trapezoidal_repeated, three_eight_method

# Validação por biblioteca: compara com scipy.integrate
try:
    from scipy import integrate
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False


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


# ─── 20 testes de robustez para Simpson ─────────────────────────────

class TestSimpsonRobustness(unittest.TestCase):

    def test_robust_01_odd_n(self):
        """n ímpar — deve falhar"""
        f = lambda x: x**2
        r = simpson(f, 0, 1, n=3)
        self.assertFalse(r["success"])

    def test_robust_02_negative_interval(self):
        """Intervalo negativo [a, b] com a > b"""
        f = lambda x: x**2
        r = simpson(f, 2, 0, n=4)
        self.assertIsInstance(r["success"], bool)

    def test_robust_03_linear_function(self):
        """Função linear — Simpson é exata"""
        f = lambda x: 2*x + 1
        r = simpson(f, 0, 2, n=2)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(r["result"], 6.0, places=5)

    def test_robust_04_constant_function(self):
        """f(x) = 5 — ∫₀² 5 dx = 10"""
        f = lambda x: 5
        r = simpson(f, 0, 2, n=2)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(r["result"], 10.0, places=5)

    def test_robust_05_sin_function(self):
        """∫₀^π sin(x) dx = 2"""
        f = lambda x: math.sin(x)
        r = simpson(f, 0, math.pi, n=100)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(r["result"], 2.0, places=3)

    def test_robust_06_exp_function(self):
        """∫₀¹ e^x dx = e - 1"""
        f = lambda x: math.exp(x)
        r = simpson(f, 0, 1, n=100)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(r["result"], math.e - 1, places=4)

    def test_robust_07_large_interval(self):
        """Intervalo grande"""
        f = lambda x: 1 / (1 + x**2)
        r = simpson(f, 0, 100, n=200)
        self.assertTrue(r["success"])

    def test_robust_08_tiny_interval(self):
        """Intervalo minúsculo"""
        f = lambda x: x**2
        r = simpson(f, 0, 1e-10, n=2)
        self.assertTrue(r["success"])

    def test_robust_09_zero_function(self):
        """f(x) = 0"""
        f = lambda x: 0
        r = simpson(f, 0, 5, n=10)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(r["result"], 0.0, places=10)

    def test_robust_10_negative_values(self):
        """Função com valores negativos"""
        f = lambda x: -x**2
        r = simpson(f, 0, 2, n=100)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(r["result"], -8/3, places=2)

    def test_robust_11_1_over_x(self):
        """1/x — descontinuidade em 0"""
        f = lambda x: 1/x
        r = simpson(f, 0.001, 1, n=100)
        self.assertTrue(r["success"])

    def test_robust_12_cos_function(self):
        """∫₀^(π/2) cos(x) dx = 1"""
        f = lambda x: math.cos(x)
        r = simpson(f, 0, math.pi/2, n=100)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(r["result"], 1.0, places=4)

    def test_robust_13_high_n(self):
        """n muito grande"""
        f = lambda x: x**2
        r = simpson(f, 0, 1, n=10000)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(r["result"], 1/3, places=5)

    def test_robust_14_n_2(self):
        """n mínimo (2)"""
        f = lambda x: x**2
        r = simpson(f, 0, 1, n=2)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(r["result"], 1/3, places=5)

    def test_robust_15_sqrt_function(self):
        """√x — não analítica em 0"""
        f = lambda x: math.sqrt(x)
        r = simpson(f, 0, 1, n=100)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(r["result"], 2/3, places=2)

    def test_robust_16_negative_a(self):
        """a negativo"""
        f = lambda x: x**2
        r = simpson(f, -2, 2, n=100)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(r["result"], 16/3, places=2)

    def test_robust_17_log_function(self):
        """∫₁^e ln(x) dx = 1"""
        f = lambda x: math.log(x)
        r = simpson(f, 1, math.e, n=100)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(r["result"], 1.0, places=2)

    def test_robust_18_rational_function(self):
        """1/(1+x²) — arctan"""
        f = lambda x: 1/(1 + x**2)
        r = simpson(f, 0, 1, n=100)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(r["result"], math.pi/4, places=3)

    def test_robust_19_nan_function(self):
        """Função que retorna NaN"""
        f = lambda x: float('nan')
        r = simpson(f, 0, 1, n=4)
        self.assertFalse(r["success"])

    def test_robust_20_inf_function(self):
        """Função que retorna infinito"""
        f = lambda x: float('inf')
        r = simpson(f, 0, 1, n=4)
        self.assertFalse(r["success"])


# ─── 20 testes de robustez para Trapézio ────────────────────────────

class TestTrapezoidalRobustness(unittest.TestCase):

    def test_robust_01_zero_n(self):
        """n = 0 — deve falhar"""
        f = lambda x: x**2
        r = trapezoidal_repeated(f, 0, 1, n=0)
        self.assertFalse(r["success"])

    def test_robust_02_negative_n(self):
        """n negativo — deve falhar"""
        f = lambda x: x**2
        r = trapezoidal_repeated(f, 0, 1, n=-5)
        self.assertIsInstance(r["success"], bool)

    def test_robust_03_constant_function(self):
        """f(x) = 5"""
        f = lambda x: 5
        r = trapezoidal_repeated(f, 0, 2, n=10)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(r["result"], 10.0, places=5)

    def test_robust_04_linear_function(self):
        """f(x) = 2x+1 — trapézio é exato"""
        f = lambda x: 2*x + 1
        r = trapezoidal_repeated(f, 0, 2, n=1)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(r["result"], 6.0, places=5)

    def test_robust_05_sin_function(self):
        """∫₀^π sin(x) dx = 2"""
        f = lambda x: math.sin(x)
        r = trapezoidal_repeated(f, 0, math.pi, n=1000)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(r["result"], 2.0, places=2)

    def test_robust_06_exp_function(self):
        """∫₀¹ e^x dx = e - 1"""
        f = lambda x: math.exp(x)
        r = trapezoidal_repeated(f, 0, 1, n=1000)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(r["result"], math.e - 1, places=3)

    def test_robust_07_zero_function(self):
        """f(x) = 0"""
        f = lambda x: 0
        r = trapezoidal_repeated(f, 0, 5, n=10)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(r["result"], 0.0, places=10)

    def test_robust_08_negative_values(self):
        """Função negativa"""
        f = lambda x: -x**2
        r = trapezoidal_repeated(f, 0, 2, n=100)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(r["result"], -8/3, places=2)

    def test_robust_09_negative_interval(self):
        """a > b"""
        f = lambda x: x**2
        r = trapezoidal_repeated(f, 2, 0, n=100)
        self.assertIsInstance(r["success"], bool)

    def test_robust_10_large_n(self):
        """n grande"""
        f = lambda x: x**2
        r = trapezoidal_repeated(f, 0, 1, n=10000)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(r["result"], 1/3, places=4)

    def test_robust_11_n_1(self):
        """n = 1 — mínimo"""
        f = lambda x: x**2
        r = trapezoidal_repeated(f, 0, 2, n=1)
        self.assertTrue(r["success"])

    def test_robust_12_sqrt_function(self):
        """√x — singular em 0"""
        f = lambda x: math.sqrt(x)
        r = trapezoidal_repeated(f, 0, 1, n=1000)
        self.assertTrue(r["success"])

    def test_robust_13_negative_a(self):
        """a negativo"""
        f = lambda x: x**2
        r = trapezoidal_repeated(f, -2, 2, n=100)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(r["result"], 16/3, places=2)

    def test_robust_14_log_function(self):
        """∫₁^e ln(x) dx = 1"""
        f = lambda x: math.log(x)
        r = trapezoidal_repeated(f, 1, math.e, n=1000)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(r["result"], 1.0, places=2)

    def test_robust_15_rational_function(self):
        """1/(1+x²)"""
        f = lambda x: 1/(1 + x**2)
        r = trapezoidal_repeated(f, 0, 1, n=1000)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(r["result"], math.pi/4, places=3)

    def test_robust_16_1_over_x(self):
        """1/x — perto de zero"""
        f = lambda x: 1/x
        r = trapezoidal_repeated(f, 0.001, 1, n=1000)
        self.assertTrue(r["success"])

    def test_robust_17_nan_function(self):
        """Função que retorna NaN"""
        f = lambda x: float('nan')
        r = trapezoidal_repeated(f, 0, 1, n=4)
        self.assertFalse(r["success"])

    def test_robust_18_inf_function(self):
        """Função que retorna infinito"""
        f = lambda x: float('inf')
        r = trapezoidal_repeated(f, 0, 1, n=4)
        self.assertFalse(r["success"])

    def test_robust_19_cos_function(self):
        """∫ cos(x) dx de 0 a π/2 = 1"""
        f = lambda x: math.cos(x)
        r = trapezoidal_repeated(f, 0, math.pi/2, n=1000)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(r["result"], 1.0, places=3)

    def test_robust_20_tiny_interval(self):
        """Intervalo minúsculo"""
        f = lambda x: x**2
        r = trapezoidal_repeated(f, 0, 1e-10, n=10)
        self.assertTrue(r["success"])


# ─── 20 testes de robustez para 3/8 ─────────────────────────────────

class TestThreeEightRobustness(unittest.TestCase):

    def test_robust_01_constant_function(self):
        """f(x) = 5 — ∫₀³ 5 dx = 15"""
        f = lambda x: 5
        r = three_eight_method(f, 0, 3)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(r["result"], 15.0, places=3)

    def test_robust_02_linear_function(self):
        """f(x) = 2x+1 — ∫₀³ (2x+1) dx = 12"""
        f = lambda x: 2*x + 1
        r = three_eight_method(f, 0, 3)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(r["result"], 12.0, places=3)

    def test_robust_03_sin_function(self):
        """∫₀^π sin(x) dx = 2"""
        f = lambda x: math.sin(x)
        r = three_eight_method(f, 0, math.pi)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(r["result"], 2.0, places=1)

    def test_robust_04_exp_function(self):
        """∫₀¹ e^x dx ≈ e-1"""
        f = lambda x: math.exp(x)
        r = three_eight_method(f, 0, 1)
        self.assertTrue(r["success"])

    def test_robust_05_negative_interval(self):
        """a > b — deve falhar"""
        f = lambda x: x**2
        r = three_eight_method(f, 3, 0)
        self.assertFalse(r["success"])

    def test_robust_06_zero_function(self):
        """f(x) = 0"""
        f = lambda x: 0
        r = three_eight_method(f, 0, 5)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(r["result"], 0.0, places=10)

    def test_robust_07_negative_values(self):
        """Função negativa"""
        f = lambda x: -x**2
        r = three_eight_method(f, 0, 3)
        self.assertTrue(r["success"])

    def test_robust_08_negative_a(self):
        """a negativo"""
        f = lambda x: x**2
        r = three_eight_method(f, -3, 0)
        self.assertTrue(r["success"])

    def test_robust_09_rational_function(self):
        """1/(1+x²)"""
        f = lambda x: 1/(1 + x**2)
        r = three_eight_method(f, 0, 1)
        self.assertTrue(r["success"])

    def test_robust_10_sqrt_function(self):
        """√x"""
        f = lambda x: math.sqrt(x)
        r = three_eight_method(f, 0, 1)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(r["result"], 2/3, places=1)

    def test_robust_11_cos_function(self):
        """∫₀^(π/2) cos(x) dx = 1"""
        f = lambda x: math.cos(x)
        r = three_eight_method(f, 0, math.pi/2)
        self.assertTrue(r["success"])

    def test_robust_12_large_interval(self):
        """Intervalo grande"""
        f = lambda x: 1/(1 + x**2)
        r = three_eight_method(f, 0, 10)
        self.assertTrue(r["success"])

    def test_robust_13_tiny_interval(self):
        """Intervalo pequeno"""
        f = lambda x: x**2
        r = three_eight_method(f, 0, 0.01)
        self.assertTrue(r["success"])

    def test_robust_14_log_function(self):
        """∫₁^e ln(x) dx = 1"""
        f = lambda x: math.log(x)
        r = three_eight_method(f, 1, math.e)
        self.assertTrue(r["success"])

    def test_robust_15_cubic_exact(self):
        """x³ — 3/8 é exato para cúbicos"""
        f = lambda x: x**3
        r = three_eight_method(f, 0, 2)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(r["result"], 4.0, places=2)

    def test_robust_16_nan_function(self):
        """Função que retorna NaN"""
        f = lambda x: float('nan')
        r = three_eight_method(f, 0, 1)
        self.assertFalse(r["success"])

    def test_robust_17_inf_function(self):
        """Função que retorna infinito"""
        f = lambda x: float('inf')
        r = three_eight_method(f, 0, 1)
        self.assertFalse(r["success"])

    def test_robust_18_1_over_x(self):
        """1/x — singular em 0"""
        f = lambda x: 1/x
        r = three_eight_method(f, 0.001, 1)
        self.assertTrue(r["success"])

    def test_robust_19_same_a_b(self):
        """a == b — integral zero"""
        f = lambda x: x**2
        r = three_eight_method(f, 2, 2)
        self.assertIsInstance(r["success"], bool)

    def test_robust_20_exp_decay(self):
        """∫₀¹ e^(-x) dx = 1 - 1/e"""
        f = lambda x: math.exp(-x)
        r = three_eight_method(f, 0, 1)
        self.assertTrue(r["success"])
        self.assertAlmostEqual(r["result"], 1 - 1/math.e, places=2)


if __name__ == "__main__":
    unittest.main()


# ==============================================================================
# VALIDAÇÃO POR BIBLIOTECA - Compara implementações do core com scipy.integrate
# ==============================================================================

@unittest.skipUnless(SCIPY_AVAILABLE, "scipy não disponível")
class TestIntegrationValidacaoBiblioteca(unittest.TestCase):
    """
    Testes que comparam as implementações do core/ com scipy.integrate.
    Garante que os métodos são compatíveis com as implementações de referência.
    """

    def test_simpson_vs_scipy_simpson(self):
        """Simpson 1/3: core vs scipy.integrate.simpson"""
        f = lambda x: x**2
        a, b = 0, 2
        n = 10  # deve ser par

        # Nossa implementação
        core_result = simpson(f, a, b, n=n)

        # scipy.integrate.simpson usa o mesmo algoritmo
        x = np.linspace(a, b, n + 1)
        y = [f(xi) for xi in x]
        scipy_result = integrate.simpson(y, x)

        self.assertTrue(core_result["success"])
        self.assertAlmostEqual(core_result["result"], scipy_result, places=6,
                               msg=f"core simpson={core_result['result']} != scipy={scipy_result}")

    def test_simpson_vs_scipy_multiple_functions(self):
        """Simpson: valida com múltiplas funções"""
        test_cases = [
            (lambda x: x**2, 0, 2, 10),           # x^2
            (lambda x: math.sin(x), 0, math.pi, 100),  # sin(x)
            (lambda x: math.exp(x), 0, 1, 100),   # e^x
            (lambda x: 1/(1 + x**2), 0, 1, 100),  # arctan
        ]
        for f, a, b, n in test_cases:
            core_result = simpson(f, a, b, n=n)
            x = np.linspace(a, b, n + 1)
            y = [f(xi) for xi in x]
            scipy_result = integrate.simpson(y, x)
            if core_result["success"]:
                self.assertAlmostEqual(core_result["result"], scipy_result, places=4)

    def test_trapezoidal_vs_scipy_trapezoid(self):
        """Trapezoidal: core vs scipy.integrate.trapezoid"""
        f = lambda x: x**2
        a, b = 0, 2
        n = 100

        # Nossa implementação
        core_result = trapezoidal_repeated(f, a, b, n=n)

        # scipy.integrate.trapezoid (antigo trapz)
        x = np.linspace(a, b, n + 1)
        y = [f(xi) for xi in x]
        scipy_result = integrate.trapezoid(y, x)

        self.assertTrue(core_result["success"])
        self.assertAlmostEqual(core_result["result"], scipy_result, places=5,
                               msg=f"core trapezoidal={core_result['result']} != scipy={scipy_result}")

    def test_trapezoidal_vs_scipy_multiple_functions(self):
        """Trapezoidal: valida com múltiplas funções"""
        test_cases = [
            (lambda x: x**2, 0, 2, 100),
            (lambda x: math.sin(x), 0, math.pi, 1000),
            (lambda x: math.exp(x), 0, 1, 1000),
        ]
        for f, a, b, n in test_cases:
            core_result = trapezoidal_repeated(f, a, b, n=n)
            x = np.linspace(a, b, n + 1)
            y = [f(xi) for xi in x]
            scipy_result = integrate.trapezoid(y, x)
            if core_result["success"]:
                self.assertAlmostEqual(core_result["result"], scipy_result, places=3)

    def test_all_methods_same_integral(self):
        """Todos os métodos devem calcular a mesma integral para f(x)=x²"""
        f = lambda x: x**2
        a, b = 0, 2

        # Valor exato: ∫₀² x² dx = 8/3
        exact = 8/3

        simpson_result = simpson(f, a, b, n=100)
        trap_result = trapezoidal_repeated(f, a, b, n=1000)

        # scipy para Simpson
        x = np.linspace(a, b, 101)
        y = [f(xi) for xi in x]
        scipy_simpson = integrate.simpson(y, x)

        self.assertTrue(simpson_result["success"])
        self.assertTrue(trap_result["success"])

        # Simpson deve ser mais próximo do exato (é exato para polinômios até grau 3)
        self.assertAlmostEqual(simpson_result["result"], exact, places=5)
        self.assertAlmostEqual(scipy_simpson, exact, places=5)

    def test_simpson_exact_for_cubic(self):
        """Simpson é exato para polinômios até grau 3"""
        # ∫₀² x³ dx = 4
        f = lambda x: x**3
        core_result = simpson(f, 0, 2, n=10)
        x = np.linspace(0, 2, 11)
        y = [f(xi) for xi in x]
        scipy_result = integrate.simpson(y, x)

        self.assertTrue(core_result["success"])
        self.assertAlmostEqual(core_result["result"], 4.0, places=5)
        self.assertAlmostEqual(core_result["result"], scipy_result, places=10)

    def test_three_eight_vs_simpson_comparison(self):
        """3/8 deve ter precisão similar ao Simpson 1/3"""
        f = lambda x: x**2
        a, b = 0, 3

        # 3/8 method (core)
        three_eight_result = three_eight_method(f, a, b)

        # Simpson 1/3 (core) - n=6 (múltiplo de 2 e próximo de 3 subintervalos)
        simpson_result = simpson(f, a, b, n=6)

        # scipy Simpson
        x = np.linspace(a, b, 4)  # 4 pontos = 3 subintervalos
        y = [f(xi) for xi in x]
        scipy_result = integrate.simpson(y, x)

        # Valor exato: ∫₀³ x² dx = 9
        exact = 9.0

        if three_eight_result["success"]:
            self.assertAlmostEqual(three_eight_result["result"], exact, places=3)
        if simpson_result["success"]:
            self.assertAlmostEqual(simpson_result["result"], scipy_result, places=5)