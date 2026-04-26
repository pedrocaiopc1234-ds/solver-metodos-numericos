"""
EDOs — Euler e Runge-Kutta 4ª Ordem — Dash Page
"""

import dash
from dash import html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
from core.ode import euler_method, runge_kutta_4
from utils.dash_ui import parse_function_2d, plot_ode_solution
from validation.ode_validation import validate_initial_condition, validate_time_interval, validate_step_size

dash.register_page(__name__, path="/edos", title="EDOs", name="EDOs")

layout = dbc.Container([
    html.H2("🌊 Equações Diferenciais Ordinárias", className="mb-3"),
    dbc.Card([
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Método"),
                    dbc.Select(
                        id="ode-method",
                        options=[
                            {"label": "Euler", "value": "euler"},
                            {"label": "Runge-Kutta 4ª Ordem", "value": "rk4"},
                        ],
                        value="euler",
                    ),
                ], width=12, md=4),
            ], className="mb-3"),
            dbc.Row([
                dbc.Col([
                    dbc.Label("f(t, y) ="),
                    dbc.Input(id="ode-f", type="text", value="y"),
                ], width=12, md=6),
                dbc.Col([
                    dbc.Label("y(0) ="),
                    dbc.Input(id="ode-y0", type="number", value=1.0, step=0.1),
                ], width=6, md=3),
            ], className="mb-3"),
            dbc.Row([
                dbc.Col([
                    dbc.Label("t₀"),
                    dbc.Input(id="ode-t0", type="number", value=0.0, step=0.1),
                ], width=4, md=3),
                dbc.Col([
                    dbc.Label("t_final"),
                    dbc.Input(id="ode-tf", type="number", value=1.0, step=0.1),
                ], width=4, md=3),
                dbc.Col([
                    dbc.Label("Passo h"),
                    dbc.Input(id="ode-h", type="number", value=0.1, step=0.01),
                ], width=4, md=3),
            ], className="mb-3"),
            dbc.Button("▶️ Calcular", id="ode-calc", color="primary", className="mt-2"),
        ])
    ], className="mb-4"),

    html.Div(id="ode-output"),
], fluid=True)


@callback(
    Output("ode-output", "children"),
    Input("ode-calc", "n_clicks"),
    State("ode-method", "value"),
    State("ode-f", "value"),
    State("ode-y0", "value"),
    State("ode-t0", "value"),
    State("ode-tf", "value"),
    State("ode-h", "value"),
    prevent_initial_call=True,
)
def calculate(n_clicks, method, f_str, y0, t0, tf, h):
    if n_clicks is None:
        return dash.no_update
    try:
        f = parse_function_2d(f_str or "y")
        y0 = float(y0) if y0 is not None else 1.0
        t0 = float(t0) if t0 is not None else 0.0
        tf = float(tf) if tf is not None else 1.0
        h = float(h) if h is not None else 0.1

        # ── Validação de entrada ──
        errors = []

        v = validate_initial_condition(y0)
        if not v["valid"]:
            errors.append(v["error"])

        v = validate_time_interval(t0, tf)
        if not v["valid"]:
            errors.append(v["error"])

        v = validate_step_size(h)
        if not v["valid"]:
            errors.append(v["error"])

        if errors:
            return dbc.Alert("❌ " + " | ".join(errors), color="danger")

        # ── Cálculo ──
        if method == "euler":
            result = euler_method(f, y0, t0, tf, h)
        else:
            result = runge_kutta_4(f, y0, t0, tf, h)

        children = []
        if not result.get("success"):
            children.append(dbc.Alert(result.get("error", "Erro desconhecido"), color="danger"))
            return children

        t = result["t"]
        y = result["y"]
        children.append(dbc.Alert("Solução encontrada com sucesso!", color="success"))
        children.append(dbc.Row([
            dbc.Col(dbc.Card([dbc.CardBody([html.H5("y(t_final)"), html.P(f"{y[-1]:.6f}")])]), width=4),
            dbc.Col(dbc.Card([dbc.CardBody([html.H5("Passos"), html.P(str(len(t)))])]), width=4),
            dbc.Col(dbc.Card([dbc.CardBody([html.H5("Passo h"), html.P(f"{h:.4f}")])]), width=4),
        ], className="mb-3"))

        fig = plot_ode_solution(t, y, "Euler" if method == "euler" else "Runge-Kutta 4ª Ordem")
        children.append(dbc.Card([
            dbc.CardBody([
                html.H5("Gráfico da Solução"),
                dcc.Graph(figure=fig),
            ])
        ], className="mb-3"))

        df = pd.DataFrame({"t": t, "y": y})
        children.append(dbc.Card([
            dbc.CardBody([
                html.H5("Tabela de Valores"),
                dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, responsive="sm", className="text-center"),
            ])
        ], className="mb-3"))

        return children
    except Exception as e:
        return dbc.Alert(f"Erro ao processar entrada: {e}", color="danger")