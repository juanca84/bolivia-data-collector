import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

SENAMHI_DIARIO_URL = os.getenv(
    "SENAMHI_DIARIO_URL",
    "https://senamhi.gob.bo/api/pronostico/diario",
)

SENAMHI_EDIARIO_URL = os.getenv(
    "SENAMHI_EDIARIO_URL",
    "https://senamhi.gob.bo/api/pronostico/ediario",
)

DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", "30"))
DEFAULT_RETRIES = int(os.getenv("DEFAULT_RETRIES", "3"))
