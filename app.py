"""
Numerical Methods Solver — Dash App
===================================
Run with:
    - python app.py (servidor web)
    - python main.py (app desktop com pywebview)

PWA: Acesse via navegador mobile e "Adicionar à Tela de Início"
"""

import dash
import dash_bootstrap_components as dbc
from dash import html, dcc

# Configuração para funcionar em modo app e web
app = dash.Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.DARKLY, dbc.icons.FONT_AWESOME],
    suppress_callback_exceptions=True,
    # Remove meta_tags duplicadas (já estão no index_string)
)

# Custom index para PWA
app.index_string = '''
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    {%metas%}
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <meta name="theme-color" content="#2C3E50">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="NumerPy">
    <link rel="manifest" href="/assets/manifest.json">
    <link rel="apple-touch-icon" href="/assets/icon-192.png">
    <title>{%title%}</title>
    {%favicon%}
    {%css%}
</head>
<body>
    {%app_entry%}
    <footer id="dash-footer">
        <script>
        // Registrar Service Worker para PWA
        if ('serviceWorker' in navigator) {
            window.addEventListener('load', function() {
                navigator.serviceWorker.register('/assets/sw.js').then(function(registration) {
                    console.log('ServiceWorker registrado:', registration.scope);
                }, function(err) {
                    console.log('ServiceWorker falhou:', err);
                });
            });
        }
        </script>
    </footer>
    {%config%}
    {%scripts%}
    {%renderer%}
</body>
</html>
'''

# Navbar responsiva
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Início", href="/")),
        dbc.NavItem(dbc.NavLink("Raízes", href="/raizes")),
        dbc.NavItem(dbc.NavLink("Sistemas", href="/sistemas-lineares")),
        dbc.NavItem(dbc.NavLink("Interpolação", href="/interpolacao")),
        dbc.NavItem(dbc.NavLink("Integração", href="/integracao")),
        dbc.NavItem(dbc.NavLink("EDOs", href="/edos")),
    ],
    brand="📊 NumerPy Solver",
    brand_href="/",
    color="primary",
    dark=True,
    fluid=True,
    className="mb-4",
    sticky="top",
)

app.layout = dbc.Container(
    [
        navbar,
        dash.page_container,
        html.Hr(className="my-4"),
        html.Footer(
            dbc.Container(
                html.P("© 2026 NumerPy Solver — Métodos Numéricos", className="text-center text-muted small"),
                fluid=True,
            ),
            className="py-3",
        ),
    ],
    fluid=True,
    className="dbc",
)

server = app.server  # Exporta o servidor WSGI para pywebview

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050, debug=True)
