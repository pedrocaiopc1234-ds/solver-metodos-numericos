"""
NumerPy Solver — Aplicação Desktop com pywebview
================================================
Este script inicia o servidor Dash embutido e abre uma janela nativa
para a aplicação, funcionando como um app desktop sem necessidade de navegador.

Uso:
    python main.py
"""

import sys
import threading
import time
import webview

# Importa o servidor Dash
from app import server, app

# Configurações da aplicação
HOST = "127.0.0.1"
PORT = 8050
WIDTH = 1400
HEIGHT = 900
TITLE = "NumerPy Solver — Métodos Numéricos"


def start_server():
    """Inicia o servidor Flask/Dash em uma thread separada."""
    app.run(host=HOST, port=PORT, debug=False, use_reloader=False)


def create_app():
    """Cria e configura a janela do aplicativo."""
    # URL da aplicação
    url = f"http://{HOST}:{PORT}"

    # Configurações da janela
    window_kwargs = {
        "title": TITLE,
        "width": WIDTH,
        "height": HEIGHT,
        "min_size": (800, 600),
        "resizable": True,
        "fullscreen": False,
        "frameless": False,
        "easy_drag": True,
    }

    # Detecta sistema operacional para configurações específicas
    if sys.platform == "darwin":
        # macOS: configurações específicas
        window_kwargs["text_select"] = True
    elif sys.platform == "win32":
        # Windows: usa EdgeChromium (WebView2) se disponível
        window_kwargs["gui"] = "edgechromium"
    elif sys.platform == "linux":
        # Linux: tenta usar GTK WebKit
        pass

    # Cria a janela principal
    window = webview.create_window(url=url, **window_kwargs)

    # Inicia o pywebview
    webview.start(
        debug=False,  # True habilita DevTools (F12)
        http_server=True,
    )


def main():
    """Função principal que inicia o servidor e a aplicação."""
    print("=" * 60)
    print("  NumerPy Solver — Aplicação Desktop")
    print("=" * 60)
    print(f"\n  Iniciando servidor em http://{HOST}:{PORT}")
    print(f"  Tamanho da janela: {WIDTH}x{HEIGHT}")
    print("\n  Pressione Ctrl+C para sair.\n")
    print("-" * 60)

    # Inicia o servidor em uma thread separada
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    # Aguarda o servidor iniciar
    time.sleep(2)

    # Cria e inicia a aplicação
    create_app()


if __name__ == "__main__":
    main()
