import os
from pathlib import Path

TESTS_DIR = Path(__file__).parent
DATA_DIR = TESTS_DIR / "test_data"
RESUMES_DIR = DATA_DIR / "resumes"
RESUMES = {p.name: p for p in RESUMES_DIR.iterdir()}

GH_TOKEN = os.environ.get("GH_TOKEN", None)
