from pathlib import Path

TESTS_DIR = Path(__file__).parent
DATA_DIR = TESTS_DIR / "test_data"
RESUMES_DIR = DATA_DIR / "resumes"
RESUMES = list(RESUMES_DIR.iterdir())
