"""
Comparacao: Implementacoes core/interpolation.py vs scipy.interpolate
50 exemplos de Interpolacao
"""

import numpy as np
from core.interpolation import newton_interpolation, lagrange_interpolation
from scipy import interpolate

# 50 Problemas de Interpolacao
PROBLEMS = [
    # ID: (pontos_x, pontos_y, x_eval, funcao_base, descricao)
    ([0, 1, 2], [0, 1, 4], 1.5, lambda x: x**2, "Interpolacao quadratica basica"),
    ([-1, 0, 1], [1, 0, 1], 0.5, lambda x: abs(x), "Ponto nao derivavel em x=0"),
    ([0, 1, 2], [1, 2.718, 7.389], 1.5, lambda x: np.exp(x), "Aproximacao exponencial"),
    (np.linspace(-5, 5, 11), 1/(1+np.linspace(-5, 5, 11)**2), 3.5, lambda x: 1/(1+x**2), "Fenomeno de Runge (11 pontos)"),
    (np.linspace(-5, 5, 21), 1/(1+np.linspace(-5, 5, 21)**2), 4.5, lambda x: 1/(1+x**2), "Runge intensificado (21 pontos)"),
    (5*np.cos((2*np.arange(11)+1)*np.pi/(2*11)), 1/(1+(5*np.cos((2*np.arange(11)+1)*np.pi/(2*11)))**2), 3.5, lambda x: 1/(1+x**2), "Chebyshev - mitigacao Runge"),
    ([1, 2, 3], [0, 0.693, 1.098], 2.5, lambda x: np.log(x), "Logaritmica"),
    ([0, np.pi/2, np.pi], [0, 1, 0], np.pi/4, lambda x: np.sin(x), "Trigonometrica"),
    ([0, 1, 2, 3], [0, 1, 0, 1], 1.5, None, "Oscilante - grau 3"),
    ([0, 1, 2, 3], [0, 1, 8, 27], 1.5, lambda x: x**3, "Newton coeficientes exatos"),
    ([0, 1, 2, 3], [0, 1, 2, 3], 1.5, lambda x: x, "Polinomio degenera para reta"),
    ([0, 1, 2], [1, 1, 1], 1.5, lambda x: 1, "Polinomio constante"),
    ([1, 1.0001, 2], [1, 1.0002, 2], 1.5, lambda x: x, "Quase coincidentes - instabilidade"),
    ([0, 1, 2], [0, 100, 0], 0.5, None, "Pico agudo - overshoot"),
    ([0, 1, 2, 3, 4], [0, 1, 4, 9, 16], 2.5, lambda x: x**2, "Grau redundante"),
    ([-2, -1, 0, 1, 2], [4, 1, 0, 1, 4], 0.5, lambda x: x**2, "Parabola simetrica"),
    ([0, 1, 2, 3], [0, 2, 2, 0], 1.5, None, "Forma de sino"),
    ([1, 2, 3], [1, 0.5, 0.333], 2.5, lambda x: 1/x, "Hiperbole"),
    ([0, 1, 4, 9], [0, 1, 2, 3], 5, lambda x: np.sqrt(x), "Espacamento nao uniforme"),
    ([0, 0.1, 0.5], [0, 0.316, 0.707], 0.25, lambda x: np.sqrt(x), "Perto da origem - derivada infinita"),
    (np.random.RandomState(42).rand(5)*10, np.random.RandomState(42).rand(5)*10, 5, None, "Pontos aleatorios"),
    ([0, 1, 2, 3, 4], [0, 1, 0, -1, 0], 1.5, None, "Senoide discreta"),
    ([1, 2, 3, 4, 5], [2, 4, 8, 16, 32], 3.5, lambda x: 2**x, "Crescimento rapido"),
    ([0, 1, 2, 3], [0, 0, 0, 1], 1.5, None, "Degrau suave"),
    ([-3, 3], [-27, 27], 0, lambda x: x, "Reta - 2 pontos"),
    ([0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5], 2.5, lambda x: x, "Linear - ordem >1 zero"),
    ([0, 1, 2, 3, 4, 5], [0, 1, 4, 9, 16, 25], 2.5, lambda x: x**2, "Quadratica - ordem >2 zero"),
    ([0, 1, 2, 3, 4], [0, 1, 8, 27, 64], 2.5, lambda x: x**3, "Cubica - ordem >3 zero"),
    ([0, 1, 2, 3], [0, 1, 16, 81], 1.5, lambda x: x**4, "Quartica"),
    ([0, 1, 2, 3], [1, 0.5, 0.25, 0.125], 1.5, lambda x: 0.5**x, "Decaimento"),
    ([0, 1, 2, 3, 4, 5], [0, 1, 0, 1, 0, 1], 2.5, None, "Zig-zag - oscilacao"),
    ([1, 2, 3, 4, 5], [1, 2, 3, 4, 10], 4.5, None, "Outlier"),
    ([0, 1, 2, 3], [0, 1, 1.414, 1.732], 1.5, lambda x: np.sqrt(x), "Raiz quadrada"),
    ([0, 0.5, 1], [0, 0.479, 0.841], 0.75, lambda x: np.sin(x), "Seno"),
    ([0, 0.5, 1], [1, 0.877, 0.540], 0.75, lambda x: np.cos(x), "Cosseno"),
    ([0, 1, 2], [0, 1.175, 3.626], 1.5, lambda x: np.sinh(x), "Seno hiperbolico"),
    ([0, 1, 2], [1, 1.543, 3.762], 1.5, lambda x: np.cosh(x), "Cosseno hiperbolico"),
    ([0, 1, 2], [0, 0.761, 0.964], 1.5, lambda x: np.tanh(x), "Tangente hiperbolica"),
    ([2, 4, 8], [0.693, 1.386, 2.079], 6, lambda x: np.log(x), "Espacamento logaritmico"),
    ([1, 10, 100], [1, 1, 1], 50, lambda x: 1, "Constante - espacamento grande"),
    ([0, 0.01, 0.04], [0, 0.1, 0.2], 0.02, lambda x: np.sqrt(x), "Muito perto de zero"),
    ([0, 1, 2, 3, 4], [0, 1, 0, -1, 0], 2.5, None, "Ciclo trigonometrico"),
    ([0, 1, 2, 3, 4], [0, 1, 4, 8, 16], 2.5, lambda x: 2**x, "Potencia de 2"),
    ([0, 1, 2, 3, 4], [0, 1, 3, 9, 27], 2.5, lambda x: 3**x, "Potencia de 3"),
    ([0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5], 2.5, lambda x: x, "Identidade"),
    ([0, 1, 2, 3], [5, 5, 5, 5], 1.5, lambda x: 5, "Constante 5"),
    ([1, 2, 3, 4], [1, 4, 1, 4], 2.5, None, "M formato"),
    ([1, 2, 3, 4], [4, 1, 4, 1], 2.5, None, "W formato"),
    ([0, 1, 2, 3, 4], [0, 1, 0, 1, 0], 1.5, None, "Dentes de serra"),
    ([0, 1, 2, 3, 4], [0, 1, 2, 3, 10], 3.5, None, "Salto no final"),
]


def relative_error(y_core, y_scipy):
    """Erro relativo entre solucoes"""
    y_c = np.array(y_core, dtype=float)
    y_s = np.array(y_scipy, dtype=float)
    norm_diff = np.linalg.norm(y_c - y_s)
    norm_s = np.linalg.norm(y_s)
    if norm_s == 0:
        return np.linalg.norm(y_c)
    return norm_diff / norm_s


def compare_newton(x_points, y_points, x_eval, problem_id, desc, funcao_base=None):
    """Compara Newton interpolation core vs scipy"""
    x_pts = np.array(x_points, dtype=float)
    y_pts = np.array(y_points, dtype=float)

    # Nossa implementacao
    try:
        core_result = newton_interpolation(x_pts, y_pts, x_eval)
        core_success = core_result["success"]
        core_y = core_result.get("result") if core_success else None
    except Exception as e:
        core_success = False
        core_y = None

    # scipy.interpolate.lagrange (polinomio unico, serve para Newton tambem)
    try:
        poly = interpolate.lagrange(x_pts, y_pts)
        scipy_y = poly(x_eval)
        scipy_success = True
    except Exception as e:
        scipy_y = None
        scipy_success = False

    # Calcular erro analitico se funcao base disponivel
    core_error_analitico = None
    if core_success and core_y is not None and funcao_base is not None:
        try:
            y_exact = funcao_base(x_eval)
            core_error_analitico = abs(core_y - y_exact) / (abs(y_exact) if y_exact != 0 else 1)
        except:
            pass

    scipy_error_analitico = None
    if scipy_success and scipy_y is not None and funcao_base is not None:
        try:
            y_exact = funcao_base(x_eval)
            scipy_error_analitico = abs(scipy_y - y_exact) / (abs(y_exact) if y_exact != 0 else 1)
        except:
            pass

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
        status = f"SO SCIPY: {core_result.get('error', 'erro desconhecido')}"
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
        "error": core_result.get("error") if not core_success else None
    }


def compare_lagrange(x_points, y_points, x_eval, problem_id, desc, funcao_base=None):
    """Compara Lagrange interpolation core vs scipy"""
    x_pts = np.array(x_points, dtype=float)
    y_pts = np.array(y_points, dtype=float)

    # Nossa implementacao
    try:
        core_result = lagrange_interpolation(x_pts, y_points, x_eval)
        core_success = core_result["success"]
        core_y = core_result.get("result") if core_success else None
    except Exception as e:
        core_success = False
        core_y = None

    # scipy.interpolate.lagrange
    try:
        poly = interpolate.lagrange(x_pts, y_pts)
        scipy_y = poly(x_eval)
        scipy_success = True
    except Exception as e:
        scipy_y = None
        scipy_success = False

    # Calcular erro analitico se funcao base disponivel
    core_error_analitico = None
    if core_success and core_y is not None and funcao_base is not None:
        try:
            y_exact = funcao_base(x_eval)
            core_error_analitico = abs(core_y - y_exact) / (abs(y_exact) if y_exact != 0 else 1)
        except:
            pass

    scipy_error_analitico = None
    if scipy_success and scipy_y is not None and funcao_base is not None:
        try:
            y_exact = funcao_base(x_eval)
            scipy_error_analitico = abs(scipy_y - y_exact) / (abs(y_exact) if y_exact != 0 else 1)
        except:
            pass

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
        status = f"SO SCIPY: {core_result.get('error', 'erro desconhecido')}"
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
        "error": core_result.get("error") if not core_success else None
    }


def print_table(results, method_name):
    """Imprime tabela de resultados"""
    print(f"\n{'='*120}")
    print(f"METODO: {method_name}")
    print(f"{'='*120}")
    print(f"{'ID':>3} | {'Status':>20} | {'Core Y':>12} | {'Scipy Y':>12} | {'Diff':>10} | {'Err Anal':>10} | Descricao")
    print(f"{'-'*120}")

    for r in results:
        core_y_str = f"{r['core_y']:.6f}" if r['core_y'] is not None else "N/A"
        scipy_y_str = f"{r['scipy_y']:.6f}" if r['scipy_y'] is not None else "N/A"
        diff_str = f"{r['diff']:.2e}" if r['diff'] is not None else "N/A"
        err_anal_str = f"{r['core_error_analitico']:.2e}" if r['core_error_analitico'] is not None else "N/A"
        desc = PROBLEMS[r['id']-1][4][:35]
        print(f"{r['id']:>3} | {r['status']:>20} | {core_y_str:>12} | {scipy_y_str:>12} | {diff_str:>10} | {err_anal_str:>10} | {desc}")


def main():
    print("="*120)
    print("COMPARACAO: core/interpolation.py vs scipy.interpolate")
    print("50 Problemas de Interpolacao")
    print("="*120)

    newton_results = []
    lagrange_results = []

    for i, (x_pts, y_pts, x_eval, funcao_base, desc) in enumerate(PROBLEMS, 1):
        try:
            newton_results.append(compare_newton(x_pts, y_pts, x_eval, i, desc, funcao_base))
            lagrange_results.append(compare_lagrange(x_pts, y_pts, x_eval, i, desc, funcao_base))
        except Exception as e:
            print(f"Problema {i}: erro inesperado - {e}")

    print_table(newton_results, "NEWTON")
    print_table(lagrange_results, "LAGRANGE")

    # Resumo estatistico
    print("\n" + "="*120)
    print("RESUMO ESTATISTICO")
    print("="*120)

    for method_name, results in [("Newton", newton_results), ("Lagrange", lagrange_results)]:
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
    print("\n" + "="*120)
    print("PROBLEMAS COM DIVERGENCIA (>1e-6 diferenca)")
    print("="*120)

    for method_name, results in [("Newton", newton_results), ("Lagrange", lagrange_results)]:
        divergentes = [r for r in results if r['diff'] is not None and r['diff'] > 1e-6]
        if divergentes:
            print(f"\n{method_name}:")
            for r in divergentes:
                print(f"  ID {r['id']}: diff={r['diff']:.2e}")
                print(f"    -> {PROBLEMS[r['id']-1][4]}")

    # Listar falhas
    print("\n" + "="*120)
    print("PROBLEMAS ONDE APENAS UM METODO FUNCIONOU")
    print("="*120)

    for method_name, results in [("Newton", newton_results), ("Lagrange", lagrange_results)]:
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
                print(f"    Erro core: {r['error']}")

    # Comparacao Newton vs Lagrange
    print("\n" + "="*120)
    print("COMPARACAO: Newton vs Lagrange (mesmos problemas)")
    print("="*120)

    print(f"\n{'ID':>3} | {'Newton Err':>12} | {'Lagrange Err':>12} | {'Descricao':>35}")
    print(f"{'-'*70}")

    for i in range(min(len(newton_results), len(lagrange_results))):
        n = newton_results[i]
        l = lagrange_results[i]
        n_err = n['core_error_analitico']
        l_err = l['core_error_analitico']

        if n_err is not None and l_err is not None:
            print(f"{i+1:>3} | {n_err:>12.2e} | {l_err:>12.2e} | {PROBLEMS[i][4][:35]}")


if __name__ == "__main__":
    main()
