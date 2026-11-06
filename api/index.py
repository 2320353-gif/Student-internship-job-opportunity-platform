"""
Vercel serverless function entrypoint for /api routes.
"""

import sys
from pathlib import Path

API_DIR = Path(__file__).resolve().parent
ROOT_DIR = API_DIR.parent
BACKEND_DIR = ROOT_DIR / "backend"

for p in [str(ROOT_DIR), str(BACKEND_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)

from backend.main import app
