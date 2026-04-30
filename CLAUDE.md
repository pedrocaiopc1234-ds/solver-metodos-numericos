# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run the app (browser mode, http://127.0.0.1:8050)
PYTHONPATH=. venv/Scripts/python.exe app.py

# Run the app (desktop mode via pywebview)
PowerShell: & "venv\Scripts\python.exe" main.py

# Run all tests
PYTHONPATH=. venv/Scripts/python.exe -m unittest discover -s tests -v
python -m pytest tests/ -v

# Run a single test class
PYTHONPATH=. venv/Scripts/python.exe -m unittest tests.test_roots.TestBisectionRobustness -v

# Run a single test
PYTHONPATH=. venv/Scripts/python.exe -m unittest tests.test_ode.TestRK4Robustness.test_robust_18 -v

# Build standalone executable (outputs to dist/NumerPy Solver/)
python build.py

# Install dependencies
pip install -r requirements.txt
```

## Architecture

NumerPy Solver is a numerical methods calculator with a Dash/Plotly web UI. The codebase follows a strict layered architecture where each layer has a single responsibility.

### Core layer (`core/`) — Pure computation, no UI

Every function returns a standardized dict: `{"success": bool, <result_key>: value, "error": str|None}`. Iterative methods also return `"iterations"` (int) and `"iterations_data"` (list of dicts for plotting). All methods are wrapped in try/except and defensively validate inputs (NaN, Inf, singular matrices, zero derivatives, divergence).

- `roots.py`: `bisection`, `newton`, `secant`
- `linear_systems.py`: `lu_factorization`, `gaussian_elimination`, `gauss_seidel`, `gauss_jacobi` — iterative methods also return `"warning"` when the matrix is not diagonally dominant
- `interpolation.py`: `newton_interpolation` (Horner evaluation), `lagrange_interpolation`
- `integration.py`: `simpson` (1/3), `trapezoidal_repeated`, `three_eight_method` (3/8)
- `ode.py`: `euler_method`, `runge_kutta_4` — use `actual_h` from `np.linspace` step to keep `t` and `y` synchronized
- `plot.py`: Plotly figure generators for every method, plus polynomial string builders for interpolation

### Validation layer (`validation/`) — Input sanitization

Functions return `{"valid": bool, "error": str|None}`. Called from Dash page callbacks before invoking core methods. Each module mirrors a core module. Key validations: bounds on tolerance (1e-15 to 1), step size (1e-10 to 100), max iterations (≤10000), matrix size (≤100x100), even `n` for Simpson, diagonal dominance warnings for iterative solvers.

### Utils layer (`utils/`) — Expression parsing and UI helpers

- `dash_ui.py` (active): `parse_function(expr_str)` compiles `lambda x: <expr>` with restricted `SAFE_GLOBALS`. `parse_function_2d(expr_str)` compiles `lambda t, y: <expr>`. Both detect complex return values and raise `ValueError`.
- `ui.py` (Streamlit legacy): same parsing functions, kept for backward compatibility.

### Pages layer (`pages/`) — Dash UI with callbacks

Each page uses `dash.register_page()` and follows the same pattern: layout with inputs → callback validates via `validation/` → calls `core/` → renders result cards, Plotly graphs, iteration tables. Routing uses Dash's `use_pages=True` with numbered filename prefixes.

## Key conventions

- User-facing text is in Portuguese (pt-BR). Error messages, UI labels, and page content are all in Portuguese.
- Function expressions from users use `x` as the variable for 1D functions and `t, y` for ODE functions.
- The `SAFE_GLOBALS` dict in `utils/` defines what math functions are available to user expressions: `sin, cos, tan, asin, acos, atan, sinh, cosh, tanh, exp, log, log10, sqrt, pi, e, abs, np, math`.
- Tests use Python `unittest` (stdlib). Each method has basic tests + 20 robustness tests per variant covering singular inputs, NaN/Inf, pathological functions, boundary conditions, and max-iteration exhaustion.