# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Projeto

Solver de métodos numéricos com interface Streamlit + PyWebview para desktop.

## Ambiente

Use o venv local (`venv/`) para desenvolvimento:
```bash
venv\Scripts\python.exe -m streamlit run app.py
```

## Executar Testes

```bash
PYTHONPATH=. venv\Scripts\python.exe tests\test.py -v
```

Para testar apenas um método específico:
```bash
PYTHONPATH=. venv\Scripts\python.exe -m unittest tests.test.TestRootsMethods.test_bisection_simple -v
```

## Estrutura

```
core/               # Implementação dos métodos numéricos
  roots.py          # Bissecção, Newton, Secante (retornam iterations_data)
  linear_systems.py # LU, Gauss, Gauss-Seidel, Gauss-Jacobi
  interpolation.py  # Newton, Lagrange
  integration.py    # Simpson, Trapézio, 3/8
  ode.py            # Euler, Runge-Kutta 4ª ordem
  plot.py           # Funções Plotly para roots, interpolation, integration

validation/         # Validação de inputs (parcialmente implementado)

utils/              # Utilitários compartilhados
  ui.py             # parse_function, parse_function_2d, display_matrix, plot_ode_solution

pages/              # Páginas Streamlit (multipage app, implementado)
  1_raizes.py
  2_sistemas_lineares.py
  3_interpolacao.py
  4_integracao.py
  5_edo.py

tests/
  test.py           # Testes unitários para core, plot e utils
```

## Padrão de Retorno dos Métodos Core

Todos os métodos em `core/` retornam um dicionário com esta estrutura:
```python
{
    "success": bool,           # True se calculou, False se falhou
    "result": float | np.array | None,
    "iterations": int | None,  # Número de iterações se aplicável
    "error": str | None        # Mensagem descritiva se success=False
}
```

Métodos de roots (`bisection`, `newton`, `secant`) também incluem `"iterations_data"` (lista de dicts) para alimentar os gráficos de plot.

Métodos de interpolação (`newton_interpolation`) também incluem `"coefficients"` (np.array).

## Tratamento de Erros

Métodos numéricos devem rodar até possível falha. Quando ocorrer erro numérico (divisão por zero, overflow, derivada zero), capturar a exceção e retornar erro descritivo ao usuário — não impedir execução.

Exemplo em `core/roots.py:46-48`:
```python
if dfx == 0:
    return {"success": False, "root": x0, "iterations": i,
            "error": f"Método falhou: derivada igual a zero no ponto x = {x0}"}
```

## Plotly e Visualizações

O módulo `core/plot.py` contém funções Plotly para gerar gráficos interativos:
- **Roots:** `plot_bisection`, `plot_newton` (tangentes), `plot_secant` (secantes)
- **Interpolation:** `plot_newton_interpolation`, `plot_lagrange_interpolation` — retornam `(fig, info_dict)` com strings dos polinômios, coeficientes, grau e base.
- **Integration:** `plot_simpson`, `plot_trapezoidal`, `plot_three_eight` — preenchem as áreas de integração.

## UI e Parsing de Funções

`utils/ui.py` define `SAFE_GLOBALS` e funções `parse_function(expr_str)` / `parse_function_2d(expr_str)` para converter strings de expressões matemáticas em lambdas seguros. Todas as páginas Streamlit usam essas funções para ler `f(x)` e `f(t, y)` do usuário.

## Fluxo de Dados

```
Usuário → Streamlit Page → parse_function → Core Method → Resultado → UI + Plotly
```

## Próximos Arquivos a Criar

- `core/linear_systems.py` — LU, Gauss, Gauss-Seidel, Gauss-Jacobi (✅ feito)
- `core/interpolation.py` — Newton, Lagrange (✅ feito)
- `core/integration.py` — Simpson, Trapézio, 3/8 (✅ feito)
- `core/ode.py` — Euler, Runge-Kutta 4ª ordem (✅ feito)
- `core/plot.py` — gráficos Plotly (✅ feito)
- `validation/*.py` — validação de inputs (parcialmente feito)
- `pages/*.py` — interface Streamlit (✅ feito)

## Plano de Implementação

### Arquitetura em Camadas

| Camada | Responsabilidade | Arquivos |
|--------|-----------------|----------|
| **UI (Streamlit)** | Interface com usuário, formulários, exibição de resultados | `app.py`, `pages/` |
| **Core (Lógica)** | Implementação dos métodos numéricos | `core/*.py` |
| **Validation** | Validação de inputs antes do cálculo | `validation/*.py` |
| **Tests** | Verificar corretude das implementações | `tests/test.py` |

### Fluxo de Dados

```
Usuário → Streamlit Page → Validation → Core Method → Resultado → UI
```

### Métodos por Arquivo Core

| Arquivo | Métodos |
|---------|---------|
| `core/roots.py` | bisection, newton, secant |
| `core/linear_systems.py` | lu_factorization, gaussian_elimination, gauss_seidel, gauss_jacobi |
| `core/interpolation.py` | newton_interpolation, lagrange_interpolation |
| `core/integration.py` | simpson, trapezoidal_repeated, three_eight_method |
| `core/ode.py` | euler_method, runge_kutta_4 |

### Tratamento de Erros Numéricos

Executar o método e, quando ocorrer erro (divisão por zero, overflow, etc.), capturar e informar ao usuário. Não bloquear execução事先.

| Método | Erro Potencial | Mensagem |
|--------|---------------|----------|
| Newton | Derivada = 0 | "derivada igual a zero no ponto X" |
| Secante | f1-f0 = 0 | "divisão por zero (pontos muito próximos)" |
| Gauss-Seidel/Jacobi | Não converge | "método não converge para este sistema" |

### Passos de Implementação

1. Criar estrutura de diretórios (✅ feito: core/, validation/, pages/, tests/)
2. Implementar `core/` — métodos numéricos
3. Implementar `validation/` — validações de inputs
4. Criar `test.py` e validar cada método do core
5. Desenvolver interface Streamlit (`app.py` + `pages/`)
6. Configurar PyWebview para desktop
7. Documentar no README

## Versionamento no GitHub

Toda alteração no código deve ser salva no repositório remoto no GitHub.

**URL do repositório:** https://github.com/pedrocaiopc1234-ds/solver-metodos-numericos

### Fluxo de commit obrigatório

1. Após editar qualquer arquivo, verificar as mudanças:
   ```bash
   git status
   git diff
   ```

2. Adicionar os arquivos modificados:
   ```bash
   git add <arquivo>
   # ou, se quiser adicionar tudo:
   git add -A
   ```

3. Criar um commit descritivo:
   ```bash
   git commit -m "descrição clara da mudança"
   ```

4. Enviar para o GitHub:
   ```bash
   git push origin master
   ```

**Regra:** nunca deixar alterações locais não commitadas. Sempre que o usuário pedir uma mudança no código, após concluir a edição, executar os comandos acima para persistir no repositório remoto.