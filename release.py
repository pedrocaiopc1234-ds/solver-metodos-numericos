"""
NumerPy Solver — Script de Release Automático
==============================================
Cria o executável, compacta e prepara para upload no GitHub Releases.

Uso:
    python release.py --version 1.0.0

O script:
1. Roda o build com PyInstaller (detecta plataforma automaticamente)
2. Compacta o executável no formato adequado para cada OS
3. Prepara para upload no GitHub Releases

Formatos por plataforma:
- Windows: ZIP (.zip)
- Linux: tar.gz (.tar.gz)
- macOS: DMG (.dmg) ou ZIP (.zip)
"""

import os
import sys
import shutil
import zipfile
import tarfile
import argparse
import subprocess
import platform
from datetime import datetime

APP_NAME = "NumerPy Solver"
VERSION = None

# Detecta plataforma
PLATFORM = platform.system()  # Windows, Linux, Darwin


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


def create_zip(source_path, zip_path):
    """Cria arquivo ZIP. source_path pode ser uma pasta (--onedir) ou um arquivo (--onefile)."""
    print(f"Criando ZIP: {zip_path}")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        if os.path.isfile(source_path):
            # --onefile: adiciona apenas o exe
            arcname = os.path.basename(source_path)
            zipf.write(source_path, arcname)
        else:
            # --onedir: adiciona toda a pasta
            for root, dirs, files in os.walk(source_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, os.path.dirname(source_path))
                    zipf.write(file_path, arcname)
    print(f"ZIP criado: {os.path.abspath(zip_path)} ({os.path.getsize(zip_path) / 1024 / 1024:.2f} MB)")


def create_tarball(source_folder, tar_path):
    """Cria arquivo tar.gz com o conteúdo da pasta (Linux)."""
    print(f"Criando tar.gz: {tar_path}")
    with tarfile.open(tar_path, 'w:gz') as tarf:
        for root, dirs, files in os.walk(source_folder):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, os.path.dirname(source_folder))
                tarf.add(file_path, arcname)
    print(f"tar.gz criado: {os.path.abspath(tar_path)} ({os.path.getsize(tar_path) / 1024 / 1024:.2f} MB)")


def create_dmg(source_folder, dmg_path):
    """Cria arquivo DMG (macOS)."""
    print(f"Criando DMG: {dmg_path}")
    # Usa hdiutil no macOS
    result = subprocess.run([
        'hdiutil', 'create',
        '-volname', APP_NAME,
        '-srcfolder', source_folder,
        '-ov',
        '-format', 'UDZO',
        dmg_path
    ], check=False)
    if result.returncode == 0:
        print(f"DMG criado: {os.path.abspath(dmg_path)} ({os.path.getsize(dmg_path) / 1024 / 1024:.2f} MB)")
    else:
        print(f"ERRO ao criar DMG. Fallback para ZIP...")
        # Fallback para ZIP se DMG falhar
        zip_path = dmg_path.replace('.dmg', '.zip')
        create_zip(source_folder, zip_path)
        return zip_path
    return dmg_path


def main():
    parser = argparse.ArgumentParser(description="Cria release do NumerPy Solver")
    parser.add_argument("--version", required=True, help="Versão da release (ex: 1.0.0)")
    parser.add_argument("--skip-build", action="store_true", help="Pula etapa de build")
    args = parser.parse_args()

    global VERSION
    VERSION = args.version

    print("=" * 60)
    print(f"  NumerPy Solver — Release {VERSION}")
    print(f"  Plataforma: {PLATFORM}")
    print("=" * 60)

    # Pastas
    build_folder = "build"
    dist_folder = "dist"
    releases_folder = "releases"

    # Detecta saída: --onefile gera exe direto em dist/, --onedir gera pasta
    onefile_exe = os.path.join(dist_folder, f"{APP_NAME}.exe" if PLATFORM == "Windows" else APP_NAME)
    onedir_folder = os.path.join(dist_folder, APP_NAME)

    if os.path.isfile(onefile_exe):
        exe_source = onefile_exe
        print(f"Modo: --onefile (exe único)")
    elif os.path.isdir(onedir_folder):
        exe_source = onedir_folder
        print(f"Modo: --onedir (pasta)")
    else:
        print(f"ERRO: Nenhum executável encontrado em {dist_folder}")
        sys.exit(1)

    # Define nome do arquivo baseado na plataforma
    if PLATFORM == "Windows":
        archive_filename = f"NumerPy-Solver-v{VERSION}-windows.zip"
    elif PLATFORM == "Linux":
        archive_filename = f"NumerPy-Solver-v{VERSION}-linux.tar.gz"
    elif PLATFORM == "Darwin":
        archive_filename = f"NumerPy-Solver-v{VERSION}-macos.dmg"
    else:
        archive_filename = f"NumerPy-Solver-v{VERSION}.zip"

    archive_path = os.path.join(dist_folder, archive_filename)

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

    # Step 2: Re-detecta após build
    if os.path.isfile(onefile_exe):
        exe_source = onefile_exe
    elif os.path.isdir(onedir_folder):
        exe_source = onedir_folder
    else:
        print(f"ERRO: Nenhum executável encontrado em {dist_folder}")
        sys.exit(1)
    print(f"Executável encontrado: {exe_source}")

    # Step 3: Criar arquivo compactado
    print("\n[3/4] Criando arquivo compactado...")
    if PLATFORM == "Windows":
        create_zip(exe_source, archive_path)
    elif PLATFORM == "Linux":
        create_tarball(exe_source, archive_path)
    elif PLATFORM == "Darwin":
        archive_path = create_dmg(exe_source, archive_path)

    # Step 4: Copiar para pasta releases
    print("\n[4/4] Copiando para pasta releases...")
    release_archive = os.path.join(releases_folder, archive_filename)
    shutil.copy2(archive_path, release_archive)
    print(f"Release pronta: {os.path.abspath(release_archive)}")

    # Resumo
    print("\n" + "=" * 60)
    print("  RELEASE PRONTA!")
    print("=" * 60)
    print(f"\n  Arquivo: {os.path.abspath(release_archive)}")
    print(f"  Tamanho: {os.path.getsize(release_archive) / 1024 / 1024:.2f} MB")
    print("\n  Para publicar no GitHub:")
    print(f"    1. Acesse: https://github.com/pedrocaiopc1234-ds/solver-metodos-numericos/releases/new")
    print(f"    2. Crie uma nova tag: v{VERSION}")
    print(f"    3. Upload do arquivo: {archive_filename}")
    print(f"    4. Preencha as release notes")
    print(f"    5. Publique!")
    print("=" * 60)


if __name__ == "__main__":
    main()
