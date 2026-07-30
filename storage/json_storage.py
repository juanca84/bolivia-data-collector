import json
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path

from utils.logger import logger


BASE_DIR = Path("data")


class JsonStorage:

    def save(self, provider_name: str, endpoint: str, data: dict | list, run_at: datetime | None = None) -> bool:
        latest_dir = BASE_DIR / provider_name / "latest"
        latest_dir.mkdir(parents=True, exist_ok=True)
        latest_path = latest_dir / f"{endpoint}.json"

        old_data = self._load(latest_path)

        if old_data is not None and old_data == data:
            logger.info("Sin cambios en %s/%s", provider_name, endpoint)
            return False

        now = run_at or datetime.now(ZoneInfo("America/La_Paz"))
        history_path = (
            BASE_DIR
            / provider_name
            / "history"
            / f"{now.year}"
            / f"{now.month:02d}"
            / f"{now.day:02d}"
            / f"{now.hour:02d}{now.minute:02d}{now.second:02d}"
            / f"{endpoint}.json"
        )
        self._write(latest_path, data)
        self._write(history_path, data)
        logger.info("Guardado %s (nuevo historial)", latest_path)
        return True

    def _load(self, path: Path):
        if not path.exists():
            return None
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _write(self, path: Path, data: dict | list) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
