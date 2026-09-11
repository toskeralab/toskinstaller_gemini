# -*- coding: utf-8 -*-
"""
TOSKINSTALLER - Módulo de Inspeção de Projetos e Dependências
ToskeraLAB ART/TECH House
"""

import os
import sys
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple

class ProjectAnalyzer:
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)

    def detect_language(self) -> Tuple[str, str]:
        """Identifica a linguagem e sugere o compilador ideal."""
        if not self.project_path.exists():
            return "Desconhecido", "Nenhum"

        files = [f.name.lower() for f in self.project_path.rglob("*") if f.is_file()]
        
        # Análise Python
        if any(f.endswith(".py") for f in files):
            main_candidates = ["main.py", "app.py", "cli.py", "index.py"]
            found_main = None
            for cand in main_candidates:
                if (self.project_path / cand).exists():
                    found_main = cand
                    break
            return "Python", "PyInstaller"
        
        # Análise Node.js
        if "package.json" in files or any(f.endswith(".js") for f in files):
            return "Node.js", "pkg"

        return "C#/C++ ou Outro", "Generico"

    def check_virtualenv(self) -> Tuple[bool, str]:
        """Detecta se existe uma venv criada na pasta do projeto."""
        venv_dirs = ["venv", ".venv", "env", ".env"]
        for venv in venv_dirs:
            venv_path = self.project_path / venv
            if venv_path.exists() and venv_path.is_dir():
                return True, str(venv_path)
        return False, ""

    def inspect_dependencies(self) -> List[str]:
        """Mapeia dependências a partir do requirements.txt ou imports do projeto."""
        req_file = self.project_path / "requirements.txt"
        deps = []
        if req_file.exists():
            with open(req_file, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        deps.append(line)
        return deps

    def install_requirements(self, venv_path: str = None) -> Tuple[bool, str]:
        """Instala os pacotes do requirements.txt no ambiente."""
        req_file = self.project_path / "requirements.txt"
        if not req_file.exists():
            return False, "requirements.txt não encontrado para instalação."

        pip_cmd = [sys.executable, "-m", "pip", "install", "-r", str(req_file)]
        if venv_path:
            # Aponta para o pip da venv se existir
            pip_exe = Path(venv_path) / "Scripts" / "pip.exe"
            if pip_exe.exists():
                pip_cmd = [str(pip_exe), "install", "-r", str(req_file)]

        try:
            res = subprocess.run(pip_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if res.returncode == 0:
                return True, "Dependências instaladas com sucesso no ambiente."
            return False, f"Erro ao instalar dependências: {res.stderr}"
        except Exception as e:
            return False, str(e)
