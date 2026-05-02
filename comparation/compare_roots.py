"""
Comparação: Implementações core/roots.py vs scipy.optimize
50 exemplos de problemas de raízes
"""

import math
import numpy as np
from core.roots import bisection, newton, secant
from scipy import optimize

# 50 Problemas de Raízes
PROBLEMS = [
    # ID: (f, df, interval/chute, descricao)
    (lambda x: x**10 - 1, lambda x: 10*x**9, (0, 1.3), "Bisseção lenta; Newton converge rápido"),
    (lambda x: (x-1)**3, lambda x: 3*(x-1)**2, (0, 2), "Raiz múltipla: Newton perde convergência quadrática"),
    (lambda x: x**3 - x - 1, lambda x: 3*x**2 - 1, (1, 2), "Newton: x0=0 leva a f'(x)=0"),
    (lambda x: math.atan(x), lambda x: 1/(1+x**2), (0.5, 2), "Newton: oscilação se x0 longe da raiz"),
    (lambda x: math.copysign(1, x-1) * math.sqrt(abs(x-1)), lambda x: 0.5/math.sqrt(abs(x-1)) if x != 1 else float('inf'), (0.5, 1.5), "Newton: oscilação entre pontos simétricos"),
    (lambda x: x * math.exp(-x), lambda x: (1-x)*math.exp(-x), (0.5, 3), "Newton: f'(x) tende a zero para x grande"),
    (lambda x: math.cos(x) - x, lambda x: -math.sin(x) - 1, (0, 1), "Comparação padrão de convergência"),
    (lambda x: x**2, lambda x: 2*x, (-1, 1), "Bisseção falha (f(a)f(b) > 0), mas há raiz em 0"),
    (lambda x: 1/x - 1 if x != 0 else float('inf'), lambda x: -1/x**2 if x != 0 else float('inf'), (0.5, 2), "Função descontínua perto de 0"),
    (lambda x: math.tan(x) - x, lambda x: 1/math.cos(x)**2 - 1, (4, 4.7), "Raízes próximas de assíntotas"),
    (lambda x: x**3 - 2*x**2 - 4*x + 8, lambda x: 3*x**2 - 4*x - 4, (1.9, 2.1), "Raiz dupla em x=2"),
    (lambda x: math.exp(x) - 3*x, lambda x: math.exp(x) - 3, (0, 1), "Newton: sensibilidade ao chute inicial"),
    (lambda x: math.log(x) - 1, lambda x: 1/x, (2, 3), "Secante: instabilidade se x0, x1 próximos"),
    (lambda x: x**2 - math.sin(x), lambda x: 2*x - math.cos(x), (0.5, 1), "Newton vs Secante em funções transcendentais"),
    (lambda x: (x-1)**2 * (x-2), lambda x: 2*(x-1)*(x-2) + (x-1)**2, (0.5, 1.5), "Raiz múltipla em x=1"),
    (lambda x: math.sin(x) - 0.5*x, lambda x: math.cos(x) - 0.5, (1, 3), "Múltiplas raízes no intervalo"),
    (lambda x: x**4 - 10*x**3 + 35*x**2 - 50*x + 24, lambda x: 4*x**3 - 30*x**2 + 70*x - 50, (0, 5), "Polinômio de Wilkinson (raízes 1,2,3,4)"),
    (lambda x: math.sqrt(x) - math.cos(x) if x >= 0 else float('nan'), lambda x: 0.5/math.sqrt(x) + math.sin(x) if x > 0 else float('inf'), (0, 1), "Domínio restrito (x >= 0)"),
    (lambda x: x**3 - 0.001, lambda x: 3*x**2, (0, 1), "Raiz muito pequena, precisão numérica"),
    (lambda x: 1/(x-0.3) if x != 0.3 else float('inf'), lambda x: -1/(x-0.3)**2 if x != 0.3 else float('inf'), (0, 1), "Bisseção falha: descontinuidade"),
    (lambda x: math.cos(x) + 1, lambda x: -math.sin(x), (3, 4), "Raiz onde f(x) não cruza o eixo"),
    (lambda x: x**2 - 2, lambda x: 2*x, (1, 2), "Cálculo de sqrt(2)"),
    (lambda x: x - math.exp(-x), lambda x: 1 + math.exp(-x), (0, 1), "Convergência rápida para Newton"),
    (lambda x: x**3 - 10*x**2 + 5, lambda x: 3*x**2 - 20*x, (0, 1), "Newton: x0=0.6 leva a um ciclo"),
    (lambda x: 8*x**4 - 8*x**2 + 1, lambda x: 32*x**3 - 16*x, (0, 0.5), "Polinômio de Chebyshev"),
    (lambda x: (x-1) * math.exp(-x), lambda x: (2-x)*math.exp(-x), (0, 2), "Newton: f'(x) pequeno para x > 1"),
    (lambda x: x**5 - x - 1, lambda x: 5*x**4 - 1, (1, 2), "Polinômio clássico sem solução analítica"),
    (lambda x: math.log10(x) - x + 2, lambda x: 1/(x*math.log(10)) - 1, (2, 3), "Função com crescimento lento"),
    (lambda x: math.sin(x**2) - x, lambda x: 2*x*math.cos(x**2) - 1, (0.5, 1), "Função altamente não-linear"),
    (lambda x: (x-2)**9, lambda x: 9*(x-2)**8, (1, 3), "Newton: extremamente lento para raízes de alta multiplicidade"),
    (lambda x: x - math.cos(x), lambda x: 1 + math.sin(x), (0, 2), "Newton: convergência global lenta"),
    (lambda x: math.exp(-x**2) - x, lambda x: -2*x*math.exp(-x**2) - 1, (0, 1), "Função gaussiana"),
    (lambda x: x**3 - 3*x + 2, lambda x: 3*x**2 - 3, (0.5, 1.5), "Raiz dupla em x=1"),
    (lambda x: x**2 - 1.1*x + 0.3, lambda x: 2*x - 1.1, (0, 0.5), "Raízes muito próximas (0.5 e 0.6)"),
    (lambda x: 1 - 4*x*math.cos(x), lambda x: -4*math.cos(x) + 4*x*math.sin(x), (0, 1), "Newton: derivada oscilante"),
    (lambda x: x**3 - 2*x - 5, lambda x: 3*x**2 - 2, (2, 3), "Exemplo histórico de Wallis"),
    (lambda x: x - math.sin(x) - 0.25, lambda x: 1 - math.cos(x), (1, 2), "Newton: f'(x) pequeno perto de 0"),
    (lambda x: (x-1)**5, lambda x: 5*(x-1)**4, (0, 2), "Raiz de multiplicidade m=5"),
    (lambda x: x**2 + 1, lambda x: 2*x, (-1, 1), "Sem raízes reais"),
    (lambda x: math.sinh(x) - 1, lambda x: math.cosh(x), (0, 1), "Função hiperbólica"),
    (lambda x: x**3 - x**2 - x + 1, lambda x: 3*x**2 - 2*x - 1, (0.5, 1.5), "Raiz dupla em x=1"),
    (lambda x: 2*x - math.exp(-x), lambda x: 2 + math.exp(-x), (0, 1), "Newton vs Bisseção"),
    (lambda x: x**4 - 5*x**2 + 4, lambda x: 4*x**3 - 10*x, (0.5, 1.5), "Raízes em 1, 2, -1, -2"),
    (lambda x: math.sqrt(abs(x)), lambda x: 0.5/math.sqrt(abs(x)) if x != 0 else float('inf'), (0.5, 2), "Newton: oscila entre 1 e -1"),
    (lambda x: x**3 - 7*x**2 + 14*x - 8, lambda x: 3*x**2 - 14*x + 14, (0, 5), "Raízes 1, 2, 4"),
    (lambda x: math.cos(x) - x**3, lambda x: -math.sin(x) - 3*x**2, (0, 1), "Newton: convergência rápida"),
    (lambda x: math.exp(x) - x - 2, lambda x: math.exp(x) - 1, (1, 2), "Newton: chute inicial baixo"),
    (lambda x: x**2 - 10, lambda x: 2*x, (3, 4), "Cálculo de sqrt(10)"),
    (lambda x: x - math.tan(x), lambda x: 1 - 1/math.cos(x)**2, (4.4, 4.6), "Newton: perto de assíntota vertical"),
    (lambda x: (x-1)*(x-2)*(x-3), lambda x: (x-2)*(x-3) + (x-1)*(x-3) + (x-1)*(x-2), (1.5, 2.5), "Secante: escolha de x0, x1 entre raízes"),
]


def safe_float(val):
    """Converte para float seguro"""
    if val is None:
        return None
    try:
        if np.isnan(val) or np.isinf(val):
            return None
        return float(val)
    except:
        return None


def safe_f(f, x):
    """Chama função f(x) de forma segura"""
    try:
        val = f(x)
        if np.isnan(val) or np.isinf(val):
            return float('nan')
        return val
    except:
        return float('nan')


def safe_df(df, x):
    """Chama derivada df(x) de forma segura"""
    try:
        val = df(x)
        if np.isnan(val) or np.isinf(val):
            return float('nan')
        return val
    except:
        return float('nan')


def compare_bisection(f, a, b, problem_id, desc):
    """Compara bisection core vs scipy"""
    # Verificar se função é válida nos extremos
    fa, fb = safe_f(f, a), safe_f(f, b)
    if np.isnan(fa) or np.isnan(fb) or np.isinf(fa) or np.isinf(fb):
        return {
            "id": problem_id,
            "core_success": False,
            "core_root": None,
            "core_iters": 0,
            "scipy_success": False,
            "scipy_root": None,
            "diff": None,
            "status": "INVÁLIDO NOS EXTREMOS",
            "error": "Função inválida em a ou b"
        }

    core_result = bisection(f, a, b, tol=1e-10, max_iter=1000)

    # scipy bisect
    try:
        scipy_root = optimize.bisect(f, a, b, xtol=1e-10, maxiter=1000)
        scipy_success = True
    except (ValueError, RuntimeError, OverflowError) as e:
        scipy_root = None
        scipy_success = False

    # Comparação
    core_root = safe_float(core_result.get("root"))

    status = "OK"
    diff = None

    if core_result["success"] and scipy_success:
        if core_root is not None and scipy_root is not None:
            diff = abs(core_root - scipy_root)
            if diff > 1e-6:
                status = f"DIFERENÇA: {diff:.2e}"
    elif not core_result["success"] and not scipy_success:
        status = "AMBOS FALHARAM"
    elif not core_result["success"]:
        status = f"SÓ SCIPY: {core_result.get('error', 'erro desconhecido')}"
    else:
        status = f"SÓ CORE: scipy falhou"

    return {
        "id": problem_id,
        "core_success": core_result["success"],
        "core_root": core_root,
        "core_iters": core_result.get("iterations", 0),
        "scipy_success": scipy_success,
        "scipy_root": safe_float(scipy_root),
        "diff": diff,
        "status": status,
        "error": core_result.get("error") if not core_result["success"] else None
    }


def compare_newton(f, df, x0, problem_id, desc):
    """Compara newton core vs scipy"""
    # Verificar se função e derivada são válidas no chute inicial
    fx0, dfx0 = safe_f(f, x0), safe_df(df, x0)
    if np.isnan(fx0) or np.isnan(dfx0) or np.isinf(fx0) or np.isinf(dfx0):
        return {
            "id": problem_id,
            "core_success": False,
            "core_root": None,
            "core_iters": 0,
            "scipy_success": False,
            "scipy_root": None,
            "diff": None,
            "status": "INVÁLIDO NO CHUTE INICIAL",
            "error": "Função ou derivada inválida em x0"
        }

    core_result = newton(f, df, x0, tol=1e-10, max_iter=1000)

    # scipy newton
    try:
        scipy_root = optimize.newton(f, x0, fprime=df, tol=1e-10, maxiter=1000)
        scipy_success = True
    except (RuntimeError, ZeroDivisionError, OverflowError, ValueError) as e:
        scipy_root = None
        scipy_success = False

    core_root = safe_float(core_result.get("root"))

    status = "OK"
    diff = None

    if core_result["success"] and scipy_success:
        if core_root is not None and scipy_root is not None:
            diff = abs(core_root - scipy_root)
            if diff > 1e-6:
                status = f"DIFERENÇA: {diff:.2e}"
    elif not core_result["success"] and not scipy_success:
        status = "AMBOS FALHARAM"
    elif not core_result["success"]:
        status = f"SÓ SCIPY: {core_result.get('error', 'erro desconhecido')}"
    else:
        status = f"SÓ CORE: scipy falhou"

    return {
        "id": problem_id,
        "core_success": core_result["success"],
        "core_root": core_root,
        "core_iters": core_result.get("iterations", 0),
        "scipy_success": scipy_success,
        "scipy_root": safe_float(scipy_root),
        "diff": diff,
        "status": status,
        "error": core_result.get("error") if not core_result["success"] else None
    }


def compare_secant(f, x0, x1, problem_id, desc):
    """Compara secant core vs scipy"""
    # Verificar se função é válida nos chutes
    fx0, fx1 = safe_f(f, x0), safe_f(f, x1)
    if np.isnan(fx0) or np.isnan(fx1) or np.isinf(fx0) or np.isinf(fx1):
        return {
            "id": problem_id,
            "core_success": False,
            "core_root": None,
            "core_iters": 0,
            "scipy_success": False,
            "scipy_root": None,
            "diff": None,
            "status": "INVÁLIDO NOS CHUTES",
            "error": "Função inválida em x0 ou x1"
        }

    core_result = secant(f, x0, x1, tol=1e-10, max_iter=1000)

    # scipy newton sem fprime usa secante
    try:
        scipy_root = optimize.newton(f, x0, tol=1e-10, maxiter=1000)
        scipy_success = True
    except (RuntimeError, ZeroDivisionError, OverflowError, ValueError) as e:
        scipy_root = None
        scipy_success = False

    core_root = safe_float(core_result.get("root"))

    status = "OK"
    diff = None

    if core_result["success"] and scipy_success:
        if core_root is not None and scipy_root is not None:
            diff = abs(core_root - scipy_root)
            if diff > 1e-6:
                status = f"DIFERENÇA: {diff:.2e}"
    elif not core_result["success"] and not scipy_success:
        status = "AMBOS FALHARAM"
    elif not core_result["success"]:
        status = f"SÓ SCIPY: {core_result.get('error', 'erro desconhecido')}"
    else:
        status = f"SÓ CORE: scipy falhou"

    return {
        "id": problem_id,
        "core_success": core_result["success"],
        "core_root": core_root,
        "core_iters": core_result.get("iterations", 0),
        "scipy_success": scipy_success,
        "scipy_root": safe_float(scipy_root),
        "diff": diff,
        "status": status,
        "error": core_result.get("error") if not core_result["success"] else None
    }


def print_table(results, method_name):
    """Imprime tabela de resultados"""
    print(f"\n{'='*100}")
    print(f"MÉTODO: {method_name}")
    print(f"{'='*100}")
    print(f"{'ID':>3} | {'Status':>25} | {'Core Root':>15} | {'Scipy Root':>15} | {'Diff':>12} | {'Iters':>6} | Descrição")
    print(f"{'-'*100}")

    for r in results:
        core_root_str = f"{r['core_root']:.8f}" if r['core_root'] is not None else "N/A"
        scipy_root_str = f"{r['scipy_root']:.8f}" if r['scipy_root'] is not None else "N/A"
        diff_str = f"{r['diff']:.2e}" if r['diff'] is not None else "N/A"

        # Truncar descrição
        desc = PROBLEMS[r['id']-1][3][:45]

        print(f"{r['id']:>3} | {r['status']:>25} | {core_root_str:>15} | {scipy_root_str:>15} | {diff_str:>12} | {r['core_iters']:>6} | {desc}")


def main():
    print("="*100)
    print("COMPARAÇÃO: core/roots.py vs scipy.optimize")
    print("50 Problemas de Raízes")
    print("="*100)

    bisection_results = []
    newton_results = []
    secant_results = []

    for i, (f, df, interval, desc) in enumerate(PROBLEMS, 1):
        try:
            # Bisseção
            if isinstance(interval, tuple) and len(interval) == 2:
                a, b = interval
                bisection_results.append(compare_bisection(f, a, b, i, desc))
            else:
                x0 = interval if not isinstance(interval, tuple) else interval[0]
                bisection_results.append(compare_bisection(f, x0-1, x0+1, i, desc))

            # Newton
            x0 = interval[0] if isinstance(interval, tuple) else interval
            newton_results.append(compare_newton(f, df, x0, i, desc))

            # Secante
            if isinstance(interval, tuple) and len(interval) == 2:
                secant_results.append(compare_secant(f, interval[0], interval[1], i, desc))
            else:
                x0 = interval if not isinstance(interval, tuple) else interval[0]
                secant_results.append(compare_secant(f, x0, x0+0.1, i, desc))
        except Exception as e:
            print(f"Problema {i}: erro inesperado - {e}")

    # Imprimir resultados
    print_table(bisection_results, "BISSEÇÃO")
    print_table(newton_results, "NEWTON")
    print_table(secant_results, "SECANTE")

    # Resumo estatístico
    print("\n" + "="*100)
    print("RESUMO ESTATÍSTICO")
    print("="*100)

    for method_name, results in [("Bisseção", bisection_results), ("Newton", newton_results), ("Secante", secant_results)]:
        total = len(results)
        both_success = sum(1 for r in results if r['core_success'] and r['scipy_success'])
        both_fail = sum(1 for r in results if not r['core_success'] and not r['scipy_success'])
        only_core = sum(1 for r in results if r['core_success'] and not r['scipy_success'])
        only_scipy = sum(1 for r in results if not r['core_success'] and r['scipy_success'])
        diffs = [r['diff'] for r in results if r['diff'] is not None]
        max_diff = max(diffs) if diffs else 0
        avg_diff = sum(diffs)/len(diffs) if diffs else 0

        print(f"\n{method_name}:")
        print(f"  Total testes: {total}")
        print(f"  Ambos sucesso: {both_success} ({100*both_success/total:.1f}%)")
        print(f"  Ambos falharam: {both_fail} ({100*both_fail/total:.1f}%)")
        print(f"  Só core funcionou: {only_core}")
        print(f"  Só scipy funcionou: {only_scipy}")
        print(f"  Maior diferença: {max_diff:.2e}")
        print(f"  Média diferenças: {avg_diff:.2e}")

    # Listar problemas com divergência
    print("\n" + "="*100)
    print("PROBLEMAS COM DIVERGÊNCIA (>1e-6 diferença)")
    print("="*100)

    for method_name, results in [("Bisseção", bisection_results), ("Newton", newton_results), ("Secante", secant_results)]:
        divergentes = [r for r in results if r['diff'] is not None and r['diff'] > 1e-6]
        if divergentes:
            print(f"\n{method_name}:")
            for r in divergentes:
                print(f"  ID {r['id']}: core={r['core_root']:.10f}, scipy={r['scipy_root']:.10f}, diff={r['diff']:.2e}")
                print(f"    -> {PROBLEMS[r['id']-1][3]}")

    # Listar falhas
    print("\n" + "="*100)
    print("PROBLEMAS ONDE APENAS UM MÉTODO FUNCIONOU")
    print("="*100)

    for method_name, results in [("Bisseção", bisection_results), ("Newton", newton_results), ("Secante", secant_results)]:
        so_core = [r for r in results if r['core_success'] and not r['scipy_success']]
        so_scipy = [r for r in results if not r['core_success'] and r['scipy_success']]

        if so_core or so_scipy:
            print(f"\n{method_name}:")
            for r in so_core:
                print(f"  ID {r['id']}: SÓ CORE funcionou (root={r['core_root']})")
                print(f"    -> {PROBLEMS[r['id']-1][3]}")
                print(f"    Erro scipy: falhou")
            for r in so_scipy:
                print(f"  ID {r['id']}: SÓ SCIPY funcionou (root={r['scipy_root']})")
                print(f"    -> {PROBLEMS[r['id']-1][3]}")
                print(f"    Erro core: {r['error']}")


if __name__ == "__main__":
    main()
