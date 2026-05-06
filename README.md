# NumerPy Solver — Métodos Numéricos

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![NumPy](https://img.shields.io/badge/NumPy-1.24+-green.svg)](https://numpy.org)
[![Plotly](https://img.shields.io/badge/Plotly-5.14+-orange.svg)](https://plotly.com)
[![Dash](https://img.shields.io/badge/Dash-2.9+-lightblue.svg)](https://dash.plotly.com)
[![Testes](https://img.shields.io/badge/testes-305%20%2B%20250%20benchmarks-brightgreen.svg)]()
[![Release](https://img.shields.io/github/v/release/pedrocaiopc1234-ds/solver-metodos-numericos?label=Release)](https://github.com/pedrocaiopc1234-ds/solver-metodos-numericos/releases)
[![Downloads](https://img.shields.io/github/downloads/pedrocaiopc1234-ds/solver-metodos-numericos/total?label=Downloads)](https://github.com/pedrocaiopc1234-ds/solver-metodos-numericos/releases)

</div>

---

## Baixar e Usar

A forma mais simples de usar o NumerPy Solver é baixar o executável pronto:

1. Acesse [Releases](https://github.com/pedrocaiopc1234-ds/solver-metodos-numericos/releases)
2. Baixe `NumerPy-Solver-vX.X.X-windows.zip`
3. Extraia e execute `NumerPy Solver.exe`

Funciona como qualquer aplicativo nativo — sem instalar Python ou dependências. Veja instruções detalhadas em [DISTRIBUICAO.md](DISTRIBUICAO.md).

---

## O que é

O NumerPy Solver é um calculador de métodos numéricos com interface web/desktop que implementa **12 algoritmos** em **5 categorias**:

| Categoria | Métodos |
|-----------|---------|
| Zeros de funções | Bisseção, Newton-Raphson, Secante |
| Sistemas lineares | Fatoração LU, Eliminação de Gauss, Gauss-Seidel, Gauss-Jacobi |
| Interpolação | Newton (diferenças divididas), Lagrange |
| Integração numérica | Simpson 1/3, Trapézios, Simpson 3/8 |
| EDOs | Euler, Runge-Kutta 4 |

Cada método retorna o resultado **e** os dados de cada iteração, permitindo visualizar o caminho até a convergência.

---

## Estrutura do Projeto

```
solver-metodos-numericos/
│
├── app.py                        # Aplicação Dash (modo navegador, porta 8050)
├── main.py                       # Aplicação Desktop (pywebview)
├── build.py                      # Build PyInstaller (--onefile --windowed)
├── release.py                    # Cria ZIP de release para GitHub
├── create_icon.py                # Gera ícone do app
├── create_shortcut.py            # Cria atalho na área de trabalho (Windows)
├── requirements.txt              # Dependências Python
│
├── core/                         # Núcleo computacional (sem UI)
│   ├── __init__.py               # Re-exporta todas as funções públicas
│   ├── roots.py                  # bisection, newton, secant
│   ├── linear_systems.py         # lu_factorization, gaussian_elimination, gauss_seidel, gauss_jacobi
│   ├── interpolation.py          # newton_interpolation, lagrange_interpolation
│   ├── integration.py            # simpson, trapezoidal_repeated, three_eight_method
│   ├── ode.py                    # euler_method, runge_kutta_4
│   └── plot.py                   # Geradores de figuras Plotly (8 funções)
│
├── validation/                   # Validação de entrada (sanitização)
│   ├── roots_validation.py       # f(x), intervalo, tolerância, iterações
│   ├── linear_systems_validation.py  # matriz, vetor, dimensões
│   ├── interpolation_validation.py    # pontos, avaliação
│   ├── integration_validation.py      # intervalo, n de subintervalos
│   └── ode_validation.py             # f(t,y), condição inicial, passo
│
├── utils/                        # Parsing e helpers de UI
│   ├── dash_ui.py                # parse_function, parse_function_2d, SAFE_GLOBALS (ativo)
│   └── ui.py                     # Versão Streamlit (legado)
│
├── pages/                        # Interface Dash (multi-page)
│   ├── home.py                   # Página inicial com cards
│   ├── 1_raizes.py               # Zeros de funções
│   ├── 2_sistemas_lineares.py    # Sistemas lineares
│   ├── 3_interpolacao.py         # Interpolação
│   ├── 4_integracao.py          # Integração numérica
│   └── 5_edo.py                  # EDOs
│
├── tests/                        # Testes unitários (305 testes)
│   ├── test_roots.py             # 65 testes (básicos + robustez + scipy)
│   ├── test_linear_systems.py    # 84 testes
│   ├── test_interpolation.py     # 42 testes
│   ├── test_integration.py       # 63 testes
│   ├── test_ode.py               # 42 testes
│   └── test_plots.py             # 9 testes (smoke tests de plotagem)
│
├── comparation/                  # Benchmarks contra SciPy (250 problemas)
│   ├── compare_roots.py          # 50 problemas (bisseção, Newton, secante vs scipy.optimize)
│   ├── compare_linear_systems.py # 50 problemas (LU, Seidel, Jacobi vs scipy.linalg.solve)
│   ├── compare_ode.py            # 50 problemas (Euler, RK4 vs scipy.integrate.solve_ivp)
│   ├── compare_interpolation.py  # 50 problemas (Newton, Lagrange vs scipy.interpolate.lagrange)
│   └── compare_integration.py    # 50 problemas (Trapézios, Simpson 1/3, 3/8 vs scipy.integrate)
│
├── assets/                       # Recursos estáticos
│   ├── style.css                 # CSS responsivo (dark theme, mobile)
│   ├── icon.ico                  # Ícone do aplicativo
│   ├── manifest.json             # PWA manifest
│   └── sw.js                     # Service Worker (offline)
│
├── docs.md                       # Documentação técnica completa
├── CLAUDE.md                      # Guia interno do projeto
├── DISTRIBUICAO.md                # Guia de distribuição
├── INSTALACAO.md                  # Guia de instalação
└── .github/workflows/build-release.yml  # CI/CD (build automático)
```

---

## Como Usar

### Modo Desktop (recomendado)

```bash
# Após clonar o repositório e instalar dependências
pip install -r requirements.txt

# Inicia o app em janela nativa (pywebview)
python main.py
```

O app abre uma janela nativa de 1400x900 com a interface completa. Se pywebview não estiver disponível, abre no navegador automaticamente.

### Modo Navegador

```bash
# Inicia o servidor Dash em http://127.0.0.1:8050
python app.py
```

Acesse `http://127.0.0.1:8050` no navegador.

### Uso Programático (importando os módulos)

Cada função do `core/` pode ser importada e usada diretamente, sem a interface:

```python
from core.roots import bisection, newton, secant
from core.linear_systems import lu_factorization, gauss_seidel
from core.interpolation import newton_interpolation, lagrange_interpolation
from core.integration import simpson, trapezoidal_repeated, three_eight_method
from core.ode import euler_method, runge_kutta_4
```

**Zeros de funções:**

```python
from core.roots import bisection, newton, secant

f = lambda x: x**2 - 4
df = lambda x: 2*x

# Bisseção
r = bisection(f, a=0, b=3, tol=1e-6)
print(r["root"])  # 2.0

# Newton (requer derivada)
r = newton(f, df, x0=3, tol=1e-6)
print(r["root"])  # 2.0

# Secante (não requer derivada)
r = secant(f, x0=1, x1=3, tol=1e-6)
print(r["root"])  # 2.0
```

**Sistemas lineares:**

```python
from core.linear_systems import lu_factorization, gauss_seidel

A = [[4, 1], [1, 3]]
b = [5, 4]

# Fatoração LU (retorna x, L, U)
r = lu_factorization(A, b)
print(r["x"])  # [1.0, 1.0]

# Gauss-Seidel iterativo (retorna x, iterações, warning se não diagonal dominante)
r = gauss_seidel(A, b, tol=1e-10)
print(r["x"])  # [1.0, 1.0]
```

**Interpolação:**

```python
from core.interpolation import newton_interpolation, lagrange_interpolation

x = [1, 2, 3]
y = [1, 4, 9]

r = newton_interpolation(x, y, 2.5)
print(r["result"])  # 6.25
print(r["coefficients"])  # [1.0, 3.0, 1.0]
```

**Integração numérica:**

```python
from core.integration import simpson, trapezoidal_repeated, three_eight_method
import math

f = lambda x: math.sin(x)

r = simpson(f, 0, math.pi, n=100)
print(r["result"])  # 2.0

r = trapezoidal_repeated(f, 0, math.pi, n=100)
print(r["result"])  # ~1.9998

r = three_eight_method(f, 0, math.pi, n=99)
print(r["result"])  # ~2.0
```

**EDOs:**

```python
from core.ode import euler_method, runge_kutta_4

f = lambda t, y: y  # dy/dt = y

r = euler_method(f, y0=1.0, t0=0, tf=1, h=0.01)
print(r["y"][-1])  # ~2.7048 (exato: e = 2.7183)

r = runge_kutta_4(f, y0=1.0, t0=0, tf=1, h=0.01)
print(r["y"][-1])  # ~2.7183 (quase exato)
```

### Formato de Retorno

Todas as funções retornam um dicionário padronizado:

```python
{
    "success": bool,          # True se convergiu
    "result": float/array,    # Resultado (nome varia por método)
    "iterations": int,       # Número de iterações (métodos iterativos)
    "iterations_data": list,  # Dados de cada iteração (para visualização)
    "error": str | None       # Mensagem de erro se success=False
}
```

Métodos iterativos (Gauss-Seidel, Gauss-Jacobi) incluem `"warning"` quando a matriz não é diagonalmente dominante. LU inclui `"L"` e `"U"`.

---

## Validação e Comparação com SciPy

O diretório `comparation/` contém 250 problemas de teste (50 por categoria) que comparam cada método do NumerPy Solver contra funções equivalentes do SciPy:

| Script | Métodos testados | Referência SciPy |
|--------|-----------------|-------------------|
| `compare_roots.py` | Bisseção, Newton, Secante | `scipy.optimize.bisect`, `scipy.optimize.newton` |
| `compare_linear_systems.py` | LU, Gauss-Seidel, Gauss-Jacobi | `scipy.linalg.solve` |
| `compare_ode.py` | Euler, RK4 | `scipy.integrate.solve_ivp(RK45)` |
| `compare_interpolation.py` | Newton, Lagrange | `scipy.interpolate.lagrange` |
| `compare_integration.py` | Trapézios, Simpson 1/3, Simpson 3/8 | `scipy.integrate.trapezoid`, `scipy.integrate.simpson` |

Para executar os benchmarks:

```bash
python comparation/compare_roots.py
python comparation/compare_linear_systems.py
python comparation/compare_ode.py
python comparation/compare_interpolation.py
python comparation/compare_integration.py
```

Cada script imprime uma tabela com status (OK/DIFERENÇA/FALHA), valores obtidos, diferença absoluta, e sumário estatístico. Veja [docs.md](docs.md) para análise detalhada dos resultados.

---

## Executando os Testes

```bash
# Todos os testes
python -m pytest tests/ -v

# Ou com unittest
python -m unittest discover -s tests -v

# Um módulo específico
python -m unittest tests.test_roots.TestBisectionRobustness -v
```

---

## Build e Release

```bash
# Criar executável standalone
python build.py

# Criar release (build + ZIP)
python release.py --version X.Y.Z

# Criar atalho na área de trabalho (Windows)
python create_shortcut.py
```

O executável é gerado com `--onefile --windowed` via PyInstaller, empacotando pywebview, pythonnet e clr_loader. Funciona em qualquer local do sistema de arquivos.

---

## Arquitetura

O fluxo de processamento segue 5 camadas com responsabilidade única:

```
[Usuário] → pages/ → validation/ → core/ → resultado dict
               ↓                        ↓
         utils/dash_ui.py          core/plot.py
         (parse_function)          (visualização)
               ↓                        ↓
            callback              Figura Plotly
               ↓
         Interface Dash renderizada
```

1. **`pages/`** — Interface Dash com callbacks. Recebe entrada do usuário, chama validação, chama core, renderiza resultado.
2. **`validation/`** — Sanitiza entradas (limites de tolerância, dimensões, NaN/Inf). Retorna `{"valid": bool, "error": str}`.
3. **`utils/dash_ui.py`** — Converte strings matemáticas em callables via `eval()` com whitelist `SAFE_GLOBALS`.
4. **`core/`** — Computação pura. Sem dependência de UI. Toda função retorna dict padronizado com `success`, resultado, `iterations_data`, `error`.
5. **`core/plot.py`** — Gera figuras Plotly com regiões de convergência, tangentes, áreas de integração.

---

## Funcionalidades por Método

### Zeros de Funções

| Método | Entrada | Critério de parada | Convergência |
|--------|---------|-------------------|--------------|
| Bisseção | f(x), [a, b] | \|f(c)\| < tol | Linear (1/2) |
| Newton | f(x), f'(x), x₀ | \|x_{n+1} - x_n\| < tol | Quadrática |
| Secante | f(x), x₀, x₁ | \|x_{n+1} - x_n\| < tol | Superlinear (φ ≈ 1.618) |

### Sistemas Lineares

| Método | Tipo | Retorna | Condição |
|--------|------|---------|----------|
| LU | Direto | x, L, U | Pivoteamento parcial |
| Gauss | Direto | x | Pivoteamento parcial |
| Gauss-Seidel | Iterativo | x, iterações, warning | Diagonal dominante |
| Gauss-Jacobi | Iterativo | x, iterações, warning | Diagonal dominante |

### Interpolação

| Método | Avaliação | Complexidade | Saída |
|--------|-----------|---------------|-------|
| Newton | Horner O(n) | Tabela O(n²) | Resultado + coeficientes |
| Lagrange | Direta O(n²) | — | Resultado |

### Integração

| Método | Ordem do erro | Requisito | Exatidão |
|--------|--------------|-----------|----------|
| Trapézios | O(h²) | n ≥ 1 | Polinômios grau ≤ 1 |
| Simpson 1/3 | O(h⁴) | n par | Polinômios grau ≤ 3 |
| Simpson 3/8 | O(h⁴) | n múltiplo de 3 | Polinômios grau ≤ 3 |

### EDOs

| Método | Ordem global | Avaliações/passo | Estabilidade |
|--------|-------------|------------------|--------------|
| Euler | O(h) | 1 | Condicional |
| RK4 | O(h⁴) | 4 | Amplamente estável |

---

## Documentação Completa

Para documentação técnica aprofundada (fundamentos matemáticos, algoritmos, análise comparativa com SciPy, complexidade computacional, validação), veja [docs.md](docs.md).

---

## Autor

**Pedro Caio** — Bacharelado em Matemática, Instituto de Matemática e Estatística — UFG

## Licença

MIT License — veja [LICENSE](LICENSE) para detalhes.