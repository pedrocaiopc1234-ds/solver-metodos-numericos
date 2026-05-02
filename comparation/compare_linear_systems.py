"""
Comparação: Implementações core/linear_systems.py vs scipy.linalg
50 exemplos de Sistemas Lineares
"""

import numpy as np
from core.linear_systems import lu_factorization, gaussian_elimination, gauss_seidel, gauss_jacobi
from scipy import linalg

# 50 Problemas de Sistemas Lineares
PROBLEMS = [
    # (A, b, descricao)
    ([[1, 1/2, 1/3, 1/4, 1/5],
      [1/2, 1/3, 1/4, 1/5, 1/6],
      [1/3, 1/4, 1/5, 1/6, 1/7],
      [1/4, 1/5, 1/6, 1/7, 1/8],
      [1/5, 1/6, 1/7, 1/8, 1/9]], [1, 1, 1, 1, 1], "Hilbert n=5 - mal condicionada"),

    ([[0, 1], [1, 1]], [1, 2], "a11=0 - LU sem pivotação falha"),
    ([[1, 2], [2, 1]], [3, 3], "Não diagonalmente dominante"),
    ([[1, 1], [1, 1.0001]], [2, 2.0001], "Quase singular - sensível a arredondamento"),
    ([[1/(i+j+1) for j in range(10)] for i in range(10)], [1]*10, "Hilbert n=10 - erro explode"),
    ([[10, 1, 1], [1, 10, 1], [1, 1, 10]], [12, 12, 12], "Diagonal dominante - convergência rápida"),
    ([[1, 2, 3], [2, 4, 6], [3, 6, 9]], [1, 2, 3], "Singular - determinante 0"),
    ([[0.1, 0.2], [0.3, 0.4]], [0.3, 0.7], "Pequenos valores na diagonal"),
    ([[1, 10], [10, 1]], [11, 11], "Jacobi diverge - raio espectral > 1"),
    ([[2, -1, 0], [-1, 2, -1], [0, -1, 2]], [1, 0, 1], "Matriz de Poisson 1D - definida positiva"),
    ([[1, 0.5, 0.33], [0.5, 0.33, 0.25], [0.33, 0.25, 0.2]], [1.83, 1.08, 0.78], "Aproximação Hilbert"),
    ([[1, 2], [3, 4]], [5, 11], "Simples - testa pivotação parcial"),
    ([[1e-10, 1], [1, 1]], [1, 2], "Pivotação essencial - erro catastrófico"),
    ([[4, 1, 1], [1, 4, 1], [1, 1, 4]], [6, 6, 6], "Estritamente diagonal dominante"),
    ([[1, 2, 0], [2, 1, 2], [0, 2, 1]], [3, 5, 3], "Jacobi diverge"),
    ([[4, 1, 0], [1, 4, 1], [0, 1, 4]], [5, 6, 5], "Tridiagonal - algoritmo de Thomas"),
    ([[1, 1], [1, 1]], [2, 2], "Sistema indeterminado"),
    ([[1, 2, 3], [0, 1, 4], [5, 6, 0]], [14, 13, 19], "LU com PA"),
    ([[1, 1, 1], [1, 2, 3], [1, 3, 6]], [3, 6, 10], "Matriz de Pascal"),
    ([[2, 1], [1, 2]], [3, 3], "Convergência garantida"),
    ([[1, 10, 100], [0, 1, 10], [0, 0, 1]], [111, 11, 1], "Triangular superior"),
    ([[1, 0, 0], [10, 1, 0], [100, 10, 1]], [101, 11, 1], "Triangular inferior"),
    ([[0, 0, 1], [0, 1, 0], [1, 0, 0]], [1, 2, 3], "Matriz de permutação"),
    ([[1, 2, 3], [4, 5, 6], [7, 8, 10]], [14, 32, 51], "Determinante pequeno"),
    ([[1, 2], [2, 4.00001]], [3, 6.00002], "Quase dependentes"),
    ([[5, -2, 1], [-2, 5, -2], [1, -2, 5]], [4, 1, 4], "Simétrica diagonal dominante"),
    ([[1, 2], [3, 4]], [5, 11], "Não diagonal dominante - GS converge"),
    ([[1, 1], [-1, 1]], [2, 0], "Matriz de rotação"),
    ([[10, 2, 1], [1, 5, 1], [2, 3, 10]], [13, 7, 15], "Diagonal dominante por colunas"),
    ([[1, 2, 3, 4], [2, 3, 4, 1], [3, 4, 1, 2], [4, 1, 2, 3]], [10, 10, 10, 10], "Matriz circulante"),
    ([[1, 0.9], [0.9, 1]], [1.9, 1.9], "Autovalores próximos - Jacobi lento"),
    ([[1, 2], [1.0001, 2]], [3, 3.0001], "Mal condicionada"),
    ([[0, 1, 2], [1, 0, 3], [4, 5, 0]], [8, 10, 14], "Zeros na diagonal"),
    ([[4, -1, 0, -1, 0, 0],
      [-1, 4, -1, 0, -1, 0],
      [0, -1, 4, 0, 0, -1],
      [-1, 0, 0, 4, -1, 0],
      [0, -1, 0, -1, 4, -1],
      [0, 0, -1, 0, -1, 4]], [4, 4, 4, 4, 4, 4], "Laplace 2D"),
    ([[1, 2, 3], [4, 5, 6], [7, 8, 9]], [1, 2, 3], "Singular - posto 2"),
    ([[1, 1e15], [1, 1]], [1e15+1, 2], "Escalas muito diferentes"),
    ([[2, -1], [-1, 2]], [1, 1], "Matriz de rigidez"),
    ([[1, 2, 3], [2, 3, 4], [3, 4, 5]], [1, 2, 3], "Singular - PA"),
    ([[10, 1], [1, 10]], [11, 11], "Raio espectral pequeno"),
    ([[1, 2, 3], [1, 2, 3.0001], [1, 2.0001, 3]], [6, 6.0001, 6.0001], "Quase singular multidimensional"),
    ([[1, 0, 1], [0, 1, 0], [1, 0, 1]], [2, 1, 2], "Singular simétrica"),
    ([[5, 1, 2], [1, 4, -1], [2, -1, 3]], [8, 4, 4], "Diagonal dominante"),
    ([[1, 2], [3, 4]], [5, 11], "Solução exata x=[1,2]"),
    ([[1, 1, 1], [0, 1, 1], [0, 0, 1]], [3, 2, 1], "Identidade + triangular"),
    ([[2, 4, 8], [4, 8, 16], [8, 16, 32]], [2, 4, 8], "Singular - múltiplas"),
    ([[1, 0.1, 0.1], [0.1, 1, 0.1], [0.1, 0.1, 1]], [1.2, 1.2, 1.2], "Quase identidade"),
    ([[0.5, 0.5], [0.5, 0.5]], [1, 1], "Singular - det=0"),
    ([[1, 2, 3], [3, 2, 1], [1, 3, 2]], [14, 10, 11], "Pivotação completo"),
    ([[100, 1], [1, 100]], [101, 101], "Jacobi vs GS"),
    ([[1, 2, 3], [4, 5, 6], [7, 8, 10]], [14, 32, 51], "Validação resíduo"),
]


def safe_float(val):
    """Converte para float seguro"""
    if val is None:
        return None
    if isinstance(val, (list, np.ndarray)):
        return [float(v) if not (np.isnan(v) or np.isinf(v)) else None for v in val]
    try:
        if np.isnan(val) or np.isinf(val):
            return None
        return float(val)
    except:
        return None


def matrix_norm(A):
    """Norma de Frobenius"""
    return np.linalg.norm(np.array(A, dtype=float))


def relative_error(x_core, x_scipy):
    """Erro relativo entre soluções"""
    x_c = np.array(x_core, dtype=float)
    x_s = np.array(x_scipy, dtype=float)
    norm_diff = np.linalg.norm(x_c - x_s)
    norm_s = np.linalg.norm(x_s)
    if norm_s == 0:
        return norm_diff
    return norm_diff / norm_s


def compare_lu(A, b, problem_id, desc):
    """Compara LU factorization core vs scipy"""
    A_np = np.array(A, dtype=float)
    b_np = np.array(b, dtype=float)

    # Nossa implementação
    core_result = lu_factorization(A, b)

    # scipy.linalg.solve (usa LU internamente com pivotação)
    try:
        scipy_x = linalg.solve(A_np, b_np)
        scipy_success = True
    except linalg.LinAlgError as e:
        scipy_x = None
        scipy_success = False

    # Verificar resíduo
    core_residual = None
    if core_result["success"] and core_result["x"] is not None:
        x_c = np.array(core_result["x"])
        residual = np.linalg.norm(A_np @ x_c - b_np)
        core_residual = residual

    scipy_residual = None
    if scipy_success:
        scipy_residual = np.linalg.norm(A_np @ scipy_x - b_np)

    # Comparação
    status = "OK"
    diff = None

    if core_result["success"] and scipy_success:
        if core_result["x"] is not None and scipy_x is not None:
            diff = relative_error(core_result["x"], scipy_x)
            if diff > 1e-6:
                status = f"DIFERENÇA: {diff:.2e}"
            elif core_residual and core_residual > 1e-6:
                status = f"RESÍDUO ALTO: {core_residual:.2e}"
    elif not core_result["success"] and not scipy_success:
        status = "AMBOS FALHARAM"
    elif not core_result["success"]:
        status = f"SÓ SCIPY: {core_result.get('error', 'erro desconhecido')}"
    else:
        status = f"SÓ CORE: scipy falhou"

    return {
        "id": problem_id,
        "core_success": core_result["success"],
        "core_x": core_result.get("x"),
        "core_residual": core_residual,
        "scipy_success": scipy_success,
        "scipy_x": scipy_x,
        "scipy_residual": scipy_residual,
        "diff": diff,
        "status": status,
        "error": core_result.get("error") if not core_result["success"] else None
    }


def compare_gauss_seidel(A, b, problem_id, desc):
    """Compara Gauss-Seidel core vs scipy"""
    A_np = np.array(A, dtype=float)
    b_np = np.array(b, dtype=float)

    # Nossa implementação
    core_result = gauss_seidel(A, b, tol=1e-10, max_iter=1000)

    # scipy.linalg.solve (solução exata)
    try:
        scipy_x = linalg.solve(A_np, b_np)
        scipy_success = True
    except linalg.LinAlgError as e:
        scipy_x = None
        scipy_success = False

    # Verificar resíduo
    core_residual = None
    if core_result["success"] and core_result["x"] is not None:
        x_c = np.array(core_result["x"])
        residual = np.linalg.norm(A_np @ x_c - b_np)
        core_residual = residual

    scipy_residual = None
    if scipy_success:
        scipy_residual = np.linalg.norm(A_np @ scipy_x - b_np)

    status = "OK"
    diff = None

    if core_result["success"] and scipy_success:
        if core_result["x"] is not None and scipy_x is not None:
            diff = relative_error(core_result["x"], scipy_x)
            if diff > 1e-6:
                status = f"DIFERENÇA: {diff:.2e}"
            elif core_residual and core_residual > 1e-6:
                status = f"RESÍDUO ALTO: {core_residual:.2e}"
    elif not core_result["success"] and not scipy_success:
        status = "AMBOS FALHARAM"
    elif not core_result["success"]:
        status = f"SÓ SCIPY: {core_result.get('error', 'erro desconhecido')}"
    else:
        status = f"SÓ CORE: scipy falhou"

    return {
        "id": problem_id,
        "core_success": core_result["success"],
        "core_x": core_result.get("x"),
        "core_iters": core_result.get("iterations", 0),
        "core_residual": core_residual,
        "scipy_success": scipy_success,
        "scipy_x": scipy_x,
        "scipy_residual": scipy_residual,
        "diff": diff,
        "status": status,
        "error": core_result.get("error") if not core_result["success"] else None,
        "warning": core_result.get("warning")
    }


def compare_gauss_jacobi(A, b, problem_id, desc):
    """Compara Gauss-Jacobi core vs scipy"""
    A_np = np.array(A, dtype=float)
    b_np = np.array(b, dtype=float)

    # Nossa implementação
    core_result = gauss_jacobi(A, b, tol=1e-10, max_iter=1000)

    # scipy.linalg.solve (solução exata)
    try:
        scipy_x = linalg.solve(A_np, b_np)
        scipy_success = True
    except linalg.LinAlgError as e:
        scipy_x = None
        scipy_success = False

    # Verificar resíduo
    core_residual = None
    if core_result["success"] and core_result["x"] is not None:
        x_c = np.array(core_result["x"])
        residual = np.linalg.norm(A_np @ x_c - b_np)
        core_residual = residual

    scipy_residual = None
    if scipy_success:
        scipy_residual = np.linalg.norm(A_np @ scipy_x - b_np)

    status = "OK"
    diff = None

    if core_result["success"] and scipy_success:
        if core_result["x"] is not None and scipy_x is not None:
            diff = relative_error(core_result["x"], scipy_x)
            if diff > 1e-6:
                status = f"DIFERENÇA: {diff:.2e}"
            elif core_residual and core_residual > 1e-6:
                status = f"RESÍDUO ALTO: {core_residual:.2e}"
    elif not core_result["success"] and not scipy_success:
        status = "AMBOS FALHARAM"
    elif not core_result["success"]:
        status = f"SÓ SCIPY: {core_result.get('error', 'erro desconhecido')}"
    else:
        status = f"SÓ CORE: scipy falhou"

    return {
        "id": problem_id,
        "core_success": core_result["success"],
        "core_x": core_result.get("x"),
        "core_iters": core_result.get("iterations", 0),
        "core_residual": core_residual,
        "scipy_success": scipy_success,
        "scipy_x": scipy_x,
        "scipy_residual": scipy_residual,
        "diff": diff,
        "status": status,
        "error": core_result.get("error") if not core_result["success"] else None,
        "warning": core_result.get("warning")
    }


def print_table_lu(results):
    """Imprime tabela de resultados para LU"""
    print(f"\n{'='*120}")
    print("MÉTODO: LU FACTORIZATION")
    print(f"{'='*120}")
    print(f"{'ID':>3} | {'Status':>30} | {'Core Res':>12} | {'Scipy Res':>12} | {'Diff':>10} | Descrição")
    print(f"{'-'*120}")

    for r in results:
        core_res_str = f"{r['core_residual']:.2e}" if r['core_residual'] is not None else "N/A"
        scipy_res_str = f"{r['scipy_residual']:.2e}" if r['scipy_residual'] is not None else "N/A"
        diff_str = f"{r['diff']:.2e}" if r['diff'] is not None else "N/A"

        desc = PROBLEMS[r['id']-1][2][:50]

        print(f"{r['id']:>3} | {r['status']:>30} | {core_res_str:>12} | {scipy_res_str:>12} | {diff_str:>10} | {desc}")


def print_table_iterative(results, method_name):
    """Imprime tabela de resultados para métodos iterativos"""
    print(f"\n{'='*130}")
    print(f"MÉTODO: {method_name}")
    print(f"{'='*130}")
    print(f"{'ID':>3} | {'Status':>25} | {'Core Res':>12} | {'Scipy Res':>12} | {'Diff':>10} | {'Iters':>7} | Descrição")
    print(f"{'-'*130}")

    for r in results:
        core_res_str = f"{r['core_residual']:.2e}" if r['core_residual'] is not None else "N/A"
        scipy_res_str = f"{r['scipy_residual']:.2e}" if r['scipy_residual'] is not None else "N/A"
        diff_str = f"{r['diff']:.2e}" if r['diff'] is not None else "N/A"

        desc = PROBLEMS[r['id']-1][2][:50]

        print(f"{r['id']:>3} | {r['status']:>25} | {core_res_str:>12} | {scipy_res_str:>12} | {diff_str:>10} | {r['core_iters']:>7} | {desc}")


def main():
    print("="*120)
    print("COMPARAÇÃO: core/linear_systems.py vs scipy.linalg")
    print("50 Problemas de Sistemas Lineares")
    print("="*120)

    lu_results = []
    seidel_results = []
    jacobi_results = []

    for i, (A, b, desc) in enumerate(PROBLEMS, 1):
        try:
            lu_results.append(compare_lu(A, b, i, desc))
            seidel_results.append(compare_gauss_seidel(A, b, i, desc))
            jacobi_results.append(compare_gauss_jacobi(A, b, i, desc))
        except Exception as e:
            print(f"Problema {i}: erro inesperado - {e}")

    # Imprimir resultados
    print_table_lu(lu_results)
    print_table_iterative(seidel_results, "GAUSS-SEIDEL")
    print_table_iterative(jacobi_results, "GAUSS-JACOBI")

    # Resumo estatístico
    print("\n" + "="*120)
    print("RESUMO ESTATÍSTICO")
    print("="*120)

    for method_name, results in [("LU", lu_results), ("Gauss-Seidel", seidel_results), ("Gauss-Jacobi", jacobi_results)]:
        total = len(results)
        both_success = sum(1 for r in results if r['core_success'] and r['scipy_success'])
        both_fail = sum(1 for r in results if not r['core_success'] and not r['scipy_success'])
        only_core = sum(1 for r in results if r['core_success'] and not r['scipy_success'])
        only_scipy = sum(1 for r in results if not r['core_success'] and r['scipy_success'])

        diffs = [r['diff'] for r in results if r['diff'] is not None and r['diff'] < 1e10]
        max_diff = max(diffs) if diffs else 0
        avg_diff = sum(diffs)/len(diffs) if diffs else 0

        # Contar resíduos altos
        high_residual = sum(1 for r in results if r['core_residual'] is not None and r['core_residual'] > 1e-6)

        print(f"\n{method_name}:")
        print(f"  Total testes: {total}")
        print(f"  Ambos sucesso: {both_success} ({100*both_success/total:.1f}%)")
        print(f"  Ambos falharam: {both_fail} ({100*both_fail/total:.1f}%)")
        print(f"  Só core funcionou: {only_core}")
        print(f"  Só scipy funcionou: {only_scipy}")
        print(f"  Maior diferença: {max_diff:.2e}")
        print(f"  Média diferenças: {avg_diff:.2e}")
        print(f"  Resíduos altos (>1e-6): {high_residual}")

    # Listar problemas com divergência
    print("\n" + "="*120)
    print("PROBLEMAS COM DIVERGÊNCIA (>1e-6 diferença)")
    print("="*120)

    for method_name, results in [("LU", lu_results), ("Gauss-Seidel", seidel_results), ("Gauss-Jacobi", jacobi_results)]:
        divergentes = [r for r in results if r['diff'] is not None and r['diff'] > 1e-6]
        if divergentes:
            print(f"\n{method_name}:")
            for r in divergentes:
                print(f"  ID {r['id']}: core_diff={r['diff']:.2e}, core_res={r['core_residual']:.2e}")
                print(f"    -> {PROBLEMS[r['id']-1][2]}")

    # Listar falhas
    print("\n" + "="*120)
    print("PROBLEMAS ONDE APENAS UM MÉTODO FUNCIONOU")
    print("="*120)

    for method_name, results in [("LU", lu_results), ("Gauss-Seidel", seidel_results), ("Gauss-Jacobi", jacobi_results)]:
        so_core = [r for r in results if r['core_success'] and not r['scipy_success']]
        so_scipy = [r for r in results if not r['core_success'] and r['scipy_success']]

        if so_core or so_scipy:
            print(f"\n{method_name}:")
            for r in so_core:
                print(f"  ID {r['id']}: SÓ CORE funcionou")
                print(f"    -> {PROBLEMS[r['id']-1][2]}")
            for r in so_scipy:
                print(f"  ID {r['id']}: SÓ SCIPY funcionou")
                print(f"    -> {PROBLEMS[r['id']-1][2]}")
                print(f"    Erro core: {r['error']}")

    # Listar problemas com aviso de não dominância diagonal
    print("\n" + "="*120)
    print("PROBLEMAS COM AVISO DE NÃO DOMINÂNCIA DIAGONAL")
    print("="*120)

    for method_name, results in [("Gauss-Seidel", seidel_results), ("Gauss-Jacobi", jacobi_results)]:
        com_aviso = [r for r in results if r.get('warning') is not None]
        if com_aviso:
            print(f"\n{method_name}:")
            for r in com_aviso:
                print(f"  ID {r['id']}: {r['warning'][:80]}")
                print(f"    -> {PROBLEMS[r['id']-1][2]}")


if __name__ == "__main__":
    main()
