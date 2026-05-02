"""
Comparacao: Implementacoes core/integration.py vs scipy.integrate
50 exemplos de Integracao Numerica
"""

import numpy as np
import math
from core.integration import simpson, trapezoidal_repeated, three_eight_method
from scipy import integrate

# 50 Problemas de Integracao
PROBLEMS = [
    # ID: (f, a, b, valor_exato, descricao)
    (lambda x: x**2, 0, 1, 1/3, "Simpson 1/3 deve ser exato"),
    (lambda x: x**3, 0, 1, 1/4, "Simpson 1/3 e 3/8 devem ser exatos"),
    (lambda x: x**4, 0, 1, 1/5, "Teste de erro para Simpson"),
    (lambda x: 1/x, 1, 2, math.log(2), "Solucao: ln(2)"),
    (lambda x: 1/np.sqrt(x) if x > 0 else 0, 0, 1, 2.0, "Singularidade em x=0 (impropria)"),
    (lambda x: np.exp(-x**2), 0, 1, 0.7468241328124271, "Funcao erro (sem primitiva elementar)"),
    (lambda x: np.sin(x), 0, math.pi, 2.0, "Funcao suave"),
    (lambda x: np.sin(100*x), 0, math.pi, 0.0, "Oscilacao rapida; exige muitos subintervalos"),
    (lambda x: np.sqrt(1 - x**2) if x <= 1 else 0, 0, 1, math.pi/4, "Quarto de circulo; derivada infinita em x=1"),
    (lambda x: abs(x - 0.5), 0, 1, 0.25, "Ponto nao derivavel em x=0.5"),
    (lambda x: 1 / (1 + x**2), 0, 1, math.pi/4, "Solucao: pi/4"),
    (lambda x: np.log(x), 1, math.e, 1.0, "Solucao: 1"),
    (lambda x: x * np.exp(x), 0, 1, 1.0, "Integracao por partes"),
    (lambda x: 1 / (2 + np.cos(x)), 0, 2*math.pi, 2*math.pi/math.sqrt(3), "Funcao periodica suave"),
    (lambda x: np.tan(x), 0, math.pi/4, math.log(np.sqrt(2)), "-"),
    (lambda x: 1 / (x**2 + 0.01), -1, 1, 100*(math.atan(100) - math.atan(-100))/10, "Pico estreito em x=0 (Lorentziana)"),
    (lambda x: np.sin(x)/x if x != 0 else 1.0, 0, 1, 0.9460830703671830, "Sinc (limite em 0 e 1)"),
    (lambda x: np.exp(np.cos(x)), 0, 2*math.pi, 7.954926521012845, "Funcao periodica"),
    (lambda x: np.sqrt(x), 0, 1, 2/3, "Derivada infinita na borda x=0"),
    (lambda x: 1 / (1 + x**4), 0, 1, 0.866972987339911, "-"),
    (lambda x: x**0.1, 0, 1, 1/1.1, "Quase singularidade"),
    (lambda x: 1 / (x + 1), 0, 100, math.log(101), "Intervalo grande"),
    (lambda x: np.cos(x**2), 0, np.sqrt(math.pi), 0.8948314694841049, "Integral de Fresnel"),
    (lambda x: np.sin(x**2), 0, np.sqrt(math.pi), 0.8948314694841049, "Integral de Fresnel"),
    (lambda x: 1 / math.log(x) if x > 1 else 0, 2, 3, 1.045163780117492, "Logaritmo integral"),
    (lambda x: x**10, 0, 1, 1/11, "Alta potencia"),
    (lambda x: np.exp(x) * np.sin(x), 0, math.pi, (np.exp(math.pi) + 1)/2, "-"),
    (lambda x: 1 / (x**2 - 4), 0, 1, -0.5 * math.log(3)/2, "Perto de polo em x=2"),
    (lambda x: np.cos(np.exp(x)), 0, 2, -0.2201628693317755, "Oscilacao que acelera"),
    (lambda x: np.floor(x), 0, 2, 1.0, "Funcao descontinua (degrau)"),
    (lambda x: np.sign(x - 0.5), 0, 1, 0.0, "Descontinuidade de salto"),
    (lambda x: x * np.sin(1/x) if x != 0 else 0, 0.01, 1, 0.503359123188109, "Oscilacao infinita perto de 0"),
    (lambda x: 1 / (1 + 100*x**2), -1, 1, 2*math.atan(10)/10, "Pico muito agudo"),
    (lambda x: np.sin(x)**10, 0, math.pi, 0.7731263170943633, "Funcao achatada com pico"),
    (lambda x: np.sqrt(np.tan(x)), 0, math.pi/3, 1.0, "-"),
    (lambda x: np.exp(-x) / x if x != 0 else 0, 1, 10, 0.000454, "Exponencial integral"),
    (lambda x: 1 / (x**2 + x + 1), 0, 1, math.pi/(3*math.sqrt(3)), "-"),
    (lambda x: x**2 * np.log(x) if x > 0 else 0, 1, 2, 4*math.log(2) - 7/3, "-"),
    (lambda x: np.cos(x) * np.cos(2*x), 0, math.pi, 0.0, "Ortogonalidade"),
    (lambda x: 1 / np.sqrt(1 - x**2), 0, 0.99, math.asin(0.99), "Perto da singularidade"),
    (lambda x: np.sinh(x), 0, 1, math.cosh(1) - 1, "-"),
    (lambda x: np.cosh(x), 0, 1, math.sinh(1), "-"),
    (lambda x: 1 / (np.exp(x) + np.exp(-x)), 0, 1, math.atan(math.sinh(1)), "Sech(x)"),
    (lambda x: x / (np.exp(x) - 1) if x != 0 else 1, 0.01, 1, 0.949823, "Funcao de Debye"),
    (lambda x: np.log(x)**2, 1, 2, 2*math.log(2)**2 - 4*math.log(2) + 2, "-"),
    (lambda x: np.exp(-1/x) if x > 0 else 0, 0.01, 1, 0.148496, "Essencialmente zero perto de 0"),
    (lambda x: 1 / (1 + x**3), 0, 1, math.log(2)/3 + math.pi/(3*math.sqrt(3)), "-"),
    (lambda x: np.sin(np.sqrt(x)), 0, 1, 2*(math.sin(1) - math.cos(1)) + 2, "-"),
    (lambda x: x * np.cos(x), 0, math.pi/2, math.pi/2 - 1, "-"),
    (lambda x: 1 / (x**4 + 1), -2, 2, 2*math.pi/(2*math.sqrt(2)), "Simetria"),
]


def relative_error(core_val, scipy_val, exact_val=None):
    """Erro relativo entre solucoes"""
    if scipy_val == 0:
        return abs(core_val)
    return abs(core_val - scipy_val) / abs(scipy_val)


def compare_trapezoidal(f, a, b, problem_id, desc, exact_val=None):
    """Compara trapezoidal_repeated core vs scipy"""
    # Nossa implementacao com n=100 subintervalos
    try:
        core_result = trapezoidal_repeated(f, a, b, n=100)
        core_success = core_result["success"]
        core_y = core_result.get("result") if core_success else None
    except Exception as e:
        core_success = False
        core_y = None

    # scipy.integrate.trapezoid (requer pontos)
    try:
        x_eval = np.linspace(a, b, 101)
        y_eval = np.array([f(x) for x in x_eval])
        scipy_result = integrate.trapezoid(y_eval, x_eval)
        scipy_success = True
        scipy_y = scipy_result
    except Exception as e:
        scipy_success = False
        scipy_y = None

    # Erro analitico
    core_error_analitico = None
    if core_success and core_y is not None and exact_val is not None:
        core_error_analitico = abs(core_y - exact_val) / (abs(exact_val) if exact_val != 0 else 1)

    scipy_error_analitico = None
    if scipy_success and scipy_y is not None and exact_val is not None:
        scipy_error_analitico = abs(scipy_y - exact_val) / (abs(exact_val) if exact_val != 0 else 1)

    status = "OK"
    diff = None

    if core_success and scipy_success:
        if core_y is not None and scipy_y is not None:
            diff = abs(core_y - scipy_y)
            if diff > 1e-6:
                status = f"DIFERENCA: {diff:.2e}"
    elif not core_success and not scipy_success:
        status = "AMBOS FALHARAM"
    elif not core_success:
        status = f"SO SCIPY: {str(e) if 'e' in dir() else 'erro desconhecido'}"
    else:
        status = f"SO CORE: scipy falhou"

    return {
        "id": problem_id,
        "core_success": core_success,
        "core_y": core_y,
        "scipy_success": scipy_success,
        "scipy_y": scipy_y,
        "diff": diff,
        "core_error_analitico": core_error_analitico,
        "scipy_error_analitico": scipy_error_analitico,
        "status": status,
        "error": str(e) if not core_success and 'e' in dir() else None
    }


def compare_simpson(f, a, b, problem_id, desc, exact_val=None):
    """Compara simpson 1/3 core vs scipy"""
    # Nossa implementacao com n=100 subintervalos (deve ser par)
    try:
        core_result = simpson(f, a, b, n=100)
        core_success = core_result["success"]
        core_y = core_result.get("result") if core_success else None
    except Exception as e:
        core_success = False
        core_y = None

    # scipy.integrate.simpson
    try:
        x_eval = np.linspace(a, b, 101)
        y_eval = np.array([f(x) for x in x_eval])
        scipy_result = integrate.simpson(y_eval, x_eval)
        scipy_success = True
        scipy_y = scipy_result
    except Exception as e:
        scipy_success = False
        scipy_y = None

    # Erro analitico
    core_error_analitico = None
    if core_success and core_y is not None and exact_val is not None:
        core_error_analitico = abs(core_y - exact_val) / (abs(exact_val) if exact_val != 0 else 1)

    scipy_error_analitico = None
    if scipy_success and scipy_y is not None and exact_val is not None:
        scipy_error_analitico = abs(scipy_y - exact_val) / (abs(exact_val) if exact_val != 0 else 1)

    status = "OK"
    diff = None

    if core_success and scipy_success:
        if core_y is not None and scipy_y is not None:
            diff = abs(core_y - scipy_y)
            if diff > 1e-6:
                status = f"DIFERENCA: {diff:.2e}"
    elif not core_success and not scipy_success:
        status = "AMBOS FALHARAM"
    elif not core_success:
        status = f"SO SCIPY"
    else:
        status = f"SO CORE: scipy falhou"

    return {
        "id": problem_id,
        "core_success": core_success,
        "core_y": core_y,
        "scipy_success": scipy_success,
        "scipy_y": scipy_y,
        "diff": diff,
        "core_error_analitico": core_error_analitico,
        "scipy_error_analitico": scipy_error_analitico,
        "status": status,
        "error": None
    }


def compare_three_eight(f, a, b, problem_id, desc, exact_val=None):
    """Compara 3/8 method core vs scipy"""
    # Nossa implementacao com n=99 subintervalos (deve ser multiplo de 3)
    try:
        core_result = three_eight_method(f, a, b, n=99)
        core_success = core_result["success"]
        core_y = core_result.get("result") if core_success else None
    except Exception as e:
        core_success = False
        core_y = None

    # scipy.integrate.simpson (3/8 e caso especial do Simpson geral)
    try:
        x_eval = np.linspace(a, b, 100)
        y_eval = np.array([f(x) for x in x_eval])
        scipy_result = integrate.simpson(y_eval, x_eval)
        scipy_success = True
        scipy_y = scipy_result
    except Exception as e:
        scipy_success = False
        scipy_y = None

    # Erro analitico
    core_error_analitico = None
    if core_success and core_y is not None and exact_val is not None:
        core_error_analitico = abs(core_y - exact_val) / (abs(exact_val) if exact_val != 0 else 1)

    scipy_error_analitico = None
    if scipy_success and scipy_y is not None and exact_val is not None:
        scipy_error_analitico = abs(scipy_y - exact_val) / (abs(exact_val) if exact_val != 0 else 1)

    status = "OK"
    diff = None

    if core_success and scipy_success:
        if core_y is not None and scipy_y is not None:
            diff = abs(core_y - scipy_y)
            if diff > 1e-6:
                status = f"DIFERENCA: {diff:.2e}"
    elif not core_success and not scipy_success:
        status = "AMBOS FALHARAM"
    elif not core_success:
        status = f"SO SCIPY"
    else:
        status = f"SO CORE: scipy falhou"

    return {
        "id": problem_id,
        "core_success": core_success,
        "core_y": core_y,
        "scipy_success": scipy_success,
        "scipy_y": scipy_y,
        "diff": diff,
        "core_error_analitico": core_error_analitico,
        "scipy_error_analitico": scipy_error_analitico,
        "status": status,
        "error": None
    }


def print_table(results, method_name):
    """Imprime tabela de resultados"""
    print(f"\n{'='*130}")
    print(f"METODO: {method_name}")
    print(f"{'='*130}")
    print(f"{'ID':>3} | {'Status':>18} | {'Core Y':>14} | {'Scipy Y':>14} | {'Diff':>10} | {'Err Anal':>10} | Descricao")
    print(f"{'-'*130}")

    for r in results:
        core_y_str = f"{r['core_y']:.8f}" if r['core_y'] is not None else "N/A"
        scipy_y_str = f"{r['scipy_y']:.8f}" if r['scipy_y'] is not None else "N/A"
        diff_str = f"{r['diff']:.2e}" if r['diff'] is not None else "N/A"
        err_anal_str = f"{r['core_error_analitico']:.2e}" if r['core_error_analitico'] is not None else "N/A"
        desc = PROBLEMS[r['id']-1][4][:30]
        print(f"{r['id']:>3} | {r['status']:>18} | {core_y_str:>14} | {scipy_y_str:>14} | {diff_str:>10} | {err_anal_str:>10} | {desc}")


def main():
    print("="*130)
    print("COMPARACAO: core/integration.py vs scipy.integrate")
    print("50 Problemas de Integracao Numerica")
    print("="*130)

    trapezoidal_results = []
    simpson_results = []
    three_eight_results = []

    for i, (f, a, b, exact_val, desc) in enumerate(PROBLEMS, 1):
        try:
            trapezoidal_results.append(compare_trapezoidal(f, a, b, i, desc, exact_val))
            simpson_results.append(compare_simpson(f, a, b, i, desc, exact_val))
            three_eight_results.append(compare_three_eight(f, a, b, i, desc, exact_val))
        except Exception as e:
            print(f"Problema {i}: erro inesperado - {e}")

    print_table(trapezoidal_results, "TRAPEZIO REPETIDO")
    print_table(simpson_results, "SIMPSON 1/3")
    print_table(three_eight_results, "SIMPSON 3/8")

    # Resumo estatistico
    print("\n" + "="*130)
    print("RESUMO ESTATISTICO")
    print("="*130)

    for method_name, results in [("Trapezio", trapezoidal_results), ("Simpson 1/3", simpson_results), ("Simpson 3/8", three_eight_results)]:
        total = len(results)
        both_success = sum(1 for r in results if r['core_success'] and r['scipy_success'])
        both_fail = sum(1 for r in results if not r['core_success'] and not r['scipy_success'])
        only_core = sum(1 for r in results if r['core_success'] and not r['scipy_success'])
        only_scipy = sum(1 for r in results if not r['core_success'] and r['scipy_success'])

        diffs = [r['diff'] for r in results if r['diff'] is not None and r['diff'] < 1e10]
        max_diff = max(diffs) if diffs else 0
        avg_diff = sum(diffs)/len(diffs) if diffs else 0

        core_anal_errors = [r['core_error_analitico'] for r in results if r['core_error_analitico'] is not None]
        scipy_anal_errors = [r['scipy_error_analitico'] for r in results if r['scipy_error_analitico'] is not None]

        print(f"\n{method_name}:")
        print(f"  Total testes: {total}")
        print(f"  Ambos sucesso: {both_success} ({100*both_success/total:.1f}%)")
        print(f"  Ambos falharam: {both_fail} ({100*both_fail/total:.1f}%)")
        print(f"  So core funcionou: {only_core}")
        print(f"  So scipy funcionou: {only_scipy}")
        print(f"  Maior diferenca: {max_diff:.2e}")
        print(f"  Media diferencas: {avg_diff:.2e}")
        if core_anal_errors:
            print(f"  Erro analitico core (med): {sum(core_anal_errors)/len(core_anal_errors):.2e}")
        if scipy_anal_errors:
            print(f"  Erro analitico scipy (med): {sum(scipy_anal_errors)/len(scipy_anal_errors):.2e}")

    # Listar problemas com divergencia
    print("\n" + "="*130)
    print("PROBLEMAS COM DIVERGENCIA (>1e-6 diferenca)")
    print("="*130)

    for method_name, results in [("Trapezio", trapezoidal_results), ("Simpson 1/3", simpson_results), ("Simpson 3/8", three_eight_results)]:
        divergentes = [r for r in results if r['diff'] is not None and r['diff'] > 1e-6]
        if divergentes:
            print(f"\n{method_name}:")
            for r in divergentes:
                print(f"  ID {r['id']}: diff={r['diff']:.2e}, core_err={r['core_error_analitico']:.2e}" if r['core_error_analitico'] else f"  ID {r['id']}: diff={r['diff']:.2e}")
                print(f"    -> {PROBLEMS[r['id']-1][4]}")

    # Listar falhas
    print("\n" + "="*130)
    print("PROBLEMAS ONDE APENAS UM METODO FUNCIONOU")
    print("="*130)

    for method_name, results in [("Trapezio", trapezoidal_results), ("Simpson 1/3", simpson_results), ("Simpson 3/8", three_eight_results)]:
        so_core = [r for r in results if r['core_success'] and not r['scipy_success']]
        so_scipy = [r for r in results if not r['core_success'] and r['scipy_success']]

        if so_core or so_scipy:
            print(f"\n{method_name}:")
            for r in so_core:
                print(f"  ID {r['id']}: SO CORE funcionou (y={r['core_y']})")
                print(f"    -> {PROBLEMS[r['id']-1][4]}")
            for r in so_scipy:
                print(f"  ID {r['id']}: SO SCIPY funcionou (y={r['scipy_y']})")
                print(f"    -> {PROBLEMS[r['id']-1][4]}")

    # Comparacao entre metodos
    print("\n" + "="*130)
    print("COMPARACAO: Trapézio vs Simpson 1/3 vs Simpson 3/8 (mesmos problemas)")
    print("="*130)

    print(f"\n{'ID':>3} | {'Trap Err':>12} | {'Simp 1/3 Err':>12} | {'Simp 3/8 Err':>12} | {'Descricao':>25}")
    print(f"{'-'*80}")

    for i in range(min(len(trapezoidal_results), len(simpson_results), len(three_eight_results))):
        t = trapezoidal_results[i]
        s = simpson_results[i]
        te = three_eight_results[i]
        t_err = t['core_error_analitico']
        s_err = s['core_error_analitico']
        te_err = te['core_error_analitico']

        if t_err is not None and s_err is not None and te_err is not None:
            print(f"{i+1:>3} | {t_err:>12.2e} | {s_err:>12.2e} | {te_err:>12.2e} | {PROBLEMS[i][4][:25]}")


if __name__ == "__main__":
    main()
