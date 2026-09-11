# -*- coding: utf-8 -*-
"""
TOSKINSTALLER - Módulo de Assinatura Digital
ToskeraLAB ART/TECH House
"""

import os
import subprocess
from typing import Tuple

class CodeSigner:
    @staticmethod
    def sign_executable(file_path: str, cert_path: str, password: str = "") -> Tuple[bool, str]:
        """Assina digitalmente um executável usando signtool.exe no Windows."""
        if not os.path.exists(file_path):
            return False, "Arquivo a ser assinado não encontrado."
        if not os.path.exists(cert_path):
            return False, "Arquivo de certificado (.pfx) não encontrado."

        cmd = [
            "signtool", "sign", "/f", cert_path,
            "/fd", "SHA256",
            "/tr", "http://timestamp.digicert.com", "/td", "SHA256"
        ]
        if password:
            cmd.extend(["/p", password])
        cmd.append(file_path)

        try:
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if res.returncode == 0:
                return True, "Assinatura digital aplicada com sucesso!"
            else:
                return False, f"Falha ao assinar: {res.stderr or res.stdout}"
        except FileNotFoundError:
            return False, "O utilitário 'signtool.exe' não foi encontrado no PATH do sistema. Instale o Windows SDK."
        except Exception as e:
            return False, f"Erro inesperado durante assinatura: {str(e)}"
