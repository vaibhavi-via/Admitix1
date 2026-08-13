import os
import sys
from pathlib import Path

BACKEND = Path(__file__).resolve().parents[1]
ROOT = BACKEND.parent
sys.path.insert(0, str(BACKEND))
sys.path.insert(0, str(ROOT))

from app.main import app

routes = {getattr(r, "path", None) for r in app.routes}
required = {
    "/ai/ocr",
    "/ai/document-verification",
    "/ai/cross-document-verification",
}
missing = required - routes
if missing:
    raise SystemExit(f"Missing AI routes: {sorted(missing)}")
print("AI routes OK:")
for route in sorted(required):
    print(route)
