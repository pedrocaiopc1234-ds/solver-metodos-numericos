"""
Common UI utilities for Streamlit pages.
"""

import math
import numpy as np
import streamlit as st
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
    """Safely parse a math expression string into a callable f(x).
    Raises ValueError if the expression produces complex numbers for a test value."""
    expr_str = expr_str.strip()
    code = compile(f"lambda x: {expr_str}", "<string>", "eval")
    f = eval(code, SAFE_GLOBALS.copy())
    test_val = f(1.0)
    if isinstance(test_val, complex):
        raise ValueError(f"Expressão retorna valor complexo ({test_val}). Use apenas funções reais.")
    return f


def parse_function_2d(expr_str):
    """Safely parse a math expression string into a callable f(t, y).
    Raises ValueError if the expression produces complex numbers for test values."""
    expr_str = expr_str.strip()
    code = compile(f"lambda t, y: {expr_str}", "<string>", "eval")
    f = eval(code, SAFE_GLOBALS.copy())
    test_val = f(0.0, 1.0)
    if isinstance(test_val, complex):
        raise ValueError(f"Expressão retorna valor complexo ({test_val}). Use apenas funções reais.")
    return f


def show_result_card(result_dict, title="Resultado"):
    """Display a result card with success/error states."""
    if result_dict.get("success"):
        st.success(f"{title} encontrado com sucesso!")
    else:
        st.error(result_dict.get("error", "Erro desconhecido"))


def styled_metric(label, value, delta=None):
    """Display a metric in a nice card-like container."""
    if delta is not None:
        st.metric(label=label, value=value, delta=delta)
    else:
        st.metric(label=label, value=value)


def display_matrix(mat, title="Matriz"):
    """Display a numpy matrix with a title."""
    st.markdown(f"**{title}**")
    st.dataframe(np.round(mat, 6), use_container_width=True)


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
        template='plotly_white',
        hovermode='x unified',
        height=500,
    )
    return fig
