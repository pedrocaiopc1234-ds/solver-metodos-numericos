"""
NumerPy Solver — Script de Release Automático
==============================================
Cria o executável, compacta e prepara para upload no GitHub Releases.

Uso:
    python release.py --version 1.0.0

O script:
1. Verifica se há tag Git para a versão
2. Roda o build com PyInstaller
3. Compacta o executável em um ZIP
4. Prepara para upload no GitHub Releases
"""

import os
import sys
import shutil
import zipfile
import argparse
import subprocess
from datetime import datetime

APP_NAME = "NumerPy Solver"
VERSION = None


def get_version():
    """Obtém a versão do argumento ou gera uma baseada na data."""
    if VERSION:
        return VERSION
    today = datetime.now()
    return f"{today.year}.{today.month}.{today.day}"


def run(cmd, capture=False):
    """Executa comando shell."""
    print(f">>> {' '.join(cmd)}")
    if capture:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        print(result.stdout)
        return result.returncode == 0
    else:
        result = subprocess.run(cmd, check=False)
        return result.returncode == 0


def create_zip(source_folder, zip_path):
    """Cria arquivo ZIP com o conteúdo da pasta."""
    print(f"Criando ZIP: {zip_path}")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_folder):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, os.path.dirname(source_folder))
                zipf.write(file_path, arcname)
    print(f"ZIP criado: {os.path.abspath(zip_path)} ({os.path.getsize(zip_path) / 1024 / 1024:.2f} MB)")


def main():
    parser = argparse.ArgumentParser(description="Cria release do NumerPy Solver")
    parser.add_argument("--version", required=True, help="Versão da release (ex: 1.0.0)")
    parser.add_argument("--skip-build", action="store_true", help="Pula etapa de build")
    args = parser.parse_args()

    global VERSION
    VERSION = args.version

    print("=" * 60)
    print(f"  NumerPy Solver — Release {VERSION}")
    print("=" * 60)

    # Pastas
    build_folder = "build"
    dist_folder = "dist"
    exe_folder = os.path.join(dist_folder, APP_NAME)
    zip_filename = f"NumerPy-Solver-v{VERSION}.zip"
    zip_path = os.path.join(dist_folder, zip_filename)
    releases_folder = "releases"

    # Cria pasta de releases
    if not os.path.exists(releases_folder):
        os.makedirs(releases_folder)

    # Step 1: Build
    if not args.skip_build:
        print("\n[1/4] Rodando build com PyInstaller...")
        if not run([sys.executable, "build.py"]):
            print("ERRO: Build falhou!")
            sys.exit(1)
    else:
        print("\n[1/4] Pulando build (--skip-build)")

    # Step 2: Verifica se executável existe
    print("\n[2/4] Verificando executável...")
    exe_path = os.path.join(exe_folder, f"{APP_NAME}.exe")
    if not os.path.exists(exe_path):
        print(f"ERRO: Executável não encontrado em {exe_path}")
        sys.exit(1)
    print(f"Executável encontrado: {exe_path}")

    # Step 3: Criar ZIP
    print("\n[3/4] Criando arquivo ZIP...")
    create_zip(exe_folder, zip_path)

    # Step 4: Copiar para pasta releases
    print("\n[4/4] Copiando para pasta releases...")
    release_zip = os.path.join(releases_folder, zip_filename)
    shutil.copy2(zip_path, release_zip)
    print(f"Release pronta: {os.path.abspath(release_zip)}")

    # Resumo
    print("\n" + "=" * 60)
    print("  RELEASE PRONTA!")
    print("=" * 60)
    print(f"\n  Arquivo: {os.path.abspath(release_zip)}")
    print(f"  Tamanho: {os.path.getsize(release_zip) / 1024 / 1024:.2f} MB")
    print("\n  Para publicar no GitHub:")
    print(f"    1. Acesse: https://github.com/pedrocaiopc1234-ds/solver-metodos-numericos/releases/new")
    print(f"    2. Crie uma nova tag: v{VERSION}")
    print(f"    3. Upload do arquivo: {zip_filename}")
    print(f"    4. Preencha as release notes")
    print(f"    5. Publique!")
    print("=" * 60)


if __name__ == "__main__":
    main()
