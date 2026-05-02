"""
Integração Numérica — Dash Page
"""

import dash
from dash import html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
import numpy as np
from core.integration import simpson, trapezoidal_repeated, three_eight_method
from core.plot import plot_simpson, plot_trapezoidal, plot_three_eight
from utils.dash_ui import parse_function
from validation.integration_validation import validate_integration_interval, validate_subintervals

dash.register_page(__name__, path="/integracao", title="Integração", name="Integração")

layout = dbc.Container([
    html.H2("📉 Integração Numérica", className="mb-3"),
    dbc.Card([
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Método"),
                    dbc.Select(
                        id="int-method",
                        options=[
                            {"label": "Simpson 1/3", "value": "simpson"},
                            {"label": "Trapézio Repetido", "value": "trapezoidal"},
                            {"label": "Simpson 3/8", "value": "three_eight"},
                        ],
                        value="simpson",
                    ),
                ], width=12, md=4),
            ], className="mb-3"),
            dbc.Row([
                dbc.Col([
                    dbc.Label("f(x) ="),
                    dbc.Input(id="int-f", type="text", value="x**2"),
                ], width=12, md=4),
                dbc.Col([
                    dbc.Label("a (limite inferior)"),
                    dbc.Input(id="int-a", type="number", value=0.0, step=0.1),
                ], width=6, md=4),
                dbc.Col([
                    dbc.Label("b (limite superior)"),
                    dbc.Input(id="int-b", type="number", value=2.0, step=0.1),
                ], width=6, md=4),
            ], className="mb-3"),
            dbc.Row([
                dbc.Col([
                    dbc.Label("n (subintervalos)"),
                    dbc.Input(id="int-n", type="number", value=99, step=1),
                ], width=12, md=4),
            ], className="mb-3"),
            html.Div(id="int-n-warning"),
            dbc.Button("▶️ Calcular", id="int-calc", color="primary", className="mt-2"),
        ])
    ], className="mb-4"),

    html.Div(id="int-output"),
], fluid=True)


@callback(
    Output("int-n-warning", "children"),
    Output("int-n", "disabled"),
    Input("int-method", "value"),
    State("int-n", "value"),
)
def update_n_warning(method, n):
    if method == "simpson":
        # Simpson 1/3: n deve ser par (múltiplo de 2)
        if n is not None and int(n) % 2 != 0:
            return dbc.Alert("Para Simpson 1/3, n deve ser par (múltiplo de 2).", color="warning"), False
        return None, False
    elif method == "three_eight":
        # Simpson 3/8: n deve ser múltiplo de 3
        if n is not None and int(n) % 3 != 0:
            return dbc.Alert("Para Simpson 3/8, n deve ser múltiplo de 3.", color="warning"), False
        return None, False
    return None, False


@callback(
    Output("int-output", "children"),
    Input("int-calc", "n_clicks"),
    State("int-method", "value"),
    State("int-f", "value"),
    State("int-a", "value"),
    State("int-b", "value"),
    State("int-n", "value"),
    prevent_initial_call=True,
)
def calculate(n_clicks, method, f_str, a, b, n):
    if n_clicks is None:
        return dash.no_update
    try:
        f = parse_function(f_str or "x")
        a = float(a) if a is not None else 0.0
        b = float(b) if b is not None else 0.0
        n = int(n) if n is not None else 4

        # ── Validação de entrada ──
        errors = []

        v = validate_integration_interval(a, b)
        if not v["valid"]:
            errors.append(v["error"])

        if method == "simpson":
            v = validate_subintervals(n, must_be_even=True)
            if not v["valid"]:
                errors.append(v["error"])
        elif method == "three_eight":
            v = validate_subintervals(n, must_be_multiple_of_3=True)
            if not v["valid"]:
                errors.append(v["error"])
        else:
            # trapezoidal: apenas verifica n > 0
            v = validate_subintervals(n)
            if not v["valid"]:
                errors.append(v["error"])

        if errors:
            return dbc.Alert("❌ " + " | ".join(errors), color="danger")

        # ── Cálculo ──
        if method == "simpson":
            result = simpson(f, a, b, n)
            fig = plot_simpson(f, a, b, n, result["result"]) if result.get("success") else None
        elif method == "trapezoidal":
            result = trapezoidal_repeated(f, a, b, n)
            fig = plot_trapezoidal(f, a, b, n, result["result"]) if result.get("success") else None
        else:
            result = three_eight_method(f, a, b, n)
            fig = plot_three_eight(f, a, b, n, result["result"]) if result.get("success") else None

        children = []
        if not result.get("success"):
            children.append(dbc.Alert(result.get("error", "Erro desconhecido"), color="danger"))
            return children

        children.append(dbc.Alert("Integral calculada com sucesso!", color="success"))
        n_used = n
        children.append(dbc.Row([
            dbc.Col(dbc.Card([dbc.CardBody([html.H5("Integral aproximada"), html.P(f"{result['result']:.10f}")])]), width=6),
            dbc.Col(dbc.Card([dbc.CardBody([html.H5("n (subintervalos)"), html.P(str(n_used))])]), width=6),
        ], className="mb-3"))

        if fig:
            children.append(dbc.Card([
                dbc.CardBody([
                    dcc.Graph(figure=fig),
                ])
            ], className="mb-3"))

        return children
    except Exception as e:
        return dbc.Alert(f"Erro ao processar entrada: {e}", color="danger")