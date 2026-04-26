"""
Métodos para Encontrar Raízes — Dash Page
"""

import dash
from dash import html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
from core.roots import bisection, newton, secant
from core.plot import plot_bisection, plot_newton, plot_secant
from utils.dash_ui import parse_function
from validation.roots_validation import validate_interval, validate_tolerance, validate_max_iterations, validate_initial_guess

dash.register_page(__name__, path="/raizes", title="Raízes", name="Raízes")

layout = dbc.Container([
    html.H2("🎯 Métodos para Encontrar Raízes", className="mb-3"),
    dbc.Card([
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Método"),
                    dbc.Select(
                        id="root-method",
                        options=[
                            {"label": "Bissecção", "value": "bisection"},
                            {"label": "Newton-Raphson", "value": "newton"},
                            {"label": "Secante", "value": "secant"},
                        ],
                        value="bisection",
                    ),
                ], width=12, md=4),
            ], className="mb-3"),
            dbc.Row([
                dbc.Col([
                    dbc.Label("f(x) ="),
                    dbc.Input(id="root-f", type="text", value="x**2 - 4"),
                ], width=12, md=6),
            ], className="mb-3"),
            html.Div(id="newton-df-container", children=[
                dbc.Row([
                    dbc.Col([
                        dbc.Label("f'(x) ="),
                        dbc.Input(id="root-df", type="text", value="2*x"),
                    ], width=12, md=6),
                ], className="mb-3"),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("a / x₀"),
                    dbc.Input(id="root-a", type="number", value=0.0, step=0.1),
                ], width=6, md=3),
                dbc.Col([
                    dbc.Label("b / x₁"),
                    dbc.Input(id="root-b", type="number", value=3.0, step=0.1),
                ], width=6, md=3),
                dbc.Col([
                    dbc.Label("Tolerância"),
                    dbc.Input(id="root-tol", type="number", value=1e-6, step=1e-7),
                ], width=6, md=3),
                dbc.Col([
                    dbc.Label("Máximo de iterações"),
                    dcc.Slider(id="root-max-iter", min=10, max=500, step=10, value=100,
                               marks={10:"10",100:"100",200:"200",300:"300",400:"400",500:"500"}),
                ], width=6, md=3),
            ], className="mb-3"),
            dbc.Button("▶️ Calcular", id="root-calc", color="primary", className="mt-2"),
        ])
    ], className="mb-4"),

    html.Div(id="root-output"),
], fluid=True)


@callback(
    Output("newton-df-container", "style"),
    Input("root-method", "value"),
)
def toggle_df(method):
    return {"display": "block"} if method == "newton" else {"display": "none"}


@callback(
    Output("root-output", "children"),
    Input("root-calc", "n_clicks"),
    State("root-method", "value"),
    State("root-f", "value"),
    State("root-df", "value"),
    State("root-a", "value"),
    State("root-b", "value"),
    State("root-tol", "value"),
    State("root-max-iter", "value"),
    prevent_initial_call=True,
)
def calculate(n_clicks, method, f_str, df_str, a, b, tol, max_iter):
    if n_clicks is None:
        return dash.no_update
    try:
        f = parse_function(f_str or "x")
        tol = float(tol) if tol is not None else 1e-6
        max_iter = int(max_iter) if max_iter is not None else 100
        a = float(a) if a is not None else 0.0
        b = float(b) if b is not None else 0.0

        # ── Validação de entrada ──
        errors = []

        v = validate_tolerance(tol)
        if not v["valid"]:
            errors.append(v["error"])

        v = validate_max_iterations(max_iter)
        if not v["valid"]:
            errors.append(v["error"])

        if method == "bisection":
            v = validate_interval(a, b)
            if not v["valid"]:
                errors.append(v["error"])

        if method == "newton":
            v = validate_initial_guess(a)
            if not v["valid"]:
                errors.append(v["error"])

        if method == "secant":
            v = validate_initial_guess(a)
            if not v["valid"]:
                errors.append(v["error"])
            v = validate_initial_guess(b)
            if not v["valid"]:
                errors.append(v["error"])
            if a is not None and b is not None and abs(float(b) - float(a)) < 1e-15:
                errors.append("x₀ e x₁ devem ser diferentes")

        if errors:
            return dbc.Alert("❌ " + " | ".join(errors), color="danger")

        # ── Cálculo ──
        if method == "bisection":
            result = bisection(f, a, b, tol, max_iter)
            fig = plot_bisection(f, a, b, result.get("root"), result.get("iterations")) if result.get("success") else None
        elif method == "newton":
            df = parse_function(df_str or "1")
            result = newton(f, df, a, tol, max_iter)
            fig = plot_newton(f, df, a, result.get("root"), result.get("iterations_data")) if result.get("success") else None
        else:
            result = secant(f, a, b, tol, max_iter)
            fig = plot_secant(f, a, b, result.get("root"), result.get("iterations_data")) if result.get("success") else None

        children = []
        if not result.get("success"):
            children.append(dbc.Alert(result.get("error", "Erro desconhecido"), color="danger"))
        else:
            children.append(dbc.Alert("Raiz encontrada com sucesso!", color="success"))
            root_val = result.get("root")
            iterations = result.get("iterations", 0)
            f_root = f(root_val) if root_val is not None else None
            children.append(dbc.Row([
                dbc.Col(dbc.Card([
                    dbc.CardBody([
                        html.H5("Raiz aproximada", className="card-title"),
                        html.P(f"{root_val:.10f}", className="card-text"),
                    ])
                ]), width=4),
                dbc.Col(dbc.Card([
                    dbc.CardBody([
                        html.H5("Iterações", className="card-title"),
                        html.P(str(iterations), className="card-text"),
                    ])
                ]), width=4),
                dbc.Col(dbc.Card([
                    dbc.CardBody([
                        html.H5("f(raiz)", className="card-title"),
                        html.P(f"{f_root:.2e}", className="card-text"),
                    ])
                ]), width=4),
            ], className="mb-3"))

        if fig:
            children.append(dbc.Card([
                dbc.CardBody([
                    html.H5("Gráfico"),
                    dcc.Graph(figure=fig),
                ])
            ], className="mb-3"))

        it_data = result.get("iterations_data")
        if it_data:
            df = pd.DataFrame(it_data)
            df.index = df.index + 1
            df.index.name = "Iteração"
            df = df.reset_index()
            for col in df.columns:
                if col != "Iteração":
                    df[col] = df[col].apply(lambda x: f"{x:.6g}" if isinstance(x, float) else str(x))
            children.append(dbc.Card([
                dbc.CardBody([
                    html.H5("Tabela de Iterações"),
                    dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, responsive="sm", className="text-center"),
                ])
            ], className="mb-3"))

        return children
    except Exception as e:
        return dbc.Alert(f"Erro ao processar entrada: {e}", color="danger")