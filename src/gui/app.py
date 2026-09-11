# -*- coding: utf-8 -*-
"""
TOSKINSTALLER - Interface Gráfica Principal (CustomTkinter)
ToskeraLAB ART/TECH House
"""

import os
import sys
import threading
import customtkinter as ctk
from tkinter import filedialog, messagebox

from src.utils.i18n import I18n
from src.utils.sys_check import SystemChecker
from src.core.analyzer import ProjectAnalyzer
from src.core.compiler_wrapper import CompilerWrapper
from src.core.config_model import SetupConfig
from src.core.packager import PackageBuilder

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class ToskinstallerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.i18n = I18n("PT-BR")
        self.config = SetupConfig()

        self.title(self.i18n.get("app_title"))
        self.geometry("980x700")
        self.minsize(900, 650)

        self.compiled_dist_dir = None

        self.build_ui()

    def build_ui(self):
        # Top Bar (Idioma e Logo da Marca)
        top_bar = ctk.CTkFrame(self, height=45, corner_radius=0)
        top_bar.pack(fill="x", side="top")

        lbl_brand = ctk.CTkLabel(top_bar, text="🚀 TOSKINSTALLER — ToskeraLAB ART/TECH House", font=ctk.CTkFont(size=14, weight="bold"))
        lbl_brand.pack(side="left", padx=15)

        self.lang_var = ctk.StringVar(value="PT-BR")
        lang_switch = ctk.CTkOptionMenu(top_bar, values=["PT-BR", "EN"], variable=self.lang_var, command=self.change_language, width=90)
        lang_switch.pack(side="right", padx=15, pady=8)

        # Tabview (Etapa 1 e Etapa 2)
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=15, pady=10)

        self.tab_step1 = self.tabview.add(self.i18n.get("step1_title"))
        self.tab_step2 = self.tabview.add(self.i18n.get("step2_title"))

        self.setup_step1_ui()
        self.setup_step2_ui()

    def change_language(self, new_lang):
        self.i18n.set_lang(new_lang)
        self.title(self.i18n.get("app_title"))

    # --- ETAPA 1 UI ---
    def setup_step1_ui(self):
        # Seleção de Projeto
        frame_project = ctk.CTkFrame(self.tab_step1)
        frame_project.pack(fill="x", padx=15, pady=10)

        lbl_proj = ctk.CTkLabel(frame_project, text=self.i18n.get("select_project_dir"))
        lbl_proj.pack(side="left", padx=10, pady=10)

        self.entry_proj_path = ctk.CTkEntry(frame_project, placeholder_text="C:\\caminho\\para\\seu\\projeto", width=450)
        self.entry_proj_path.pack(side="left", padx=10, expand=True, fill="x")

        btn_browse = ctk.CTkButton(frame_project, text=self.i18n.get("browse"), command=self.browse_project)
        btn_browse.pack(side="right", padx=10)

        # Detecção e Ferramentas
        frame_info = ctk.CTkFrame(self.tab_step1)
        frame_info.pack(fill="x", padx=15, pady=5)

        self.lbl_lang_detected = ctk.CTkLabel(frame_info, text=f"{self.i18n.get('detect_lang')} ---")
        self.lbl_lang_detected.pack(side="left", padx=15, pady=10)

        self.compiler_option = ctk.CTkOptionMenu(frame_info, values=["PyInstaller", "Nuitka", "cx_Freeze"])
        self.compiler_option.pack(side="right", padx=15)

        lbl_comp = ctk.CTkLabel(frame_info, text=self.i18n.get("compiler_tool"))
        lbl_comp.pack(side="right", padx=5)

        # Botão de Ação Etapa 1
        btn_convert = ctk.CTkButton(self.tab_step1, text=self.i18n.get("btn_convert"), font=ctk.CTkFont(size=14, weight="bold"), fg_color="#10b981", hover_color="#059669", command=self.start_conversion_thread)
        btn_convert.pack(fill="x", padx=15, pady=10)

        # Log Box
        lbl_logs = ctk.CTkLabel(self.tab_step1, text=self.i18n.get("logs_label"))
        lbl_logs.pack(anchor="w", padx=15)

        self.txt_logs = ctk.CTkTextbox(self.tab_step1, font=ctk.CTkFont(family="Consolas", size=11))
        self.txt_logs.pack(fill="both", expand=True, padx=15, pady=(5, 15))

    def browse_project(self):
        path = filedialog.askdirectory()
        if path:
            self.entry_proj_path.delete(0, "end")
            self.entry_proj_path.insert(0, path)
            
            analyzer = ProjectAnalyzer(path)
            lang, suggested_compiler = analyzer.detect_language()
            self.lbl_lang_detected.configure(text=f"{self.i18n.get('detect_lang')} {lang}")
            self.compiler_option.set(suggested_compiler)

            # Verifica se ferramentas estão instaladas
            if not SystemChecker.is_tool_installed(suggested_compiler.lower()):
                info = SystemChecker.get_installation_instructions(suggested_compiler)
                messagebox.showwarning(
                    self.i18n.get("install_guide_title"),
                    f"{self.i18n.get('missing_tool_warn')}\n\n{info['desc']}\n\n{self.i18n.get('install_pip_cmd')}\n{info['cmd']}"
                )

    def append_log(self, text: str):
        self.txt_logs.insert("end", text + "\n")
        self.txt_logs.see("end")

    def start_conversion_thread(self):
        proj_dir = self.entry_proj_path.get()
        if not proj_dir or not os.path.exists(proj_dir):
            messagebox.showerror("Erro", "Selecione uma pasta de projeto válida.")
            return

        threading.Thread(target=self.run_conversion, daemon=True).start()

    def run_conversion(self):
        proj_dir = self.entry_proj_path.get()
        compiler = self.compiler_option.get()

        self.append_log(f"--- INICIANDO ETAPA 1 PARA: {proj_dir} ---")
        
        output_dist = os.path.join(proj_dir, "dist_toskinstaller")
        wrapper = CompilerWrapper(proj_dir, compiler, self.append_log)
        success = wrapper.build_executable(output_dist)

        if success:
            self.compiled_dist_dir = output_dist
            self.append_log("\n[SUCESSO] Etapa 1 concluída com êxito! Avance para a Etapa 2.")
            messagebox.showinfo("Sucesso", "Conversão concluída! Aponte para a Etapa 2 para customizar e gerar o instalador.")
            self.tabview.set(self.i18n.get("step2_title"))

    # --- ETAPA 2 UI ---
    def setup_step2_ui(self):
        scroll_frame = ctk.CTkScrollableFrame(self.tab_step2)
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Informações Básicas
        f1 = ctk.CTkFrame(scroll_frame)
        f1.pack(fill="x", pady=5)
        
        ctk.CTkLabel(f1, text=self.i18n.get("app_name")).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.entry_app_name = ctk.CTkEntry(f1, width=200)
        self.entry_app_name.insert(0, "MeuApp")
        self.entry_app_name.grid(row=0, column=1, padx=10, pady=5)

        ctk.CTkLabel(f1, text=self.i18n.get("app_version")).grid(row=0, column=2, padx=10, pady=5, sticky="w")
        self.entry_app_ver = ctk.CTkEntry(f1, width=120)
        self.entry_app_ver.insert(0, "1.0.0")
        self.entry_app_ver.grid(row=0, column=3, padx=10, pady=5)

        # Opções do Pacote
        f2 = ctk.CTkFrame(scroll_frame)
        f2.pack(fill="x", pady=5)

        ctk.CTkLabel(f2, text=self.i18n.get("pkg_format")).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.opt_pkg_format = ctk.CTkOptionMenu(f2, values=[".EXE Instalador", "Portable Extractor", ".MSI Instalador"])
        self.opt_pkg_format.grid(row=0, column=1, padx=10, pady=5)

        ctk.CTkLabel(f2, text=self.i18n.get("theme_choice")).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.opt_theme = ctk.CTkOptionMenu(f2, values=["Toskera Cyber", "Dark", "Light"])
        self.opt_theme.grid(row=1, column=1, padx=10, pady=5)

        ctk.CTkLabel(f2, text=self.i18n.get("anim_choice")).grid(row=1, column=2, padx=10, pady=5, sticky="w")
        self.opt_anim = ctk.CTkOptionMenu(f2, values=["Pulse Glow", "Smooth Bar", "Matrix Stepper"])
        self.opt_anim.grid(row=1, column=3, padx=10, pady=5)

        # Softwares Parceiros
        f3 = ctk.CTkFrame(scroll_frame)
        f3.pack(fill="x", pady=5)

        ctk.CTkLabel(f3, text=self.i18n.get("partner_apps")).pack(anchor="w", padx=10, pady=(5,0))
        self.entry_partners = ctk.CTkEntry(f3, placeholder_text="ex: vcredist_x64.exe, partner_setup.exe")
        self.entry_partners.pack(fill="x", padx=10, pady=5)

        # Botão de Gerar Pacote Final
        btn_build_final = ctk.CTkButton(scroll_frame, text=self.i18n.get("btn_build_package"), font=ctk.CTkFont(size=15, weight="bold"), fg_color="#3b82f6", hover_color="#2563eb", height=45, command=self.build_final_package)
        btn_build_final.pack(fill="x", pady=20)

    def build_final_package(self):
        if not self.compiled_dist_dir or not os.path.exists(self.compiled_dist_dir):
            messagebox.showerror("Erro", "Conclua a Etapa 1 antes de gerar o pacote final.")
            return

        self.config.app_name = self.entry_app_name.get()
        self.config.app_version = self.entry_app_ver.get()
        self.config.package_format = self.opt_pkg_format.get()
        self.config.theme = self.opt_theme.get()
        self.config.animation_style = self.opt_anim.get()
        
        partners_str = self.entry_partners.get()
        self.config.partner_apps = [p.strip() for p in partners_str.split(",") if p.strip()]

        out_dir = os.path.join(os.path.dirname(self.compiled_dist_dir), "output_packages")
        builder = PackageBuilder(self.compiled_dist_dir, self.config, out_dir)
        
        final_pkg = builder.build()
        messagebox.showinfo("Sucesso", f"{self.i18n.get('build_success')}\n{final_pkg}")

if __name__ == "__main__":
    app = ToskinstallerApp()
    app.mainloop()
