"""
NumerPy Solver — Aplicação Desktop
===================================
Este script inicia o servidor Dash e abre uma janela no navegador
ou em uma janela nativa usando pywebview.

Uso:
    python main.py
"""

import sys
import os
import threading
import time
import webbrowser
import socket
import logging

# PyInstaller freeze support
import multiprocessing
multiprocessing.freeze_support()

# Configuração de logging — funciona tanto em modo console quanto windowed
LOG_FILE = os.path.join(
    os.path.expanduser("~"), "NumerPy_Solver.log"
)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8", mode="w"),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger("NumerPy")


def get_resource_path(relative_path):
    """Retorna o caminho absoluto, funcionando no Python normal e no PyInstaller."""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


# Adiciona o diretório da aplicação ao sys.path (PyInstaller)
if hasattr(sys, "_MEIPASS"):
    sys.path.insert(0, sys._MEIPASS)

# Importa o servidor Dash
from app import server, app

# Configurações da aplicação
HOST = "127.0.0.1"
PORT = 8050
WIDTH = 1400
HEIGHT = 900
TITLE = "NumerPy Solver — Métodos Numéricos"


def is_port_available(port):
    """Verifica se a porta está disponível."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((HOST, port)) != 0


def start_server():
    """Inicia o servidor Flask/Dash em uma thread separada."""
    app.run(host=HOST, port=PORT, debug=False, use_reloader=False)


def wait_for_server(timeout=30):
    """Aguarda o servidor estar respondendo."""
    import urllib.request
    url = f"http://{HOST}:{PORT}"
    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            urllib.request.urlopen(url, timeout=1)
            return True
        except Exception:
            time.sleep(0.5)
    return False


def open_in_browser():
    """Abre o aplicativo no navegador padrão."""
    url = f"http://{HOST}:{PORT}"
    webbrowser.open(url)
    log.info(f"Aplicação aberta no navegador: {url}")
    log.info("Pressione Ctrl+C para parar o servidor.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        log.info("Fechando...")


def run_native_window():
    """Tenta criar janela nativa com pywebview."""
    try:
        import webview
    except ImportError as e:
        log.warning(f"pywebview não disponível ({e}). Usando navegador.")
        return False

    url = f"http://{HOST}:{PORT}"

    if not wait_for_server(timeout=15):
        log.error("Servidor não respondeu a tempo.")
        return False

    try:
        window = webview.create_window(
            title=TITLE,
            url=url,
            width=WIDTH,
            height=HEIGHT,
            min_size=(800, 600),
            resizable=True,
            fullscreen=False,
        )

        webview.start(debug=False)
        return True

    except Exception as e:
        log.error(f"Não foi possível criar janela nativa: {e}", exc_info=True)
        return False


def main():
    """Função principal que inicia o servidor e a aplicação."""
    log.info("=" * 60)
    log.info("  NumerPy Solver — Aplicação Desktop")
    log.info("=" * 60)
    log.info(f"Iniciando servidor em http://{HOST}:{PORT}")
    log.info(f"Tamanho da janela: {WIDTH}x{HEIGHT}")
    log.info(f"Log salvo em: {LOG_FILE}")

    # Inicia o servidor em thread separada
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    time.sleep(2)

    # Tenta janela nativa, fallback para navegador
    if not run_native_window():
        open_in_browser()


if __name__ == "__main__":
    main()
