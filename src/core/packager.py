# -*- coding: utf-8 -*-
"""
TOSKINSTALLER - Motor de Empacotamento Final (.EXE, .MSI e Portable)
ToskeraLAB ART/TECH House
"""

import os
import sys
import shutil
import zipfile
import subprocess
from pathlib import Path
from src.core.config_model import SetupConfig
from src.utils.signer import CodeSigner

class PackageBuilder:
    def __init__(self, compiled_app_dir: str, config: SetupConfig, output_dir: str):
        self.compiled_app_dir = Path(compiled_app_dir)
        self.config = config
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def create_payload_zip(self, temp_dir: Path) -> Path:
        """Comprime o aplicativo compilado em um payload.zip."""
        zip_path = temp_dir / "payload.zip"
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(self.compiled_app_dir):
                for file in files:
                    full_path = Path(root) / file
                    arcname = full_path.relative_to(self.compiled_app_dir)
                    zipf.write(full_path, arcname)
        return zip_path

    def build(() -> str:
        """Gera o formato escolhido (.EXE Instalador, Portable ou .MSI)."""
        fmt = self.config.package_format
        temp_dir = self.output_dir / "_temp_packager"
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
        temp_dir.mkdir(parents=True)

        payload_zip = self.create_payload_zip(temp_dir)
        config_json = temp_dir / "installer_config.json"
        self.config.to_json(str(config_json))

        final_file = ""

        if "Portable" in fmt:
            # Portable Extractor: Zip de extração direta + executável de acionamento
            portable_name = f"{self.config.app_name}_v{self.config.app_version}_Portable.zip"
            final_file = str(self.output_dir / portable_name)
            shutil.copy(payload_zip, final_file)

        elif ".MSI" in fmt:
            # Geração de manifesto .WXS e invocação do WiX Toolset caso presente
            wxs_file = temp_dir / "setup.wxs"
            self._generate_wix_manifest(wxs_file)
            msi_name = f"{self.config.app_name}_v{self.config.app_version}_Setup.msi"
            final_file = str(self.output_dir / msi_name)
            
            # Tenta invocar o WiX v3/v4 se instalado
            res = subprocess.run(["wix", "build", str(wxs_file), "-o", final_file], capture_output=True)
            if res.returncode != 0:
                # Fallback: Copia pacote e gera instrução
                shutil.copy(payload_zip, self.output_dir / f"{self.config.app_name}_payload.zip")

        else: # Default: .EXE Instalador Wizard
            exe_name = f"{self.config.app_name}_v{self.config.app_version}_Setup.exe"
            final_file = str(self.output_dir / exe_name)

            # Empacota o runtime_stub + payload + config em um executável autônomo
            stub_script = Path(__file__).parent.parent / "runtime_stub" / "setup_runner.py"
            
            cmd = [
                sys.executable, "-m", "PyInstaller",
                "--noconfirm", "--onefile", "--windowed",
                f"--name={Path(final_file).stem}",
                f"--distpath={str(self.output_dir)}",
                f"--add-data={str(payload_zip)}:.",
                f"--add-data={str(config_json)}:.",
                str(stub_script)
            ]
            subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Aplica Assinatura Digital caso configurado
        if self.config.sign_package and self.config.cert_path and os.path.exists(final_file):
            CodeSigner.sign_executable(final_file, self.config.cert_path, self.config.cert_password)

        shutil.rmtree(temp_dir, ignore_errors=True)
        return final_file

    def _generate_wix_manifest(self, output_wxs: Path):
        """Gera manifesto WXS dinâmico para o WiX Toolset."""
        content = f"""<?xml version="1.0" encoding="UTF-8"?>
<Wix xmlns="http://wixtoolset.org/schemas/v4/wxs">
    <Package Name="{self.config.app_name}" Version="{self.config.app_version}" Manufacturer="{self.config.publisher}" UpgradeCode="{{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}}">
        <MajorUpgrade DowngradeErrorMessage="Uma versão mais recente já está instalada." />
        <MediaTemplate EmbedCab="yes" />
        <StandardDirectory Id="ProgramFilesFolder">
            <Directory Id="INSTALLFOLDER" Name="{self.config.app_name}" />
        </StandardDirectory>
    </Package>
</Wix>
"""
        with open(output_wxs, "w", encoding="utf-8") as f:
            f.write(content)
