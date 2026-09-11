# -*- coding: utf-8 -*-
"""
TOSKINSTALLER - Compilação do TOSKINSTALLER em um Único Executável Portátil (.EXE)
ToskeraLAB ART/TECH House
"""

import os
import sys
import subprocess
from pathlib import Path

def build_portable_toskinstaller():
    root_dir = Path(__file__).parent.resolve()
    main_script = root_dir / "main.py"
    dist_dir = root_dir / "dist"

    print("==========================================================")
    print(" Compilando TOSKINSTALLER.exe Portátil (Single File)")
    print(" ToskeraLAB ART/TECH House")
    print("==========================================================")

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--clean",
        "--onefile",
        "--windowed",
        "--name=TOSKINSTALLER_Portable",
        f"--distpath={str(dist_dir)}",
        f"--add-data={str(root_dir / 'src')};src",
        str(main_script)
    ]

    print(f"\n[EXEC] {' '.join(cmd)}\n")
    res = subprocess.run(cmd)

    if res.returncode == 0:
        exe_path = dist_dir / "TOSKINSTALLER_Portable.exe"
        print("----------------------------------------------------------")
        print(f"[SUCESSO] Executável Portátil gerado com êxito!")
        print(f"Caminho do Arquivo: {exe_path}")
        print("----------------------------------------------------------")
    else:
        print("\n[ERRO] Falha na compilação do TOSKINSTALLER.")

if __name__ == "__main__":
    build_portable_toskinstaller()
