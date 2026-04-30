"""
NumerPy Solver — Build do Executável Desktop
=============================================
Cria um .exe standalone com PyInstaller.

Uso:
    python build.py

Requisitos:
    pip install pyinstaller

Saída:
    dist/NumerPy Solver/NumerPy Solver.exe
"""

import os
import sys
import shutil
import subprocess

APP_NAME = "NumerPy Solver"
ENTRY_POINT = "main.py"
ICON_PATH = os.path.join("assets", "icon.ico")


def run(cmd):
    print(f">>> {' '.join(cmd)}")
    result = subprocess.run(cmd, check=False)
    if result.returncode != 0:
        print(f"ERRO: comando falhou com código {result.returncode}")
        sys.exit(1)


def main():
    # Verifica se o ícone existe; se não, tenta gerar
    if not os.path.exists(ICON_PATH):
        print("Ícone não encontrado. Tentando gerar com create_icon.py...")
        subprocess.run([sys.executable, "create_icon.py"], check=False)

    # Limpa builds antigos
    for folder in ["build", "dist"]:
        if os.path.exists(folder):
            print(f"Removendo pasta antiga: {folder}")
            shutil.rmtree(folder)

    # Monta comando do PyInstaller
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--onedir",          # Pasta única (mais rápido que onefile)
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
    ]

    if os.path.exists(ICON_PATH):
        cmd += ["--icon", ICON_PATH]
    else:
        print("AVISO: Ícone não encontrado. O .exe usará o ícone padrão do Windows.")

    cmd.append(ENTRY_POINT)

    run(cmd)

    print("\n" + "=" * 60)
    print("  BUILD CONCLUÍDO!")
    print("=" * 60)
    exe_path = os.path.join("dist", APP_NAME, f"{APP_NAME}.exe")
    print(f"\n  Executável: {os.path.abspath(exe_path)}")
    print(f"  Pasta: {os.path.abspath(os.path.join('dist', APP_NAME))}")
    print("\n  Para criar um atalho na área de trabalho:")
    print(f"    1. Vá em: dist\\{APP_NAME}")
    print(f"    2. Clique com o botão direito em '{APP_NAME}.exe'")
    print(f"    3. Envie para > Área de Trabalho (criar atalho)")
    print("\n  Para distribuir: compacte a pasta inteira 'dist/" + APP_NAME + "'")
    print("=" * 60)


if __name__ == "__main__":
    main()
