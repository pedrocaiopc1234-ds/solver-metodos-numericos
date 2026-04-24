"""
Sistemas Lineares — Dash Page
"""

import dash
from dash import html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
from core.linear_systems import lu_factorization, gaussian_elimination, gauss_seidel, gauss_jacobi
from utils.dash_ui import display_matrix

dash.register_page(__name__, path="/sistemas-lineares", title="Sistemas Lineares", name="Sistemas Lineares")

layout = dbc.Container([
    html.H2("📐 Sistemas Lineares", className="mb-3"),
    dbc.Card([
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Método"),
                    dbc.Select(
                        id="ls-method",
                        options=[
                            {"label": "Fatoração LU", "value": "lu"},
                            {"label": "Eliminação de Gauss", "value": "gauss"},
                            {"label": "Gauss-Seidel", "value": "gauss_seidel"},
                            {"label": "Gauss-Jacobi", "value": "gauss_jacobi"},
                        ],
                        value="lu",
                    ),
                ], width=12, md=4),
            ], className="mb-3"),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Matriz A (linhas separadas por vírgula ou ponto e vírgula)"),
                    dbc.Textarea(id="ls-A", value="4, 1, 2\n1, 3, 1\n2, 1, 5", rows=4),
                ], width=12, md=6),
                dbc.Col([
                    dbc.Label("Vetor b (valores separados por vírgula)"),
                    dbc.Input(id="ls-b", type="text", value="4, 3, 7"),
                ], width=12, md=6),
            ], className="mb-3"),
            html.Div(id="ls-iter-container", children=[
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Tolerância"),
                        dbc.Input(id="ls-tol", type="number", value=1e-10, step=1e-11),
                    ], width=6, md=3),
                    dbc.Col([
                        dbc.Label("Máximo de iterações"),
                        dbc.Input(id="ls-max-iter", type="number", value=100, step=10),
                    ], width=6, md=3),
                ], className="mb-3"),
            ]),
            dbc.Button("▶️ Calcular", id="ls-calc", color="primary", className="mt-2"),
        ])
    ], className="mb-4"),

    html.Div(id="ls-output"),
], fluid=True)


@callback(
    Output("ls-iter-container", "style"),
    Input("ls-method", "value"),
)
def toggle_iter(method):
    return {"display": "block"} if method in ("gauss_seidel", "gauss_jacobi") else {"display": "none"}


@callback(
    Output("ls-output", "children"),
    Input("ls-calc", "n_clicks"),
    State("ls-method", "value"),
    State("ls-A", "value"),
    State("ls-b", "value"),
    State("ls-tol", "value"),
    State("ls-max-iter", "value"),
    prevent_initial_call=True,
)
def calculate(n_clicks, method, A_str, b_str, tol, max_iter):
    if n_clicks is None:
        return dash.no_update
    try:
        A = np.array([[float(x.strip()) for x in row.split(",")] for row in A_str.strip().splitlines() if row.strip()])
        b = np.array([float(x.strip()) for x in b_str.split(",")])
        tol = float(tol) if tol is not None else 1e-10
        max_iter = int(max_iter) if max_iter is not None else 100

        children = []
        children.append(html.H5("Entrada Validada"))
        df_A = display_matrix(A, "A")
        df_b = display_matrix(b.reshape(-1, 1), "b")
        children.append(dbc.Row([
            dbc.Col(dbc.Card([dbc.CardBody([html.H6("Matriz A"), dbc.Table.from_dataframe(df_A, striped=True, bordered=True, hover=True, responsive="sm", className="text-center")])]), width=6),
            dbc.Col(dbc.Card([dbc.CardBody([html.H6("Vetor b"), dbc.Table.from_dataframe(df_b, striped=True, bordered=True, hover=True, responsive="sm", className="text-center")])]), width=6),
        ], className="mb-3"))

        if method == "lu":
            result = lu_factorization(A, b)
        elif method == "gauss":
            result = gaussian_elimination(A, b)
        elif method == "gauss_seidel":
            result = gauss_seidel(A, b, tol=tol, max_iter=max_iter)
        else:
            result = gauss_jacobi(A, b, tol=tol, max_iter=max_iter)

        if not result.get("success"):
            children.append(dbc.Alert(result.get("error", "Erro desconhecido"), color="danger"))
            return children

        children.append(dbc.Alert("Solução encontrada com sucesso!", color="success"))

        if method in ("gauss_seidel", "gauss_jacobi"):
            children.append(dbc.Row([
                dbc.Col(dbc.Card([dbc.CardBody([html.H5("Iterações"), html.P(str(result.get("iterations", 0)))])]), width=4),
                dbc.Col(dbc.Card([dbc.CardBody([html.H5("Tolerância"), html.P(f"{tol:.2e}")])]), width=4),
                dbc.Col(dbc.Card([dbc.CardBody([html.H5("Convergiu"), html.P("Sim ✅")])]), width=4),
            ], className="mb-3"))

        if method == "lu" and "L" in result and "U" in result:
            df_L = display_matrix(result["L"], "L")
            df_U = display_matrix(result["U"], "U")
            children.append(dbc.Row([
                dbc.Col(dbc.Card([dbc.CardBody([html.H6("Matriz L"), dbc.Table.from_dataframe(df_L, striped=True, bordered=True, hover=True, responsive="sm", className="text-center")])]), width=6),
                dbc.Col(dbc.Card([dbc.CardBody([html.H6("Matriz U"), dbc.Table.from_dataframe(df_U, striped=True, bordered=True, hover=True, responsive="sm", className="text-center")])]), width=6),
            ], className="mb-3"))

        x = result.get("x")
        if x is not None:
            x = np.array(x)
            df_x = display_matrix(x.reshape(-1, 1), "x")
            children.append(dbc.Card([
                dbc.CardBody([
                    html.H5("Solução x"),
                    dbc.Table.from_dataframe(df_x, striped=True, bordered=True, hover=True, responsive="sm", className="text-center"),
                ])
            ], className="mb-3"))
            Ax = np.dot(A, x)
            err = np.linalg.norm(Ax - b)
            df_Ax = display_matrix(Ax.reshape(-1, 1), "A·x")
            children.append(dbc.Card([
                dbc.CardBody([
                    html.H5("Verificação A·x"),
                    dbc.Table.from_dataframe(df_Ax, striped=True, bordered=True, hover=True, responsive="sm", className="text-center"),
                    html.P(f"Erro ||Ax - b||₂: {err:.2e}"),
                ])
            ], className="mb-3"))

        return children
    except Exception as e:
        return dbc.Alert(f"Erro ao processar entrada: {e}", color="danger")
