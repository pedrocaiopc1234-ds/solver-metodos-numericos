"""
NumerPy Solver — Aplicação Desktop
===================================
Este script inicia o servidor Dash e abre uma janela nativa
usando pywebview (com fallback para navegador).

Uso:
    python main.py
"""

import sys
import os
import subprocess
import threading
import time
import webbrowser
import socket
import logging
import ctypes

# Fix CWD quando lançado via atalho/barra de tarefas —
# o Windows muda o diretório de trabalho para System32
if getattr(sys, 'frozen', False):
    os.chdir(os.path.dirname(sys.executable))

# PyInstaller freeze support
import multiprocessing
multiprocessing.freeze_support()


def unblock_dlls():
    """Remove Zone.Identifier (Mark of the Web) de DLLs no diretório do app.

    Windows marca arquivos baixados da internet com um fluxo alternativo
    'Zone.Identifier'. O .NET Framework se recusa a carregar DLLs com essa
    marca, causando o erro:
      RuntimeError: Failed to resolve Python.Runtime.Loader.Initialize

    Esta função remove essa marca de todos os arquivos no diretório do app
    quando executado a partir de um build PyInstaller.
    """
    if not hasattr(sys, "_MEIPASS"):
        return  # Só necessário no executável empacotado

    app_dir = sys._MEIPASS

    # Método 1: PowerShell Unblock-File (mais confiável)
    try:
        ps_cmd = (
            f'Get-ChildItem -Path "{app_dir}" -Recurse -File '
            f'| Unblock-File'
        )
        subprocess.run(
            ["powershell", "-Command", ps_cmd],
            capture_output=True,
            timeout=30,
        )
        log.info(f"Zone.Identifier removido de: {app_dir}")
        return
    except Exception:
        pass

    # Método 2: API do Windows via ctypes
    try:
        for root, _dirs, files in os.walk(app_dir):
            for fname in files:
                fpath = os.path.join(root, fname)
                try:
                    ctypes.windll.kernel32.DeleteFileW(
                        f"{fpath}:Zone.Identifier"
                    )
                except Exception:
                    pass
        log.info(f"Zone.Identifier removido (ctypes) de: {app_dir}")
    except Exception as e:
        log.warning(f"Não foi possível remover Zone.Identifier: {e}")


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
    # Remove Zone.Identifier antes de importar clr/pythonnet
    unblock_dlls()

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