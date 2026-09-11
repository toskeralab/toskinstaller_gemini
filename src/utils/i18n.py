# -*- coding: utf-8 -*-
"""
TOSKINSTALLER - Módulo de Internacionalização (PT-BR e EN)
ToskeraLAB ART/TECH House
"""

TRANSLATIONS = {
    "PT-BR": {
        "app_title": "TOSKINSTALLER v1.0.0 — ToskeraLAB ART/TECH House",
        "step1_title": "Etapa 1: Análise e Conversão para Executável",
        "step2_title": "Etapa 2: Configuração e Empacotamento do Setup",
        "select_project_dir": "Selecionar Pasta do Projeto:",
        "browse": "Procurar...",
        "detect_lang": "Linguagem Detectada:",
        "compiler_tool": "Compilador Escolhido:",
        "check_tools": "Verificar Ferramentas",
        "install_guide_title": "Guia de Instalação de Ferramenta Faltante",
        "btn_convert": "Converter Projeto em Executável (.EXE)",
        "logs_label": "Logs do Processo em Tempo Real:",
        "pkg_format": "Formato do Pacote Final:",
        "delivery_mode": "Modo de Entrega do App:",
        "theme_choice": "Tema do Setup Wizard:",
        "anim_choice": "Animação da Porcentagem:",
        "partner_apps": "Apps Parceiros Opcionais (Separados por vírgula):",
        "partner_help": "Instaladores (.exe/msi) que rodam ao final da instalação principal.",
        "sign_pkg": "Assinar Pacote Digitalmente (.pfx):",
        "cert_path": "Caminho do Certificado:",
        "cert_pass": "Senha do Certificado:",
        "arch_choice": "Arquitetura Alvo:",
        "shortcuts": "Criar Atalhos:",
        "desktop_shortcut": "Área de Trabalho",
        "start_menu_shortcut": "Menu Iniciar",
        "app_name": "Nome da Aplicação:",
        "app_version": "Versão do App:",
        "publisher": "Desenvolvedor / Empresa:",
        "license_file": "Arquivo de Licença (.txt):",
        "btn_build_package": "Gerar Pacote Final",
        "build_success": "Pacote gerado com sucesso em:",
        "missing_tool_warn": "A ferramenta necessária não foi encontrada no sistema.",
        "install_pip_cmd": "Execute o comando abaixo no terminal:",
        "venv_detected": "Ambiente Virtual (VENV) detectado no projeto.",
        "venv_missing": "Nenhum VENV encontrado. Dependências globais serão mapeadas.",
        "install_deps_prompt": "Deseja instalar dependências mapeadas antes de compilar?",
    },
    "EN": {
        "app_title": "TOSKINSTALLER v1.0.0 — ToskeraLAB ART/TECH House",
        "step1_title": "Step 1: Analysis & Executable Conversion",
        "step2_title": "Step 2: Setup Configuration & Packaging",
        "select_project_dir": "Select Project Folder:",
        "browse": "Browse...",
        "detect_lang": "Detected Language:",
        "compiler_tool": "Selected Compiler:",
        "check_tools": "Check Tools",
        "install_guide_title": "Missing Tool Installation Guide",
        "btn_convert": "Convert Project to Executable (.EXE)",
        "logs_label": "Real-time Execution Logs:",
        "pkg_format": "Final Package Format:",
        "delivery_mode": "App Delivery Mode:",
        "theme_choice": "Setup Wizard Theme:",
        "anim_choice": "Percentage Animation Style:",
        "partner_apps": "Optional Partner Apps (Comma separated):",
        "partner_help": "Installers (.exe/msi) executed after main app installation.",
        "sign_pkg": "Digitally Sign Package (.pfx):",
        "cert_path": "Certificate Path:",
        "cert_pass": "Certificate Password:",
        "arch_choice": "Target Architecture:",
        "shortcuts": "Create Shortcuts:",
        "desktop_shortcut": "Desktop",
        "start_menu_shortcut": "Start Menu",
        "app_name": "Application Name:",
        "app_version": "App Version:",
        "publisher": "Publisher / Company:",
        "license_file": "License File (.txt):",
        "btn_build_package": "Generate Final Package",
        "build_success": "Package successfully created at:",
        "missing_tool_warn": "The required compilation tool was not found on your system.",
        "install_pip_cmd": "Run the following command in your terminal:",
        "venv_detected": "Virtual Environment (VENV) detected in project.",
        "venv_missing": "No VENV found. Global dependencies will be inspected.",
        "install_deps_prompt": "Do you want to install mapped dependencies before compiling?",
    }
}

class I18n:
    def __init__(self, lang="PT-BR"):
        self.lang = lang

    def set_lang(self, lang):
        if lang in TRANSLATIONS:
            self.lang = lang

    def get(self, key):
        return TRANSLATIONS.get(self.lang, {}).get(key, key)
