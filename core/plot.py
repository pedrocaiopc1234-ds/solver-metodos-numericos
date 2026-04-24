"""
Plotting utilities for numerical methods using Plotly.
"""

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def plot_bisection(f, a, b, root, iterations):
    """
    Plot bisection method: function curve, interval [a,b], and root.
    """
    margin = (b - a) * 0.3 if b != a else 1.0
    x_min, x_max = a - margin, b + margin
    xs = np.linspace(x_min, x_max, 500)
    ys = np.array([f(xi) for xi in xs])

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=xs, y=ys, mode='lines', name='f(x)'))
    fig.add_trace(go.Scatter(x=[a, b], y=[f(a), f(b)], mode='markers',
                              marker=dict(size=10, color='orange'),
                              name='Intervalo [a, b]'))
    if root is not None:
        fig.add_trace(go.Scatter(x=[root], y=[f(root)], mode='markers',
                                  marker=dict(size=12, color='green'),
                                  name=f'Raiz ≈ {root:.6f}'))
        fig.add_vline(x=root, line=dict(dash='dash', color='green'))
    fig.add_hline(y=0, line=dict(color='black', width=1))
    fig.update_layout(title='Método da Bissecção',
                      xaxis_title='x', yaxis_title='f(x)',
                      template='plotly_white')
    return fig


def plot_newton(f, df, x0, root, iterations_data=None):
    """
    Plot Newton's method: function, tangent lines, and iteration path.
    iterations_data: list of dicts with keys 'x', 'fx', 'dfx', 'x_next'
    """
    if iterations_data:
        xs_vals = [d['x'] for d in iterations_data]
        x_min = min(xs_vals + ([root] if root is not None else []))
        x_max = max(xs_vals + ([root] if root is not None else []))
    else:
        x_min, x_max = x0 - 2, x0 + 2
    margin = (x_max - x_min) * 0.4 if x_max != x_min else 2.0
    xs = np.linspace(x_min - margin, x_max + margin, 500)
    ys = np.array([f(xi) for xi in xs])

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=xs, y=ys, mode='lines', name='f(x)'))
    fig.add_hline(y=0, line=dict(color='black', width=1))

    if iterations_data:
        for i, d in enumerate(iterations_data):
            x_i, fx_i, dfx_i = d['x'], d['fx'], d['dfx']
            x_next = d.get('x_next')
            # Tangent line: y = dfx_i * (x - x_i) + fx_i
            tan_x = np.linspace(x_i - margin*0.3, x_i + margin*0.3, 100)
            tan_y = dfx_i * (tan_x - x_i) + fx_i
            fig.add_trace(go.Scatter(x=tan_x, y=tan_y, mode='lines',
                                      line=dict(dash='dash', color='red'),
                                      name=f'Tangente it {i+1}', showlegend=False))
            fig.add_trace(go.Scatter(x=[x_i], y=[fx_i], mode='markers',
                                      marker=dict(size=10, color='red'),
                                      name=f'x{i}', showlegend=False))
            if x_next is not None:
                fig.add_trace(go.Scatter(x=[x_next, x_next], y=[0, fx_i],
                                          mode='lines', line=dict(color='blue'),
                                          showlegend=False))
                fig.add_trace(go.Scatter(x=[x_next], y=[0], mode='markers',
                                          marker=dict(size=8, color='blue'),
                                          showlegend=False))

    if root is not None:
        fig.add_trace(go.Scatter(x=[root], y=[f(root)], mode='markers',
                                  marker=dict(size=12, color='green'),
                                  name=f'Raiz ≈ {root:.6f}'))
        fig.add_vline(x=root, line=dict(dash='dash', color='green'))

    fig.update_layout(title="Método de Newton", xaxis_title='x', yaxis_title='f(x)',
                      template='plotly_white')
    return fig


def plot_secant(f, x0, x1, root, iterations_data=None):
    """
    Plot Secant method: function, secant lines, and iteration path.
    iterations_data: list of dicts with keys 'x0', 'x1', 'f0', 'f1', 'x2'
    """
    if iterations_data:
        xs_vals = []
        for d in iterations_data:
            xs_vals.extend([d['x0'], d['x1'], d.get('x2')])
        xs_vals = [v for v in xs_vals if v is not None]
        x_min = min(xs_vals + ([root] if root is not None else []))
        x_max = max(xs_vals + ([root] if root is not None else []))
    else:
        x_min, x_max = min(x0, x1) - 2, max(x0, x1) + 2
    margin = (x_max - x_min) * 0.4 if x_max != x_min else 2.0
    xs = np.linspace(x_min - margin, x_max + margin, 500)
    ys = np.array([f(xi) for xi in xs])

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=xs, y=ys, mode='lines', name='f(x)'))
    fig.add_hline(y=0, line=dict(color='black', width=1))

    if iterations_data:
        for i, d in enumerate(iterations_data):
            x0_i, x1_i, f0_i, f1_i = d['x0'], d['x1'], d['f0'], d['f1']
            x2 = d.get('x2')
            sec_x = np.array([x0_i, x1_i])
            sec_y = np.array([f0_i, f1_i])
            fig.add_trace(go.Scatter(x=sec_x, y=sec_y, mode='lines+markers',
                                      line=dict(dash='dash', color='red'),
                                      marker=dict(size=8, color='red'),
                                      name=f'Secante it {i+1}', showlegend=False))
            if x2 is not None:
                fig.add_trace(go.Scatter(x=[x2, x2], y=[0, f1_i],
                                          mode='lines', line=dict(color='blue'),
                                          showlegend=False))
                fig.add_trace(go.Scatter(x=[x2], y=[0], mode='markers',
                                          marker=dict(size=8, color='blue'),
                                          showlegend=False))

    if root is not None:
        fig.add_trace(go.Scatter(x=[root], y=[f(root)], mode='markers',
                                  marker=dict(size=12, color='green'),
                                  name=f'Raiz ≈ {root:.6f}'))
        fig.add_vline(x=root, line=dict(dash='dash', color='green'))

    fig.update_layout(title="Método da Secante", xaxis_title='x', yaxis_title='f(x)',
                      template='plotly_white')
    return fig


def _build_newton_polynomial_str(x_nodes, coefficients):
    """Build human-readable Newton polynomial string."""
    terms = []
    for i, c in enumerate(coefficients):
        if abs(c) < 1e-12:
            continue
        sign = " - " if c < 0 else " + "
        c_abs = abs(c)
        coeff_str = f"{c_abs:.6g}" if c_abs != 1 or i == 0 else ""
        if i == 0:
            term = f"{c:.6g}"
            terms.append(term)
        else:
            factors = []
            for j in range(i):
                if x_nodes[j] == 0:
                    factors.append("x")
                else:
                    factors.append(f"(x - {x_nodes[j]:.6g})")
            term = f"{coeff_str}{''.join(factors)}"
            terms.append(sign + term)
    if not terms:
        return "P(x) = 0"
    poly = "P(x) = " + terms[0] + "".join(terms[1:])
    return poly


def _newton_polynomial_func(coefficients, x_nodes):
    """Return a callable for the Newton interpolating polynomial."""
    def P(x):
        result = coefficients[0]
        for i in range(1, len(coefficients)):
            term = coefficients[i]
            for j in range(i):
                term *= (x - x_nodes[j])
            result += term
        return result
    return P


def plot_newton_interpolation(x_nodes, y_nodes, coefficients, x_eval=None, y_eval=None):
    """
    Plot Newton interpolation with polynomial shape details.
    Returns fig and a dict with polynomial info.
    """
    x_nodes = np.array(x_nodes, dtype=float)
    y_nodes = np.array(y_nodes, dtype=float)
    coefficients = np.array(coefficients, dtype=float)

    P = _newton_polynomial_func(coefficients, x_nodes)
    margin = (x_nodes.max() - x_nodes.min()) * 0.3 if len(x_nodes) > 1 else 1.0
    x_min, x_max = x_nodes.min() - margin, x_nodes.max() + margin
    xs = np.linspace(x_min, x_max, 500)
    ys = np.array([P(xi) for xi in xs])

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=xs, y=ys, mode='lines', name='Polinômio Interpolador'))
    fig.add_trace(go.Scatter(x=x_nodes, y=y_nodes, mode='markers',
                              marker=dict(size=12, color='red'),
                              name='Pontos Dados'))
    if x_eval is not None and y_eval is not None:
        fig.add_trace(go.Scatter(x=[x_eval], y=[y_eval], mode='markers',
                                  marker=dict(size=12, color='green', symbol='star'),
                                  name=f'P({x_eval:.4f}) ≈ {y_eval:.6f}'))

    fig.update_layout(title='Interpolação de Newton',
                      xaxis_title='x', yaxis_title='y',
                      template='plotly_white')

    poly_str = _build_newton_polynomial_str(x_nodes, coefficients)
    info = {
        "polynomial_string": poly_str,
        "coefficients": coefficients.tolist(),
        "degree": len(coefficients) - 1,
        "basis": "Diferenças divididas (forma de Newton)",
        "form": "P(x) = c0 + c1(x-x0) + c2(x-x0)(x-x1) + ..."
    }
    return fig, info


def _lagrange_basis_polynomials(x_nodes):
    """
    Return list of callable basis polynomials L_i(x) and their string forms.
    """
    n = len(x_nodes)
    bases = []
    strings = []
    for i in range(n):
        def make_Li(i_copy):
            def Li(x):
                result = 1.0
                for j in range(n):
                    if i_copy != j:
                        result *= (x - x_nodes[j]) / (x_nodes[i_copy] - x_nodes[j])
                return result
            return Li
        bases.append(make_Li(i))
        # Build string representation
        factors = []
        for j in range(n):
            if i != j:
                denom = x_nodes[i] - x_nodes[j]
                if x_nodes[j] == 0:
                    factors.append(f"x/{denom:.6g}")
                else:
                    factors.append(f"(x - {x_nodes[j]:.6g})/{denom:.6g}")
        if factors:
            strings.append(f"L_{i}(x) = " + " * ".join(factors))
        else:
            strings.append(f"L_{i}(x) = 1")
    return bases, strings


def _build_lagrange_polynomial_str(x_nodes, y_nodes):
    """Build human-readable Lagrange polynomial string."""
    terms = []
    for i, yi in enumerate(y_nodes):
        if abs(yi) < 1e-12:
            continue
        sign = " - " if yi < 0 else " + "
        c_abs = abs(yi)
        coeff_str = f"{c_abs:.6g}"
        factors = []
        for j in range(len(x_nodes)):
            if i != j:
                if x_nodes[j] == 0:
                    factors.append("x")
                else:
                    factors.append(f"(x - {x_nodes[j]:.6g})")
        denom = 1.0
        for j in range(len(x_nodes)):
            if i != j:
                denom *= (x_nodes[i] - x_nodes[j])
        if factors:
            term = f"{coeff_str}/({denom:.6g}) * " + " * ".join(factors)
        else:
            term = f"{coeff_str}"
        if i == 0 and yi >= 0:
            terms.append(term)
        else:
            terms.append(sign + term)
    if not terms:
        return "P(x) = 0"
    return "P(x) = " + terms[0] + "".join(terms)


def plot_lagrange_interpolation(x_nodes, y_nodes, x_eval=None, y_eval=None):
    """
    Plot Lagrange interpolation with detailed polynomial information.
    Returns fig and a dict with polynomial info.
    """
    x_nodes = np.array(x_nodes, dtype=float)
    y_nodes = np.array(y_nodes, dtype=float)
    n = len(x_nodes)

    bases, basis_strings = _lagrange_basis_polynomials(x_nodes)

    def P(x):
        result = 0.0
        for i in range(n):
            result += y_nodes[i] * bases[i](x)
        return result

    margin = (x_nodes.max() - x_nodes.min()) * 0.3 if n > 1 else 1.0
    x_min, x_max = x_nodes.min() - margin, x_nodes.max() + margin
    xs = np.linspace(x_min, x_max, 500)
    ys = np.array([P(xi) for xi in xs])

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=xs, y=ys, mode='lines', name='Polinômio Interpolador'))
    fig.add_trace(go.Scatter(x=x_nodes, y=y_nodes, mode='markers',
                              marker=dict(size=12, color='red'),
                              name='Pontos Dados'))
    if x_eval is not None and y_eval is not None:
        fig.add_trace(go.Scatter(x=[x_eval], y=[y_eval], mode='markers',
                                  marker=dict(size=12, color='green', symbol='star'),
                                  name=f'P({x_eval:.4f}) ≈ {y_eval:.6f}'))

    fig.update_layout(title='Interpolação de Lagrange',
                      xaxis_title='x', yaxis_title='y',
                      template='plotly_white')

    poly_str = _build_lagrange_polynomial_str(x_nodes, y_nodes)
    info = {
        "polynomial_string": poly_str,
        "basis_strings": basis_strings,
        "degree": n - 1,
        "basis": "Polinômios de Lagrange L_i(x)",
        "form": "P(x) = Σ y_i * L_i(x), onde L_i(x) = Π (x - x_j)/(x_i - x_j) para j≠i"
    }
    return fig, info


def plot_simpson(f, a, b, n, result):
    """
    Plot Simpson's 1/3 rule: function and parabolic areas.
    """
    a, b = float(a), float(b)
    n = int(n)
    h = (b - a) / n
    x_nodes = np.linspace(a, b, n + 1)
    y_nodes = np.array([f(xi) for xi in x_nodes])

    xs = np.linspace(a, b, 500)
    ys = np.array([f(xi) for xi in xs])

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=xs, y=ys, mode='lines', name='f(x)'))
    fig.add_trace(go.Scatter(x=x_nodes, y=y_nodes, mode='markers',
                              marker=dict(size=8, color='red'),
                              name='Pontos de integração'))

    # Shade parabolic regions
    for i in range(0, n, 2):
        x0, x1, x2 = x_nodes[i], x_nodes[i+1], x_nodes[i+2]
        y0, y1, y2 = y_nodes[i], y_nodes[i+1], y_nodes[i+2]
        px = np.linspace(x0, x2, 100)
        # Lagrange quadratic through three points
        py = np.zeros_like(px)
        for k, xk in enumerate([x0, x1, x2]):
            yk = [y0, y1, y2][k]
            Lk = np.ones_like(px)
            for m, xm in enumerate([x0, x1, x2]):
                if m != k:
                    Lk *= (px - xm) / (xk - xm)
            py += yk * Lk
        fig.add_trace(go.Scatter(x=px, y=py, fill='tonexty', mode='lines',
                                  line=dict(width=0),
                                  fillcolor='rgba(0,100,80,0.2)',
                                  showlegend=False))
        fig.add_trace(go.Scatter(x=px, y=np.zeros_like(px), mode='lines',
                                  line=dict(width=0),
                                  showlegend=False))

    fig.add_hline(y=0, line=dict(color='black', width=1))
    fig.update_layout(title=f'Regra de Simpson 1/3 (n={n}, resultado≈{result:.6f})',
                      xaxis_title='x', yaxis_title='f(x)',
                      template='plotly_white')
    return fig


def plot_trapezoidal(f, a, b, n, result):
    """
    Plot repeated trapezoidal rule: function and trapezoid areas.
    """
    a, b = float(a), float(b)
    n = int(n)
    h = (b - a) / n
    x_nodes = np.linspace(a, b, n + 1)
    y_nodes = np.array([f(xi) for xi in x_nodes])

    xs = np.linspace(a, b, 500)
    ys = np.array([f(xi) for xi in xs])

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=xs, y=ys, mode='lines', name='f(x)'))

    for i in range(n):
        x_seg = [x_nodes[i], x_nodes[i+1], x_nodes[i+1], x_nodes[i], x_nodes[i]]
        y_seg = [0, 0, y_nodes[i+1], y_nodes[i], 0]
        fig.add_trace(go.Scatter(x=x_seg, y=y_seg, fill='toself', mode='lines',
                                  fillcolor='rgba(0,100,80,0.2)',
                                  line=dict(color='rgba(0,100,80,0.5)'),
                                  showlegend=(i == 0),
                                  name='Área do trapézio'))

    fig.add_trace(go.Scatter(x=x_nodes, y=y_nodes, mode='markers',
                              marker=dict(size=8, color='red'),
                              name='Pontos de integração'))
    fig.add_hline(y=0, line=dict(color='black', width=1))
    fig.update_layout(title=f'Regra do Trapézio (n={n}, resultado≈{result:.6f})',
                      xaxis_title='x', yaxis_title='f(x)',
                      template='plotly_white')
    return fig


def plot_three_eight(f, a, b, result):
    """
    Plot Simpson's 3/8 rule: function and cubic area.
    """
    a, b = float(a), float(b)
    h = (b - a) / 3
    x_nodes = np.array([a, a + h, a + 2*h, b])
    y_nodes = np.array([f(xi) for xi in x_nodes])

    xs = np.linspace(a, b, 500)
    ys = np.array([f(xi) for xi in xs])

    # Cubic interpolant through 4 points
    px = np.linspace(a, b, 100)
    py = np.zeros_like(px)
    for k, xk in enumerate(x_nodes):
        Lk = np.ones_like(px)
        for m, xm in enumerate(x_nodes):
            if m != k:
                Lk *= (px - xm) / (xk - xm)
        py += y_nodes[k] * Lk

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=xs, y=ys, mode='lines', name='f(x)'))
    fig.add_trace(go.Scatter(x=x_nodes, y=y_nodes, mode='markers',
                              marker=dict(size=10, color='red'),
                              name='Pontos de integração'))
    fig.add_trace(go.Scatter(x=px, y=py, fill='tonexty', mode='lines',
                              line=dict(width=0),
                              fillcolor='rgba(0,100,80,0.2)',
                              showlegend=False))
    fig.add_trace(go.Scatter(x=px, y=np.zeros_like(px), mode='lines',
                              line=dict(width=0),
                              showlegend=False))

    fig.add_hline(y=0, line=dict(color='black', width=1))
    fig.update_layout(title=f'Regra de Simpson 3/8 (resultado≈{result:.6f})',
                      xaxis_title='x', yaxis_title='f(x)',
                      template='plotly_white')
    return fig
