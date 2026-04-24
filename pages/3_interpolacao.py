"""
Interpolação Polinomial — Dash Page
"""

import dash
from dash import html, dcc, callback, Output, Input, State, dash_table
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
from core.interpolation import newton_interpolation, lagrange_interpolation
from core.plot import plot_newton_interpolation, plot_lagrange_interpolation

dash.register_page(__name__, path="/interpolacao", title="Interpolação", name="Interpolação")

METHODS = [
    {"label": "Newton (Diferenças Divididas)", "value": "newton"},
    {"label": "Lagrange", "value": "lagrange"},
]

layout = dbc.Container([
    html.H2("📈 Interpolação Polinomial", className="mb-3"),
    dbc.Card([
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Método"),
                    dcc.Dropdown(
                        id="interp-method",
                        options=METHODS,
                        value="newton",
                        clearable=False,
                    ),
                ], width=12, md=4),
            ], className="mb-3"),
            dbc.Row([
                dbc.Col([
                    dbc.Label("x (separados por vírgula)"),
                    dbc.Input(id="interp-x", type="text", value="1, 2, 3, 4"),
                ], width=12, md=6),
                dbc.Col([
                    dbc.Label("y (separados por vírgula)"),
                    dbc.Input(id="interp-y", type="text", value="1, 4, 9, 16"),
                ], width=12, md=6),
            ], className="mb-3"),
            dbc.Row([
                dbc.Col([
                    dbc.Label("x a avaliar"),
                    dbc.Input(id="interp-xeval", type="number", value=2.5, step=0.1),
                ], width=12, md=4),
            ], className="mb-3"),
            dbc.Button("▶️ Calcular", id="interp-calc", color="primary", className="mt-2"),
        ])
    ], className="mb-4"),

    html.Div(id="interp-output"),
], fluid=True)


@callback(
    Output("interp-output", "children"),
    Input("interp-calc", "n_clicks"),
    State("interp-method", "value"),
    State("interp-x", "value"),
    State("interp-y", "value"),
    State("interp-xeval", "value"),
    prevent_initial_call=True,
)
def calculate(n_clicks, method, x_str, y_str, x_eval):
    if n_clicks is None:
        return dash.no_update
    try:
        x = np.array([float(v.strip()) for v in x_str.split(",")])
        y = np.array([float(v.strip()) for v in y_str.split(",")])
        x_eval = float(x_eval) if x_eval is not None else 0.0

        children = []
        if len(x) != len(y):
            return dbc.Alert("x e y devem ter o mesmo número de elementos.", color="danger")
        if len(x) < 2:
            return dbc.Alert("Mínimo de 2 pontos necessários.", color="danger")

        pts_df = pd.DataFrame({"x": x, "y": y})
        children.append(dbc.Card([
            dbc.CardBody([
                html.H5("Pontos de Interpolação"),
                dash_table.DataTable(
                    data=pts_df.to_dict("records"),
                    columns=[{"name": c, "id": c} for c in pts_df.columns],
                    style_table={"overflowX": "auto"},
                    style_cell={"textAlign": "center"},
                )
            ])
        ], className="mb-3"))

        if method == "newton":
            result = newton_interpolation(x, y, x_eval)
        else:
            result = lagrange_interpolation(x, y, x_eval)

        if not result.get("success"):
            children.append(dbc.Alert(result.get("error", "Erro desconhecido"), color="danger"))
            return children

        children.append(dbc.Alert("Interpolação realizada com sucesso!", color="success"))
        children.append(dbc.Row([
            dbc.Col(dbc.Card([dbc.CardBody([html.H5("P(x) avaliado"), html.P(f"{result['result']:.6f}")])]), width=4),
            dbc.Col(dbc.Card([dbc.CardBody([html.H5("Grau do polinômio"), html.P(str(len(x) - 1))])]), width=4),
            dbc.Col(dbc.Card([dbc.CardBody([html.H5("x avaliado"), html.P(f"{x_eval:.4f}")])]), width=4),
        ], className="mb-3"))

        if method == "newton":
            fig, info = plot_newton_interpolation(x, y, result.get("coefficients"), x_eval=x_eval, y_eval=result["result"])
        else:
            fig, info = plot_lagrange_interpolation(x, y, x_eval=x_eval, y_eval=result["result"])

        children.append(dbc.Card([
            dbc.CardBody([
                html.H5("Gráfico do Polinômio Interpolador"),
                dcc.Graph(figure=fig),
            ])
        ], className="mb-3"))

        info_children = [
            html.P(f"Base: {info['basis']}"),
            html.P(f"Forma: {info['form']}"),
            html.P(f"Grau: {info['degree']}"),
        ]
        if "coefficients" in info:
            info_children.append(html.P("Coeficientes (c₀, c₁, ...):"))
            for i, c in enumerate(info["coefficients"]):
                info_children.append(html.P(f"c{i} = {c:.6g}"))
        if "basis_strings" in info:
            info_children.append(html.P("Polinômios base Lᵢ(x):"))
            for s in info["basis_strings"]:
                info_children.append(html.P(f"{s}"))
        info_children.append(html.Pre(info["polynomial_string"], className="bg-dark p-2 rounded"))

        children.append(dbc.Card([
            dbc.CardBody([
                html.H5("Informações do Polinômio"),
                html.Div(info_children),
            ])
        ], className="mb-3"))

        return children
    except Exception as e:
        return dbc.Alert(f"Erro ao processar entrada: {e}", color="danger")
