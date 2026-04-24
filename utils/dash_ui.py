"""
Common UI utilities for Dash pages.
"""

import math
import numpy as np
import plotly.graph_objects as go

SAFE_GLOBALS = {
    "np": np,
    "math": math,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "asin": math.asin,
    "acos": math.acos,
    "atan": math.atan,
    "sinh": math.sinh,
    "cosh": math.cosh,
    "tanh": math.tanh,
    "exp": math.exp,
    "log": math.log,
    "log10": math.log10,
    "sqrt": math.sqrt,
    "pi": math.pi,
    "e": math.e,
    "abs": abs,
}


def parse_function(expr_str):
    """Safely parse a math expression string into a callable f(x)."""
    expr_str = expr_str.strip()
    code = compile(f"lambda x: {expr_str}", "<string>", "eval")
    return eval(code, SAFE_GLOBALS.copy())


def parse_function_2d(expr_str):
    """Safely parse a math expression string into a callable f(t, y)."""
    expr_str = expr_str.strip()
    code = compile(f"lambda t, y: {expr_str}", "<string>", "eval")
    return eval(code, SAFE_GLOBALS.copy())


def dash_result_card(success, error_msg="Erro desconhecido"):
    """Return a Dash Alert for success/error states."""
    if success:
        return None  # handled by caller with success styling
    else:
        from dash import html
        return html.Div(
            html.Strong(f"Erro: {error_msg}"),
            className="alert alert-danger",
            role="alert",
        )


def display_matrix(mat, title="Matriz"):
    """Return a rounded numpy matrix as a pandas DataFrame."""
    import pandas as pd
    rounded = np.round(mat, 6)
    if rounded.ndim == 1:
        rounded = rounded.reshape(-1, 1)
    return pd.DataFrame(rounded)


def plot_ode_solution(t, y, method_name="Método"):
    """Plot ODE solution using Plotly."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=t, y=y,
        mode='lines+markers',
        name='y(t)',
        line=dict(color='#1f77b4', width=2),
        marker=dict(size=6)
    ))
    fig.update_layout(
        title=f'Solução da EDO — {method_name}',
        xaxis_title='t',
        yaxis_title='y',
        template='plotly_dark',
        hovermode='x unified',
        height=500,
    )
    return fig
