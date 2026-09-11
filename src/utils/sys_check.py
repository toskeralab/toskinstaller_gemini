# -*- coding: utf-8 -*-
"""
TOSKINSTALLER - Diagnóstico de Ferramentas e Guias Passo a Passo
ToskeraLAB ART/TECH House
"""

import shutil
import subprocess

class SystemChecker:
    @staticmethod
    def is_tool_installed(tool_name: str) -> bool:
        """Verifica se um executável ou módulo está disponível na CLI."""
        if shutil.which(tool_name):
            return True
        # Se for módulo Python (ex: pyinstaller, nuitka, cx_Freeze)
        try:
            res = subprocess.run(["python", "-m", tool_name, "--version"], 
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            return res.returncode == 0
        except Exception:
            return False

    @staticmethod
    def get_installation_instructions(tool_name: str) -> dict:
        """Retorna comandos e guia passo a passo para instalar a ferramenta faltante."""
        tool = tool_name.lower()
        if "pyinstaller" in tool:
            return {
                "name": "PyInstaller",
                "cmd": "pip install pyinstaller",
                "desc": "Ferramenta padrão rápida para conversão de código Python em binários standalone.",
                "url": "https://pyinstaller.org"
            }
        elif "nuitka" in tool:
            return {
                "name": "Nuitka",
                "cmd": "pip install nuitka",
                "desc": "Compilador Python para C que gera executáveis de altíssima performance.",
                "url": "https://nuitka.net"
            }
        elif "cx_freeze" in tool:
            return {
                "name": "cx_Freeze",
                "cmd": "pip install cx_Freeze",
                "desc": "Empacotador tradicional multiplataforma para Python.",
                "url": "https://marcelotduarte.github.io/cx_Freeze/"
            }
        elif "wix" in tool:
            return {
                "name": "WiX Toolset (para geração de .MSI)",
                "cmd": "dotnet tool install --global wix",
                "desc": "Requerido para compilar instalações padrão Microsoft Windows Installer (.MSI).",
                "url": "https://wixtoolset.org"
            }
        elif "pkg" in tool or "node" in tool:
            return {
                "name": "pkg (Node.js)",
                "cmd": "npm install -g pkg",
                "desc": "Converte projetos Node.js em executáveis autônomos.",
                "url": "https://github.com/vercel/pkg"
            }
        return {
            "name": tool_name,
            "cmd": f"pip install {tool_name}",
            "desc": "Dependência externa necessária.",
            "url": "https://pypi.org"
        }
