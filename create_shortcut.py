"""
NumerPy Solver — Criar Atalho na Área de Trabalho
==================================================
Cria um atalho .lnk do app na área de trabalho do Windows.

Uso:
    python create_shortcut.py
"""

import os
import sys


def create_shortcut():
    exe_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dist", "NumerPy Solver", "NumerPy Solver.exe")
    icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "icon.ico")

    if not os.path.exists(exe_path):
        print(f"ERRO: Executável não encontrado em:\n  {exe_path}")
        print("\nVocê precisa rodar 'python build.py' primeiro.")
        sys.exit(1)

    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    shortcut_path = os.path.join(desktop, "NumerPy Solver.lnk")

    # Usa PowerShell para criar o atalho .lnk
    ps_script = f'''
$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("{shortcut_path}")
$Shortcut.TargetPath = "{exe_path}"
$Shortcut.WorkingDirectory = "{os.path.dirname(exe_path)}"
$Shortcut.IconLocation = "{icon_path}"
$Shortcut.Description = "NumerPy Solver — Métodos Numéricos"
$Shortcut.Save()
'''
    import subprocess
    subprocess.run(["powershell", "-Command", ps_script], check=True)

    print("=" * 60)
    print("  ATALHO CRIADO!")
    print("=" * 60)
    print(f"\n  Local: {shortcut_path}")
    print(f"  Ícone: {icon_path}")
    print("\n  Agora você pode abrir o app direto da área de trabalho!")
    print("=" * 60)


if __name__ == "__main__":
    create_shortcut()
