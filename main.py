"""
Root entrypoint for FastAPI development.
Allows running `uvicorn main:app --reload` or `fastapi dev main.py`
from the project root directory.
"""

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = ROOT_DIR / "backend"

for p in [str(ROOT_DIR), str(BACKEND_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)

from backend.main import app
