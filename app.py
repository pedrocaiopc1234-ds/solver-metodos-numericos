"""
Numerical Methods Solver — Dash App
===================================
Run with: python app.py
"""

import dash
import dash_bootstrap_components as dbc
from dash import html, dcc

app = dash.Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.DARKLY, dbc.icons.FONT_AWESOME],
    suppress_callback_exceptions=True,
)

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Início", href="/")),
        dbc.NavItem(dbc.NavLink("Raízes", href="/raizes")),
        dbc.NavItem(dbc.NavLink("Sistemas Lineares", href="/sistemas-lineares")),
        dbc.NavItem(dbc.NavLink("Interpolação", href="/interpolacao")),
        dbc.NavItem(dbc.NavLink("Integração", href="/integracao")),
        dbc.NavItem(dbc.NavLink("EDOs", href="/edos")),
    ],
    brand="Solver de Métodos Numéricos",
    brand_href="/",
    color="primary",
    dark=True,
    fluid=True,
    className="mb-4",
)

app.layout = dbc.Container(
    [
        navbar,
        dash.page_container,
        html.Hr(),
        html.Footer(
            dbc.Container(
                html.P("Solver de Métodos Numéricos — Dash + Plotly", className="text-center text-muted"),
                fluid=True,
            )
        ),
    ],
    fluid=True,
    className="dbc",
)

if __name__ == "__main__":
    app.run(debug=True)
