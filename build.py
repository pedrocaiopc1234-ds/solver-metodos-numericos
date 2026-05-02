"""
NumerPy Solver — Build do Executável Desktop
=============================================
Cria um executável standalone com PyInstaller.

Uso:
    python build.py

Requisitos:
    pip install pyinstaller

Saída:
    dist/NumerPy Solver/NumerPy Solver.exe (Windows)
    dist/NumerPy Solver/NumerPy Solver (Linux)
    dist/NumerPy Solver/NumerPy Solver.app (macOS)
"""

import os
import sys
import shutil
import subprocess

APP_NAME = "NumerPy Solver"
ENTRY_POINT = "main.py"

# Detecta plataforma para ícone e nome do executável
if sys.platform == "win32":
    ICON_PATH = os.path.join("assets", "icon.ico")
    EXE_NAME = f"{APP_NAME}.exe"
elif sys.platform == "darwin":
    ICON_PATH = os.path.join("assets", "icon.icns") if os.path.exists(os.path.join("assets", "icon.icns")) else None
    EXE_NAME = APP_NAME
else:  # Linux
    ICON_PATH = os.path.join("assets", "icon.png") if os.path.exists(os.path.join("assets", "icon.png")) else None
    EXE_NAME = APP_NAME


def run(cmd):
    print(f">>> {' '.join(cmd)}")
    result = subprocess.run(cmd, check=False)
    if result.returncode != 0:
        print(f"ERRO: comando falhou com código {result.returncode}")
        sys.exit(1)


def main():
    # Verifica se o ícone existe; se não, tenta gerar
    if ICON_PATH and not os.path.exists(ICON_PATH):
        print(f"Ícone não encontrado: {ICON_PATH}")
        if sys.platform == "win32":
            print("Tentando gerar com create_icon.py...")
            subprocess.run([sys.executable, "create_icon.py"], check=False)

    # Limpa builds antigos (ignora erros de permissão no Windows)
    for folder in ["build", "dist"]:
        if os.path.exists(folder):
            print(f"Removendo pasta antiga: {folder}")
            try:
                shutil.rmtree(folder)
            except PermissionError:
                print(f"Aviso: Não foi possível remover {folder}. Tentando ignorar...")
                pass

    # Monta comando do PyInstaller
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--onefile",          # Exe único (funciona de qualquer lugar)
        "--windowed",        # Sem console
        "--clean",
        "--name", APP_NAME,
        "--add-data", f"assets{os.pathsep}assets",
        "--add-data", f"pages{os.pathsep}pages",
        "--add-data", f"core{os.pathsep}core",
        "--add-data", f"utils{os.pathsep}utils",
        "--add-data", f"validation{os.pathsep}validation",
        "--hidden-import", "dash",
        "--hidden-import", "dash_bootstrap_components",
        "--hidden-import", "dash.pages",
        "--hidden-import", "plotly",
        "--hidden-import", "plotly.graph_objects",
        "--hidden-import", "plotly.express",
        "--hidden-import", "numpy",
        "--hidden-import", "pandas",
        "--hidden-import", "core.roots",
        "--hidden-import", "core.linear_systems",
        "--hidden-import", "core.interpolation",
        "--hidden-import", "core.integration",
        "--hidden-import", "core.ode",
        "--hidden-import", "core.plot",
        "--hidden-import", "utils.dash_ui",
        "--hidden-import", "utils.ui",
        "--hidden-import", "validation.roots_validation",
        "--hidden-import", "validation.linear_systems_validation",
        "--hidden-import", "validation.interpolation_validation",
        "--hidden-import", "validation.integration_validation",
        "--hidden-import", "validation.ode_validation",
        "--hidden-import", "pages.home",
        "--hidden-import", "pages.1_raizes",
        "--hidden-import", "pages.2_sistemas_lineares",
        "--hidden-import", "pages.3_interpolacao",
        "--hidden-import", "pages.4_integracao",
        "--hidden-import", "pages.5_edo",
        "--hidden-import", "webview",
        "--hidden-import", "pkg_resources",
        # Hooks específicos para webview no Windows
        "--hidden-import", "webview.platforms",
        "--hidden-import", "webview.platforms.winforms",
        "--hidden-import", "webview.platforms.edgechromium",
        "--hidden-import", "webview.guilib",
        "--collect-all", "webview",
        # pythonnet + clr_loader são obrigatórios para pywebview no Windows
        "--hidden-import", "clr",
        "--hidden-import", "pythonnet",
        "--hidden-import", "clr_loader",
        "--hidden-import", "clr_loader.ffi",
        "--hidden-import", "clr_loader.util",
        "--collect-all", "pythonnet",
        "--collect-all", "clr_loader",
    ]

    if ICON_PATH and os.path.exists(ICON_PATH):
        cmd += ["--icon", ICON_PATH]
    else:
        if sys.platform == "win32":
            print("AVISO: Ícone não encontrado. O .exe usará o ícone padrão do Windows.")
        elif sys.platform == "darwin":
            print("AVISO: Ícone .icns não encontrado. Usando ícone padrão do macOS.")
        else:
            print("AVISO: Ícone PNG não encontrado. Usando ícone padrão no Linux.")

    cmd.append(ENTRY_POINT)

    run(cmd)

    print("\n" + "=" * 60)
    print("  BUILD CONCLUÍDO!")
    print("=" * 60)
    if sys.platform == "win32":
        exe_path = os.path.join("dist", f"{APP_NAME}.exe")
        print(f"\n  Executável: {os.path.abspath(exe_path)}")
        print("\n  Exe único (--onefile): pode ser copiado para qualquer lugar.")
        print("  Para distribuir: use python release.py --version X.Y.Z")
    elif sys.platform == "darwin":
        exe_path = os.path.join("dist", APP_NAME)
        print(f"\n  Executável: {os.path.abspath(exe_path)}")
        print("\n  Para usar:")
        print(f"    ./dist/{APP_NAME}")
    else:
        exe_path = os.path.join("dist", APP_NAME)
        print(f"\n  Executável: {os.path.abspath(exe_path)}")
        print("\n  Para usar:")
        print(f"    ./dist/{APP_NAME}")
    print("=" * 60)


if __name__ == "__main__":
    main()
