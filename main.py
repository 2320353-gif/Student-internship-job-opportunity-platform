"""
Root entrypoint for FastAPI development.
Allows running `fastapi dev main.py` or `uvicorn main:app --reload`
directly from the project root directory as well as from the `backend` folder.
"""

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = ROOT_DIR / "backend"

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

# Import the FastAPI app from backend/main.py
import importlib.util

spec = importlib.util.spec_from_file_location("backend_main", BACKEND_DIR / "main.py")
backend_main = importlib.util.module_from_spec(spec)
sys.modules["backend_main"] = backend_main
spec.loader.exec_module(backend_main)

app = backend_main.app
