# toskinstaller_gemini
# TOSKINSTALLER

**Portable Windows app packager — turn any project into an installer or a portable executable.**

Developed by **ToskeraLAB ART/TECH House**

---

## What is TOSKINSTALLER?

TOSKINSTALLER is a portable Windows application that takes the files of a finished software project, converts it into a standalone executable, and packages it into a distributable final format — a traditional installer (`.EXE` / `.MSI`) or a portable decompressor.

It is both a **compiler wrapper** and a **packager**: the user drops in a project, TOSKINSTALLER detects the language, uses the appropriate external build tool to produce a `.exe`, and then wraps that `.exe` into a fully customizable Setup Wizard or portable package.

---

## What it does

TOSKINSTALLER performs two stages:

### Stage 1 — Project → Executable
- Accepts the raw files of a project (e.g. a Python project, or an AI-generated "vibe code" project).
- Automatically detects the project language.
- Selects and runs the correct external build tool (PyInstaller, Nuitka, cx_Freeze for Python; pkg, electron-builder for Node; and so on).
- If the required tool is not installed, TOSKINSTALLER guides the user step by step until it is ready, then continues.

### Stage 2 — Executable → Final Package
- Wraps the generated executable into the final distributable format chosen by the user:
  - `.EXE` installer
  - `.MSI` installer
  - Portable decompressor (extracts the app to a folder and produces an executable entry point)
- Lets the user fully customize the Setup Wizard before building:
  - Logo
  - License text
  - Animated banners
  - Optional installation of partner apps (installed separately, not bundled with the main app)
  - Color themes
  - Install progress animation (at least 3 styles)
  - Start Menu and Desktop shortcuts
  - Target folder and decompression options
  - Digital signature (optional)
  - Architecture and compatibility
  - PT-BR / EN localization

Every option above is **configurable at runtime** — nothing is hard-coded.

---

## What it delivers

- **TOSKINSTALLER itself**: a portable Windows executable, ideally distributed as a single file.
- **The final package**: a single executable when the chosen format allows it, containing only the user's app and the configured install/decompression resources. TOSKINSTALLER is **never** embedded into the generated package.

When the generated package runs on the end user's machine, it will either:
- Install the app on the system, or
- Open guided windows to choose a target folder, decompress the portable app, and create Start Menu / Desktop shortcuts, and
- Optionally install configured partner apps, separately from the main app.

---

## Key principles

- **Portable** — no installation required to run TOSKINSTALLER.
- **Offline-first** — works without an internet connection, except when it needs to guide the user through installing a required build tool.
- **Configurable** — every wizard page, theme, animation, and packaging option is chosen by the user at runtime.
- **Reproducible** — builds are deterministic and scriptable.
- **GitHub-ready** — organized repository structure, clear folder conventions, commit-friendly.

---

## Status

This project is part of an open comparison test between multiple code AIs. Each AI produces its own version of TOSKINSTALLER in its own public repository, so results can be compared side by side.

---

## Brand

**ToskeraLAB ART/TECH House**

---

## License

To be defined by ToskeraLAB ART/TECH House.

---
---

nir pela ToskeraLAB ART/TECH House.

# 🚀 TOSKINSTALLER

> **Desenvolvido por:** ToskeraLAB ART/TECH House  
> **Repositório:** `https://github.com/toskeralab/toskinstaller_gemini`

O **TOSKINSTALLER** é um aplicativo portátil para Windows projetado para automatizar a conversão de projetos de software (como projetos Python ou Vibe Coding) em executáveis standalone e empacotá-los em instaladores profissionais (.EXE com Setup Wizard, .MSI ou Extrator Portable).

---

## 🛠️ Como Compilar o TOSKINSTALLER em um Único Executável Portátil (.exe)

### Pré-requisitos (Windows)
* Python 3.10 ou superior instalado no Windows.
* Git instalado.

### Atalho de teclado para abrir o Prompt de Comando (CMD)
Windows (ou Windows + R) e digite “cmd” : Execute o Prompt de Comando no modo normal.
Win + X e pressione C : Execute o Prompt de Comando no modo normal. (Novo no Windows 10)
Win + X e pressione A : Execute o Prompt de Comando com privilégios administrativos. (Novo no Windows 10)
Alt + F4 (ou digite “sair” no prompt) : Fechar o Prompt de Comando.
Alt + Enter : Alterna entre o modo de tela inteira e janela.

### Passo a Passo de Compilação

### Passo a Passo de Compilação

**1. Clonar o Repositório:**
```cmd
git clone https://github.com/toskeralab/toskinstaller_gemini.git
cd toskinstaller_gemini
```

**2. Criar e Ativar Ambiente Virtual:**
```cmd
python -m venv venv
call venv\Scripts\activate
```

**3. Instalar Dependências:**
```cmd
pip install -r requirements.txt
```

**4. Gerar o Executável Portátil Único:**
```cmd
python build_portable.py
```

5. **Localização do Binário:**
O executável portátil standalone gerado estará pronto para uso na pasta:
dist/TOSKINSTALLER_Portable.exe

💻 Como Usar o TOSKINSTALLER
Abra o TOSKINSTALLER_Portable.exe.

Etapa 1: Selecione a pasta do seu projeto Python/Node, clique em Converter Projeto em Executável. Caso falte o PyInstaller ou Nuitka, o TOSKINSTALLER exibirá um guia de comando para instalação.

Etapa 2: Escolha o tema visual, o estilo da animação de porcentagem, atalhos, softwares parceiros e o formato final (.EXE, .MSI ou Portable).

Clique em Gerar Pacote Final para obter o seu instalador pronto para distribuição aos usuários finais.
