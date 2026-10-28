"""Entrada serverless para a Vercel. Mesmo app do uvicorn, só muda o caminho de importação."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from main import app  # noqa: E402,F401
