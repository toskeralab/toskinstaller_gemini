# -*- coding: utf-8 -*-
"""
TOSKINSTALLER - Modelo de Configuração do Pacote do Instalador
ToskeraLAB ART/TECH House
"""

import json
from dataclasses import dataclass, asdict, field
from typing import List

@dataclass
class SetupConfig:
    app_name: str = "MeuAplicativo"
    app_version: str = "1.0.0"
    publisher: str = "ToskeraLAB ART/TECH House"
    package_format: str = ".EXE Instalador"  # .EXE Instalador, .MSI, Portable Extractor, Ambos
    delivery_mode: str = "Instalado no sistema"  # Instalado no sistema, Descompactado em pasta
    theme: str = "Toskera Cyber"  # Dark, Light, Toskera Cyber
    animation_style: str = "Pulse Glow"  # Smooth Bar, Pulse Glow, Matrix Stepper
    partner_apps: List[str] = field(default_factory=list)
    sign_package: bool = False
    cert_path: str = ""
    cert_password: str = ""
    architecture: str = "x64"
    desktop_shortcut: bool = True
    start_menu_shortcut: bool = True
    license_text: str = "Licença Padrão ToskeraLAB ART/TECH House."
    language: str = "PT-BR"

    def to_json(self, file_path: str):
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(asdict(self), f, indent=4, ensure_ascii=False)

    @classmethod
    def from_json(cls, file_path: str):
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return cls(**data)
