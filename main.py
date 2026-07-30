import json
from datetime import datetime
from zoneinfo import ZoneInfo

from providers import PROVIDERS
from storage.json_storage import JsonStorage
from utils.logger import logger
from utils.metrics import MetricsCollector


def main() -> None:
    logger.info("Iniciando recolección de datos")

    storage = JsonStorage()
    metrics = MetricsCollector()
    run_at = datetime.now(ZoneInfo("America/La_Paz"))

    for provider_name, provider_cls in PROVIDERS.items():
        logger.info("Ejecutando provider: %s", provider_name)
        provider = provider_cls()
        results = provider.run_all()

        for endpoint, result in results.items():
            if result["success"]:
                changed = storage.save(provider_name=provider_name, endpoint=endpoint, data=result["data"], run_at=run_at)
                size = len(json.dumps(result["data"]))
                metrics.record_endpoint(
                    provider=provider_name,
                    endpoint=endpoint,
                    duration_ms=result.get("duration_ms", 0),
                    size_bytes=size,
                    changed=changed,
                    success=True,
                )
            else:
                logger.error("Error en %s/%s: %s", provider_name, endpoint, result.get("error"))
                metrics.record_endpoint(
                    provider=provider_name,
                    endpoint=endpoint,
                    duration_ms=result.get("duration_ms", 0),
                    size_bytes=0,
                    changed=False,
                    success=False,
                )

    metrics.save()
    logger.info("Recolección finalizada")


if __name__ == "__main__":
    main()
