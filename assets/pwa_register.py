"""
Componente para registrar Service Worker (PWA) no Dash
"""

from dash import html, dcc

PWA_REGISTER = html.Div([
    # Service Worker
    dcc.Markdown("""
    <script>
    if ('serviceWorker' in navigator) {
        window.addEventListener('load', function() {
            navigator.serviceWorker.register('/sw.js').then(function(registration) {
                console.log('ServiceWorker registrado:', registration.scope);
            }, function(err) {
                console.log('ServiceWorker falhou:', err);
            });
        });
    }
    </script>
    """, dangerously_allow_html=True),

    # Meta tags para PWA mobile
    html.Meta(name="mobile-web-app-capable", content="yes"),
    html.Meta(name="apple-mobile-web-app-capable", content="yes"),
    html.Meta(name="apple-mobile-web-app-status-bar-style", content="black-translucent"),
    html.Meta(name="apple-mobile-web-app-title", content="NumerPy"),
    html.Link(rel="manifest", href="/assets/manifest.json"),
    html.Link(rel="apple-touch-icon", href="/assets/icon-192.png"),
])
