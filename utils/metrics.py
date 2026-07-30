import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from utils.logger import logger


METRICS_DIR = Path("data") / "metrics"
METRICS_FILE = METRICS_DIR / "metrics.json"


class MetricsCollector:

    def __init__(self):
        self._entries: list[dict] = []

    def record_endpoint(
        self,
        provider: str,
        endpoint: str,
        duration_ms: float,
        size_bytes: int,
        changed: bool,
        success: bool,
    ) -> None:
        entry = {
            "timestamp": datetime.now(ZoneInfo("America/La_Paz")).isoformat(),
            "provider": provider,
            "endpoint": endpoint,
            "duration_ms": round(duration_ms, 1),
            "size_bytes": size_bytes,
            "changed": changed,
            "success": success,
        }
        self._entries.append(entry)

        logger.info(
            "%s/%s  %.1fs  %s  cambios: %s",
            provider,
            endpoint,
            duration_ms / 1000,
            _fmt_size(size_bytes),
            "sí" if changed else "no",
        )

    def save(self) -> None:
        METRICS_DIR.mkdir(parents=True, exist_ok=True)

        existing = []
        if METRICS_FILE.exists():
            existing = json.loads(METRICS_FILE.read_text(encoding="utf-8"))

        existing.extend(self._entries)

        METRICS_FILE.write_text(
            json.dumps(existing, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        logger.info("Métricas guardadas (%d ejecuciones)", len(existing))


def _fmt_size(bytes_: int) -> str:
    if bytes_ < 1024:
        return f"{bytes_}B"
    if bytes_ < 1024 * 1024:
        return f"{bytes_ / 1024:.0f}KB"
    return f"{bytes_ / (1024 * 1024):.1f}MB"
