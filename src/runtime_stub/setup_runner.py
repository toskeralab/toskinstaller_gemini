# -*- coding: utf-8 -*-
"""
TOSKINSTALLER - Runtime Stub (Instalador Gerado Entregue ao Cliente Final)
ToskeraLAB ART/TECH House
Nota: Este arquivo roda de forma 100% autônoma no computador do cliente final.
"""

import os
import sys
import json
import zipfile
import shutil
import subprocess
import threading
import time
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

CONFIG_FILENAME = "installer_config.json"
PAYLOAD_FILENAME = "payload.zip"

class GeneratedSetupWizard:
    def __init__(self, root):
        self.root = root
        self.config = self.load_config()
        self.setup_ui()

    def load_config(self) -> dict:
        """Carrega a configuração embutida ou adjacente."""
        if os.path.exists(CONFIG_FILENAME):
            with open(CONFIG_FILENAME, "r", encoding="utf-8") as f:
                return json.load(f)
        return {
            "app_name": "Aplicativo Empacotado",
            "app_version": "1.0.0",
            "publisher": "ToskeraLAB ART/TECH House",
            "theme": "Toskera Cyber",
            "animation_style": "Pulse Glow",
            "license_text": "Termos de Uso e Licença de Software.",
            "desktop_shortcut": True,
            "start_menu_shortcut": True,
            "partner_apps": []
        }

    def setup_ui(self):
        self.root.title(f"Instalação — {self.config.get('app_name')} v{self.config.get('app_version')}")
        self.root.geometry("640x420")
        self.root.resizable(False, False)

        # Temas visuais
        theme = self.config.get("theme", "Toskera Cyber")
        if theme == "Toskera Cyber":
            self.bg_color = "#0f172a"
            self.fg_color = "#38bdf8"
            self.card_color = "#1e293b"
            self.text_color = "#f8fafc"
        elif theme == "Dark":
            self.bg_color = "#18181b"
            self.fg_color = "#a1a1aa"
            self.card_color = "#27272a"
            self.text_color = "#ffffff"
        else: # Light
            self.bg_color = "#f4f4f5"
            self.fg_color = "#2563eb"
            self.card_color = "#ffffff"
            self.text_color = "#09090b"

        self.root.configure(bg=self.bg_color)

        # Header
        header = tk.Frame(self.root, bg=self.card_color, height=60)
        header.pack(fill="x", side="top")
        
        lbl_title = tk.Label(header, text=self.config.get("app_name"), font=("Segoe UI", 16, "bold"), bg=self.card_color, fg=self.fg_color)
        lbl_title.pack(anchor="w", padx=20, pady=(10, 0))
        
        lbl_sub = tk.Label(header, text=f"Por: {self.config.get('publisher')}", font=("Segoe UI", 9), bg=self.card_color, fg=self.text_color)
        lbl_sub.pack(anchor="w", padx=20)

        # Main Body
        self.body = tk.Frame(self.root, bg=self.bg_color)
        self.body.pack(fill="both", expand=True, padx=20, pady=20)

        # Seleção de Destino
        lbl_dir = tk.Label(self.body, text="Escolha a pasta de destino para instalação:", font=("Segoe UI", 10), bg=self.bg_color, fg=self.text_color)
        lbl_dir.pack(anchor="w", pady=(0, 5))

        dir_frame = tk.Frame(self.body, bg=self.bg_color)
        dir_frame.pack(fill="x", pady=5)

        default_install_dir = os.path.join(os.environ.get("LOCALAPPDATA", "C:\\"), self.config.get("app_name"))
        self.target_dir_var = tk.StringVar(value=default_install_dir)

        entry_dir = tk.Entry(dir_frame, textvariable=self.target_dir_var, font=("Segoe UI", 10))
        entry_dir.pack(side="left", fill="x", expand=True, padx=(0, 10))

        btn_browse = tk.Button(dir_frame, text="Procurar...", command=self.browse_target_dir, bg=self.card_color, fg=self.text_color)
        btn_browse.pack(side="right")

        # Barra de Progresso
        self.progress = ttk.Progressbar(self.body, orient="horizontal", mode="determinate")
        self.progress.pack(fill="x", pady=20)

        self.lbl_status = tk.Label(self.body, text="Pronto para iniciar.", font=("Segoe UI", 9, "italic"), bg=self.bg_color, fg=self.text_color)
        self.lbl_status.pack(anchor="w")

        # Footer Buttons
        footer = tk.Frame(self.root, bg=self.card_color, height=50)
        footer.pack(fill="x", side="bottom")

        self.btn_install = tk.Button(footer, text="Instalar Agora", command=self.start_installation_thread, bg=self.fg_color, fg="#ffffff", font=("Segoe UI", 10, "bold"), padx=15, pady=5)
        self.btn_install.pack(side="right", padx=20, pady=10)

    def browse_target_dir(self):
        selected = filedialog.askdirectory()
        if selected:
            self.target_dir_var.set(selected)

    def start_installation_thread(self):
        self.btn_install.config(state="disabled")
        threading.Thread(target=self.run_installation, daemon=True).start()

    def run_installation(self):
        target = self.target_dir_var.get()
        os.makedirs(target, exist_ok=True)

        anim_style = self.config.get("animation_style", "Pulse Glow")

        # Animação e Descompactação
        self.lbl_status.config(text="Extraindo arquivos do payload...")
        
        if os.path.exists(PAYLOAD_FILENAME):
            with zipfile.ZipFile(PAYLOAD_FILENAME, 'r') as zip_ref:
                files = zip_ref.namelist()
                total = len(files)
                for idx, f in enumerate(files):
                    zip_ref.extract(f, target)
                    pct = int(((idx + 1) / total) * 80)
                    
                    if anim_style == "Pulse Glow":
                        self.lbl_status.config(text=f"Instalando: [{pct}%] — {f}")
                    elif anim_style == "Matrix Stepper":
                        self.lbl_status.config(text=f">> STEP {idx+1}/{total} | EXTRACTING: {f}")
                    else:
                        self.lbl_status.config(text=f"Copiando arquivos... {pct}%")

                    self.progress['value'] = pct
                    self.root.update_idletasks()
                    time.sleep(0.01)

        # Criação de Atalhos
        self.lbl_status.config(text="Configurando atalhos no sistema...")
        self.create_shortcuts(target)
        self.progress['value'] = 90

        # Apps Parceiros
        partners = self.config.get("partner_apps", [])
        if partners:
            self.lbl_status.config(text="Executando instaladores de softwares parceiros...")
            for p_app in partners:
                p_path = os.path.join(target, p_app)
                if os.path.exists(p_path):
                    subprocess.run([p_path, "/S"], shell=True)

        self.progress['value'] = 100
        self.lbl_status.config(text="Instalação concluída com sucesso!")
        messagebox.showinfo("Sucesso", f"{self.config.get('app_name')} foi instalado com êxito!")
        self.root.destroy()

    def create_shortcuts(self, install_dir: str):
        """Cria atalhos na Área de Trabalho e Menu Iniciar usando PowerShell nativo do Windows."""
        exe_files = [f for f in os.listdir(install_dir) if f.endswith(".exe")]
        if not exe_files:
            return
        target_exe = os.path.join(install_dir, exe_files[0])
        app_name = self.config.get("app_name", "App")

        # Shortcut Desktop
        if self.config.get("desktop_shortcut"):
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            shortcut_path = os.path.join(desktop, f"{app_name}.lnk")
            ps_cmd = f"$s=(New-Object -COM WScript.Shell).CreateShortcut('{shortcut_path}');$s.TargetPath='{target_exe}';$s.Save()"
            subprocess.run(["powershell", "-Command", ps_cmd], capture_output=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = GeneratedSetupWizard(root)
    root.mainloop()
