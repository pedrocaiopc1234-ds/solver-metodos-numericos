"""
NumerPy Solver — Aplicação Desktop com pywebview
=================================================
Este script inicia o servidor Dash embutido e abre uma janela nativa
para a aplicação, funcionando como um app desktop sem necessidade de navegador.

Uso:
    python main.py
"""

import sys
import os
import threading
import time

# PyInstaller freeze support (necessário para executáveis no Windows)
import multiprocessing
multiprocessing.freeze_support()


def get_resource_path(relative_path):
    """Retorna o caminho absoluto, funcionando no Python normal e no PyInstaller."""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


# Adiciona o diretório da aplicação ao sys.path (PyInstaller)
if hasattr(sys, "_MEIPASS"):
    sys.path.insert(0, sys._MEIPASS)

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
    url = f"http://{HOST}:{PORT}"

    # Aguarda o servidor Flask/Dash estar respondendo
    import urllib.request
    for _ in range(50):
        try:
            urllib.request.urlopen(url, timeout=0.2)
            break
        except Exception:
            time.sleep(0.1)
    else:
        print("AVISO: Servidor não respondeu a tempo. Abrindo janela mesmo assim...")

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

    if sys.platform == "darwin":
        window_kwargs["text_select"] = True

    webview.create_window(url=url, **window_kwargs)

    start_kwargs = {"debug": False}
    if sys.platform == "win32":
        start_kwargs["gui"] = "edgechromium"

    webview.start(**start_kwargs)


def main():
    """Função principal que inicia o servidor e a aplicação."""
    print("=" * 60)
    print("  NumerPy Solver — Aplicação Desktop")
    print("=" * 60)
    print(f"\n  Iniciando servidor em http://{HOST}:{PORT}")
    print(f"  Tamanho da janela: {WIDTH}x{HEIGHT}")
    print("\n  Pressione Ctrl+C para sair.\n")
    print("-" * 60)

    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    time.sleep(2)
    create_app()


if __name__ == "__main__":
    main()
