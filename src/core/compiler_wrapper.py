# -*- coding: utf-8 -*-
"""
TOSKINSTALLER - Executor de Compiladores Externos (PyInstaller, Nuitka, cx_Freeze)
ToskeraLAB ART/TECH House
"""

import os
import sys
import subprocess
import threading
from pathlib import Path
from typing import Callable, Optional

class CompilerWrapper:
    def __init__(self, project_path: str, compiler: str = "PyInstaller", log_callback: Optional[Callable[[str], None]] = None):
        self.project_path = Path(project_path)
        self.compiler = compiler
        self.log_callback = log_callback

    def _log(self, text: str):
        if self.log_callback:
            self.log_callback(text)
        else:
            print(text)

    def find_entry_point(self) -> Optional[Path]:
        candidates = ["main.py", "app.py", "index.py", "cli.py"]
        for c in candidates:
            p = self.project_path / c
            if p.exists():
                return p
        # Retorna o primeiro .py encontrado caso não ache padrão
        py_files = list(self.project_path.glob("*.py"))
        return py_files[0] if py_files else None

    def build_executable(self, output_dir: str) -> bool:
        """Executa a compilação do projeto em um processo separado e transmite os logs."""
        entry_point = self.find_entry_point()
        if not entry_point:
            self._log("[ERRO] Nenhum arquivo ponto de entrada (.py) foi encontrado no projeto.")
            return False

        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)

        cmd = []
        if self.compiler == "PyInstaller":
            cmd = [
                sys.executable, "-m", "PyInstaller",
                "--noconfirm", "--onedir", "--windowed",
                "--distpath", str(out_path),
                "--workpath", str(out_path / "build"),
                "--specpath", str(out_path),
                str(entry_point)
            ]
        elif self.compiler == "Nuitka":
            cmd = [
                sys.executable, "-m", "nuitka",
                "--standalone", "--plugin-enable=tk-inter",
                f"--output-dir={str(out_path)}",
                str(entry_point)
            ]
        elif self.compiler == "cx_Freeze":
            cmd = [
                sys.executable, "-m", "cx_Freeze",
                f"--target-dir={str(out_path)}",
                str(entry_point)
            ]
        else:
            self._log(f"[ERRO] Compilador '{self.compiler}' não suportado diretamente.")
            return False

        self._log(f"[INFO] Iniciando compilação do projeto usando {self.compiler}...")
        self._log(f"[CMD] {' '.join(cmd)}\n")

        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                cwd=str(self.project_path),
                bufsize=1
            )

            for line in iter(process.stdout.readline, ''):
                if line:
                    self._log(line.strip())

            process.stdout.close()
            return_code = process.wait()

            if return_code == 0:
                self._log("\n[SUCESSO] Compilação concluída com êxito!")
                return True
            else:
                self._log(f"\n[ERRO] Falha no processo de compilação. Código de retorno: {return_code}")
                return False

        except Exception as e:
            self._log(f"\n[EXCEÇÃO] Erro ao executar compilador: {str(e)}")
            return False
