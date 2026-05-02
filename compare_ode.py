"""
Comparacao: Implementacoes core/ode.py vs scipy.integrate
50 exemplos de Equacoes Diferenciais Ordinarias
"""

import numpy as np
import math
from core.ode import euler_method, runge_kutta_4
from scipy import integrate

# 50 Problemas de EDOs
# (f, y0, t0, tf, h, solucao_analitica, descricao)
PROBLEMS = [
    (lambda t, y: y, 1.0, 0, 1, 0.1, lambda t: math.exp(t), "Crescimento exponencial"),
    (lambda t, y: -y, 1.0, 0, 1, 0.1, lambda t: math.exp(-t), "Decaimento exponencial"),
    (lambda t, y: -100*y, 1.0, 0, 0.1, 0.001, lambda t: math.exp(-100*t), "Stiff: Euler exige h < 0.02"),
    (lambda t, y: y - t**2 + 1, 0.5, 0, 1, 0.1, lambda t: (t+1)**2 - 0.5*math.exp(t), "Exemplo Burden"),
    (lambda t, y: math.sin(t), 0.0, 0, math.pi, 0.1, lambda t: 1 - math.cos(t), "Integracao oscilante"),
    (lambda t, y: y * math.cos(t), 1.0, 0, 2, 0.1, lambda t: math.exp(math.sin(t)), "y = e^sin(t)"),
    (lambda t, y: -2*t*y, 1.0, 0, 1, 0.1, lambda t: math.exp(-t**2), "Gaussiana"),
    (lambda t, y: 1 / (1 + t**2), 0.0, 0, 1, 0.1, lambda t: math.atan(t), "y = arctan(t)"),
    (lambda t, y: y**2, 1.0, 0, 0.9, 0.01, lambda t: 1/(1-t), "Explosao em tempo finito"),
    (lambda t, y: math.sqrt(y) if y >= 0 else 0, 0.0, 0, 1, 0.1, lambda t: t**2/4, "Nao-unicidade"),
    (lambda t, y: -50*(y - math.cos(t)), 0.0, 0, 1, 0.01, lambda t: (50/2501)*(math.cos(t) + 50*math.sin(t)) - (50/2501)*math.exp(-50*t), "Stiff: segue cos(t)"),
    (lambda t, y: t + y, 1.0, 0, 1, 0.1, lambda t: 2*math.exp(t) - t - 1, "Linear simples"),
    (lambda t, y: (y/t)**2 + (y/t) if t != 0 else 0, 1.0, 1, 2, 0.1, lambda t: t/(1-math.log(t)), "EDO homogenea"),
    (lambda t, y: -2*y + t**3 * math.exp(-2*t), 1.0, 0, 1, 0.1, lambda t: (t**4/4 + 1)*math.exp(-2*t), "Termo forcante"),
    (lambda t, y: 1 + (t - y)**2, 1.0, 2, 3, 0.1, lambda t: t + math.tan(t - 2), "Riccati"),
    (lambda t, y: math.cos(2*t) + math.sin(3*t), 1.0, 0, 2, 0.1, lambda t: 1 + math.sin(2*t)/2 - math.cos(3*t)/3 + 1/3, "Multiplas frequencias"),
    (lambda t, y: -y + 10*math.sin(3*t), 0.0, 0, 5, 0.1, lambda t: 10/10*(math.sin(3*t) - 3*math.cos(3*t)) + 30/10*math.exp(-t), "Resposta frequencia"),
    (lambda t, y: y * (1 - y), 0.5, 0, 5, 0.1, lambda t: 1/(1 + math.exp(-t)), "Logistica"),
    (lambda t, y: -1000*(y - math.exp(-t)), 0.0, 0, 0.01, 0.0001, lambda t: math.exp(-t) - math.exp(-1000*t), "Extremamente Stiff"),
    (lambda t, y: y/t - (y/t)**2 if t != 0 else 0, 1.0, 1, 2, 0.1, lambda t: t/(1 + math.log(t)), "Bernoulli"),
    (lambda t, y: 2*y/t + t**2 * math.exp(t) if t != 0 else 0, 0.0, 1, 2, 0.1, lambda t: t**2 * (math.exp(t) - math.e), "Linear ordem superior"),
    (lambda t, y: -y**3, 1.0, 0, 2, 0.1, lambda t: 1/math.sqrt(1 + 2*t), "Decaimento algebraico"),
    (lambda t, y: math.exp(t - y), 1.0, 0, 1, 0.1, lambda t: math.log(math.exp(t) + math.e - 1), "Nao-linear exponencial"),
    (lambda t, y: (t**2 - y**2) / (t**2 + y**2) if (t**2 + y**2) != 0 else 0, 1.0, 0, 2, 0.1, None, "Estabilidade RK4"),
    (lambda t, y: -y + math.sqrt(t) if t >= 0 else -y, 0.0, 0, 1, 0.1, None, "Derivada infinita em t=0"),
    (lambda t, y: 10*(1 - y), 0.0, 0, 1, 0.1, lambda t: 1 - math.exp(-10*t), "Estado estacionario"),
    (lambda t, y: -y + math.sin(t) + math.cos(t), 0.0, 0, 2*math.pi, 0.1, lambda t: math.sin(t), "y = sin(t)"),
    (lambda t, y: y * math.log(y) if y > 0 else 0, math.e, 0, 1, 0.1, lambda t: math.exp(math.exp(t)), "Crescimento super-exponencial"),
    (lambda t, y: -2*t*y**2, 1.0, 0, 1, 0.1, lambda t: 1/(1 + t**2), "y = 1/(1+t^2)"),
    (lambda t, y: (4*t**3 * y) / (1 + t**4) if (1 + t**4) != 0 else 0, 1.0, 0, 1, 0.1, lambda t: 1 + t**4, "y = 1 + t^4"),
    (lambda t, y: -y + math.exp(-t) * math.cos(t), 0.0, 0, 5, 0.1, None, "Termo forcante complexo"),
    (lambda t, y: y * (2 - y), 0.1, 0, 5, 0.1, lambda t: 2/(1 + 19*math.exp(-2*t)), "Logistica K=2"),
    (lambda t, y: 1 / (2*y - 2) if (2*y - 2) != 0 else 0, 3.0, 0, 1, 0.1, None, "EDO implicita"),
    (lambda t, y: -y + 2*math.exp(t), 1.0, 0, 1, 0.1, lambda t: math.exp(t), "y = e^t"),
    (lambda t, y: (y**2 + y)/t if t != 0 else 0, 1.0, 1, 2, 0.1, lambda t: t/(1 - math.log(t)), "Intervalo t > 0"),
    (lambda t, y: -10*y + 10*t + 1, 0.0, 0, 1, 0.1, lambda t: t, "y = t"),
    (lambda t, y: y * math.cos(t) / (1 + math.sin(t)) if (1 + math.sin(t)) != 0 else 0, 1.0, 0, 2, 0.1, lambda t: 1 + math.sin(t), "y = 1 + sin(t)"),
    (lambda t, y: -y + t**2, 1.0, 0, 1, 0.1, lambda t: t**2 - 2*t + 2 - math.exp(-t), "Polinomial forcante"),
    (lambda t, y: y * (1 - math.log(y)) if y > 0 else 0, 1.0, 0, 2, 0.1, lambda t: math.exp(1 - math.exp(-t)), "Gompertz"),
    (lambda t, y: -y + (1 if t >= 1 else 0), 0.0, 0, 2, 0.1, lambda t: (1 - math.exp(-(t-1))) if t >= 1 else 0, "Funcao degrau"),
    (lambda t, y: -y + (10 if 0.99 <= t <= 1.01 else 0), 0.0, 0, 2, 0.1, None, "Impulso"),
    (lambda t, y: math.sin(y), 1.0, 0, 3, 0.1, None, "Ponto fixo y = pi"),
    (lambda t, y: -y + t**3, 0.0, 0, 1, 0.1, lambda t: t**3 - 3*t**2 + 6*t - 6 + 6*math.exp(-t), "Polinomio cubico"),
    (lambda t, y: 1 / (y - t) if (y - t) != 0 else 0, 2.0, 0, 1, 0.1, None, "Singularidade y = t"),
    (lambda t, y: -100*y + 100*t + 1, 0.0, 0, 1, 0.01, lambda t: t, "Stiff reta"),
    (lambda t, y: y**2 - t, 0.0, 0, 2, 0.1, None, "Airy/Riccati"),
    (lambda t, y: (y**2 - 1) / 2, 0.0, 0, 2, 0.1, lambda t: -math.tanh(t/2), "y = -tanh(t/2)"),
    (lambda t, y: -y + 5*math.exp(-t)*math.sin(5*t), 0.0, 0, 5, 0.1, None, "Oscilacao amortecida"),
    (lambda t, y: y * (1 - y/10), 1.0, 0, 10, 0.1, lambda t: 10/(1 + 9*math.exp(-t)), "Logistica K=10"),
    (lambda t, y: -200*(y - math.sin(t)), 0.0, 0, 1, 0.01, None, "Stiff oscilante"),
]


def relative_error(y_core, y_scipy):
    """Erro relativo entre solucoes"""
    y_c = np.array(y_core, dtype=float)
    y_s = np.array(y_scipy, dtype=float)
    norm_diff = np.linalg.norm(y_c - y_s)
    norm_s = np.linalg.norm(y_s)
    if norm_s == 0:
        return norm_diff
    return norm_diff / norm_s


def compare_euler(f, y0, t0, tf, h, problem_id, desc, y_analitica=None):
    """Compara Euler core vs scipy"""
    core_result = euler_method(f, y0, t0, tf, h)

    n_steps = int((tf - t0) / h) + 1
    t_eval = np.linspace(t0, tf, n_steps)

    try:
        scipy_sol = integrate.solve_ivp(f, [t0, tf], [y0], method='RK45',
                                         t_eval=t_eval, rtol=1e-9, atol=1e-12)
        scipy_success = scipy_sol.success
        scipy_y = scipy_sol.y[0] if scipy_success else None
    except Exception as e:
        scipy_success = False
        scipy_y = None

    core_error_analitico = None
    if core_result["success"] and y_analitica is not None:
        t_vals = core_result["t"]
        y_vals = core_result["y"]
        try:
            y_exact = [y_analitica(t) for t in t_vals]
            core_error_analitico = np.linalg.norm(np.array(y_vals) - np.array(y_exact)) / np.linalg.norm(y_exact)
        except:
            pass

    scipy_error_analitico = None
    if scipy_success and y_analitica is not None:
        try:
            y_exact = [y_analitica(t) for t in t_eval]
            scipy_error_analitico = np.linalg.norm(scipy_y - np.array(y_exact)) / np.linalg.norm(y_exact)
        except:
            pass

    status = "OK"
    diff = None

    if core_result["success"] and scipy_success:
        if core_result["y"] is not None and scipy_y is not None:
            diff = relative_error(core_result["y"], scipy_y)
            if diff > 1e-2:
                status = f"DIFERENCA: {diff:.2e}"
    elif not core_result["success"] and not scipy_success:
        status = "AMBOS FALHARAM"
    elif not core_result["success"]:
        status = f"SO SCIPY: {core_result.get('error', 'erro desconhecido')}"
    else:
        status = f"SO CORE: scipy falhou"

    return {
        "id": problem_id,
        "core_success": core_result["success"],
        "core_y_final": core_result["y"][-1] if core_result["success"] and core_result["y"] is not None else None,
        "core_steps": len(core_result["t"]) if core_result["success"] else 0,
        "scipy_success": scipy_success,
        "scipy_y_final": scipy_y[-1] if scipy_success and scipy_y is not None else None,
        "diff": diff,
        "core_error_analitico": core_error_analitico,
        "scipy_error_analitico": scipy_error_analitico,
        "status": status,
        "error": core_result.get("error") if not core_result["success"] else None
    }


def compare_rk4(f, y0, t0, tf, h, problem_id, desc, y_analitica=None):
    """Compara RK4 core vs scipy"""
    core_result = runge_kutta_4(f, y0, t0, tf, h)

    n_steps = int((tf - t0) / h) + 1
    t_eval = np.linspace(t0, tf, n_steps)

    try:
        scipy_sol = integrate.solve_ivp(f, [t0, tf], [y0], method='RK45',
                                         t_eval=t_eval, rtol=1e-9, atol=1e-12)
        scipy_success = scipy_sol.success
        scipy_y = scipy_sol.y[0] if scipy_success else None
    except Exception as e:
        scipy_success = False
        scipy_y = None

    core_error_analitico = None
    if core_result["success"] and y_analitica is not None:
        t_vals = core_result["t"]
        y_vals = core_result["y"]
        try:
            y_exact = [y_analitica(t) for t in t_vals]
            core_error_analitico = np.linalg.norm(np.array(y_vals) - np.array(y_exact)) / np.linalg.norm(y_exact)
        except:
            pass

    scipy_error_analitico = None
    if scipy_success and y_analitica is not None:
        try:
            y_exact = [y_analitica(t) for t in t_eval]
            scipy_error_analitico = np.linalg.norm(scipy_y - np.array(y_exact)) / np.linalg.norm(y_exact)
        except:
            pass

    status = "OK"
    diff = None

    if core_result["success"] and scipy_success:
        if core_result["y"] is not None and scipy_y is not None:
            diff = relative_error(core_result["y"], scipy_y)
            if diff > 1e-6:
                status = f"DIFERENCA: {diff:.2e}"
    elif not core_result["success"] and not scipy_success:
        status = "AMBOS FALHARAM"
    elif not core_result["success"]:
        status = f"SO SCIPY: {core_result.get('error', 'erro desconhecido')}"
    else:
        status = f"SO CORE: scipy falhou"

    return {
        "id": problem_id,
        "core_success": core_result["success"],
        "core_y_final": core_result["y"][-1] if core_result["success"] and core_result["y"] is not None else None,
        "core_steps": len(core_result["t"]) if core_result["success"] else 0,
        "scipy_success": scipy_success,
        "scipy_y_final": scipy_y[-1] if scipy_success and scipy_y is not None else None,
        "diff": diff,
        "core_error_analitico": core_error_analitico,
        "scipy_error_analitico": scipy_error_analitico,
        "status": status,
        "error": core_result.get("error") if not core_result["success"] else None
    }


def print_table_euler(results):
    print(f"\n{'='*130}")
    print("METODO: EULER")
    print(f"{'='*130}")
    print(f"{'ID':>3} | {'Status':>20} | {'Core Y':>12} | {'Scipy Y':>12} | {'Diff':>10} | {'Err Anal':>10} | Descricao")
    print(f"{'-'*130}")

    for r in results:
        core_y_str = f"{r['core_y_final']:.6f}" if r['core_y_final'] is not None else "N/A"
        scipy_y_str = f"{r['scipy_y_final']:.6f}" if r['scipy_y_final'] is not None else "N/A"
        diff_str = f"{r['diff']:.2e}" if r['diff'] is not None else "N/A"
        err_anal_str = f"{r['core_error_analitico']:.2e}" if r['core_error_analitico'] is not None else "N/A"
        desc = PROBLEMS[r['id']-1][6][:35]
        print(f"{r['id']:>3} | {r['status']:>20} | {core_y_str:>12} | {scipy_y_str:>12} | {diff_str:>10} | {err_anal_str:>10} | {desc}")


def print_table_rk4(results):
    print(f"\n{'='*130}")
    print("METODO: RUNGE-KUTTA 4")
    print(f"{'='*130}")
    print(f"{'ID':>3} | {'Status':>20} | {'Core Y':>12} | {'Scipy Y':>12} | {'Diff':>10} | {'Err Anal':>10} | Descricao")
    print(f"{'-'*130}")

    for r in results:
        core_y_str = f"{r['core_y_final']:.6f}" if r['core_y_final'] is not None else "N/A"
        scipy_y_str = f"{r['scipy_y_final']:.6f}" if r['scipy_y_final'] is not None else "N/A"
        diff_str = f"{r['diff']:.2e}" if r['diff'] is not None else "N/A"
        err_anal_str = f"{r['core_error_analitico']:.2e}" if r['core_error_analitico'] is not None else "N/A"
        desc = PROBLEMS[r['id']-1][6][:35]
        print(f"{r['id']:>3} | {r['status']:>20} | {core_y_str:>12} | {scipy_y_str:>12} | {diff_str:>10} | {err_anal_str:>10} | {desc}")


def main():
    print("="*120)
    print("COMPARACAO: core/ode.py vs scipy.integrate")
    print("50 Problemas de Equacoes Diferenciais Ordinarias")
    print("="*120)

    euler_results = []
    rk4_results = []

    for i, (f, y0, t0, tf, h, y_analitica, desc) in enumerate(PROBLEMS, 1):
        try:
            euler_results.append(compare_euler(f, y0, t0, tf, h, i, desc, y_analitica))
            rk4_results.append(compare_rk4(f, y0, t0, tf, h, i, desc, y_analitica))
        except Exception as e:
            print(f"Problema {i}: erro inesperado - {e}")

    print_table_euler(euler_results)
    print_table_rk4(rk4_results)

    print("\n" + "="*120)
    print("RESUMO ESTATISTICO")
    print("="*120)

    for method_name, results in [("Euler", euler_results), ("RK4", rk4_results)]:
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

    print("\n" + "="*120)
    print("PROBLEMAS COM DIVERGENCIA (>1e-2 diferenca)")
    print("="*120)

    for method_name, results in [("Euler", euler_results), ("RK4", rk4_results)]:
        divergentes = [r for r in results if r['diff'] is not None and r['diff'] > 1e-2]
        if divergentes:
            print(f"\n{method_name}:")
            for r in divergentes:
                print(f"  ID {r['id']}: diff={r['diff']:.2e}")
                print(f"    -> {PROBLEMS[r['id']-1][6]}")

    print("\n" + "="*120)
    print("PROBLEMAS ONDE APENAS UM METODO FUNCIONOU")
    print("="*120)

    for method_name, results in [("Euler", euler_results), ("RK4", rk4_results)]:
        so_core = [r for r in results if r['core_success'] and not r['scipy_success']]
        so_scipy = [r for r in results if not r['core_success'] and r['scipy_success']]

        if so_core or so_scipy:
            print(f"\n{method_name}:")
            for r in so_core:
                print(f"  ID {r['id']}: SO CORE funcionou (y={r['core_y_final']})")
                print(f"    -> {PROBLEMS[r['id']-1][6]}")
            for r in so_scipy:
                print(f"  ID {r['id']}: SO SCIPY funcionou (y={r['scipy_y_final']})")
                print(f"    -> {PROBLEMS[r['id']-1][6]}")
                print(f"    Erro core: {r['error']}")

    print("\n" + "="*120)
    print("COMPARACAO: Euler vs RK4 (mesmos problemas)")
    print("="*120)

    print(f"\n{'ID':>3} | {'Euler Err':>12} | {'RK4 Err':>12} | {'Descricao':>35}")
    print(f"{'-'*70}")

    for i in range(min(len(euler_results), len(rk4_results))):
        e = euler_results[i]
        r = rk4_results[i]
        e_err = e['core_error_analitico']
        r_err = r['core_error_analitico']

        if e_err is not None and r_err is not None:
            print(f"{i+1:>3} | {e_err:>12.2e} | {r_err:>12.2e} | {PROBLEMS[i][6][:35]}")


if __name__ == "__main__":
    main()
