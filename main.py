# -*- coding: utf-8 -*-
"""
TOSKINSTALLER - Main Entrypoint
ToskeraLAB ART/TECH House
"""

import sys
import os

# Garante inclusão de diretórios no PATH de execução
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.gui.app import ToskinstallerApp

def main():
    app = ToskinstallerApp()
    app.mainloop()

if __name__ == "__main__":
    main()
