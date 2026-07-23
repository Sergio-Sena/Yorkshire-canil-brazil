"""
conftest.py — Configuração global do pytest
"""

import sys
import os

# Garante que os módulos Lambda estão no path para todos os testes
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lambda"))
