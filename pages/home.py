"""
Landing / Home Page
"""

import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/", title="Início", name="Início")

layout = dbc.Container([
    html.H1("📊 Solver de Métodos Numéricos", className="text-center my-4"),
    html.Hr(),
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("🎯 Raízes", className="card-title"),
                html.P("Encontre zeros de funções reais com:"),
                html.Ul([
                    html.Li("Bissecção"),
                    html.Li("Newton-Raphson"),
                    html.Li("Secante"),
                ]),
            ])
        ]), width=12, md=4, className="mb-3"),
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("📐 Sistemas Lineares", className="card-title"),
                html.P("Resolva sistemas Ax = b com:"),
                html.Ul([
                    html.Li("Fatoração LU"),
                    html.Li("Eliminação de Gauss"),
                    html.Li("Gauss-Seidel"),
                    html.Li("Gauss-Jacobi"),
                ]),
            ])
        ]), width=12, md=4, className="mb-3"),
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("📈 Interpolação", className="card-title"),
                html.P("Aproxime funções por polinômios com:"),
                html.Ul([
                    html.Li("Newton (diferenças divididas)"),
                    html.Li("Lagrange"),
                ]),
            ])
        ]), width=12, md=4, className="mb-3"),
    ]),
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("📉 Integração", className="card-title"),
                html.P("Calcule integrais definidas com:"),
                html.Ul([
                    html.Li("Simpson 1/3"),
                    html.Li("Trapézio Repetido"),
                    html.Li("Simpson 3/8"),
                ]),
            ])
        ]), width=12, md=4, className="mb-3"),
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("🌊 EDOs", className="card-title"),
                html.P("Resolva equações diferenciais com:"),
                html.Ul([
                    html.Li("Euler"),
                    html.Li("Runge-Kutta 4ª ordem"),
                ]),
            ])
        ]), width=12, md=4, className="mb-3"),
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("✨ Recursos", className="card-title"),
                html.P("O que o solver oferece:"),
                html.Ul([
                    html.Li("Visualizações interativas com Plotly"),
                    html.Li("Tabelas de iterações detalhadas"),
                    html.Li("Informações sobre polinômios interpoladores"),
                    html.Li("Gráficos de convergência e áreas"),
                ]),
            ])
        ]), width=12, md=4, className="mb-3"),
    ]),
    html.Hr(),
    html.P("Selecione um método no menu superior para começar.", className="text-center text-muted"),
], fluid=True)
