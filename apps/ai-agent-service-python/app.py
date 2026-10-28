"""Entrada da Vercel para o ai-agent-service. Mesmo app do uvicorn, com o src/ no caminho de importação."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from main import app  # noqa: E402,F401
