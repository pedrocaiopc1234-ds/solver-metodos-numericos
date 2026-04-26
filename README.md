# Solver de Métodos Numéricos

Aplicação web para resolução de métodos numéricos com interface interativa Dash + Plotly.

## Métodos Implementados

| Categoria | Métodos |
|-----------|---------|
| **Raízes** | Bissecção, Newton-Raphson, Secante |
| **Sistemas Lineares** | Fatoração LU, Eliminação de Gauss, Gauss-Seidel, Gauss-Jacobi |
| **Interpolação** | Newton, Lagrange |
| **Integração** | Simpson 1/3, Trapézio Repetido, 3/8 |
| **EDOs** | Euler, Runge-Kutta 4ª ordem |

## Funcionalidades

- Interface web com tema escuro (Dash Bootstrap — Darkly)
- Gráficos interativos com Plotly (visualização de iterações, tangentes, secantes, áreas de integração)
- Parsing seguro de expressões matemáticas digitadas pelo usuário
- Tratamento de erros numéricos com mensagens descritivas
- Validação de inputs antes do cálculo

## Instalação

```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux/Mac

pip install -r requirements.txt
```

## Uso

```bash
venv\Scripts\python.exe app.py
```

Acesse http://127.0.0.1:8050 no navegador.

## Testes

Rodar todos os testes:

```bash
PYTHONPATH=. venv\Scripts\python.exe -m unittest discover -s tests -v
```

Testar apenas um módulo:

```bash
PYTHONPATH=. venv\Scripts\python.exe -m unittest tests.test_roots -v
```

Testar apenas um caso específico:

```bash
PYTHONPATH=. venv\Scripts\python.exe -m unittest tests.test_roots.TestRootsMethods.test_bisection_simple -v
```

## Estrutura do Projeto

```
core/               # Implementação dos métodos numéricos
  roots.py          # Bissecção, Newton, Secante
  linear_systems.py # LU, Gauss, Gauss-Seidel, Gauss-Jacobi
  interpolation.py  # Newton, Lagrange
  integration.py    # Simpson, Trapézio, 3/8
  ode.py            # Euler, Runge-Kutta 4
  plot.py           # Gráficos Plotly

validation/         # Validação de inputs
utils/              # Utilitários (parsing de funções, exibição de matrizes)
pages/              # Páginas Dash (multipage app)
tests/              # Testes unitários separados por módulo
app.py              # Entry point da aplicação
```

## Tecnologias

- **Dash** — Framework web
- **Dash Bootstrap Components** — UI com tema Darkly
- **Plotly** — Gráficos interativos
- **NumPy** — Cálculos numéricos
- **Pandas** — Exibição de matrizes