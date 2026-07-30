from datetime import datetime
from zoneinfo import ZoneInfo

from providers.senamhi.collector import SenamhiProvider
from storage.json_storage import JsonStorage
from utils.logger import logger


def main() -> None:
    logger.info("Iniciando recolección de datos")

    storage = JsonStorage()
    provider = SenamhiProvider()

    results = provider.run_all()
    run_at = datetime.now(ZoneInfo("America/La_Paz"))

    for name, result in results.items():
        if result["success"]:
            storage.save(provider_name="senamhi", endpoint=name, data=result["data"], run_at=run_at)
        else:
            logger.error("Error en %s: %s", name, result.get("error"))

    logger.info("Recolección finalizada")


if __name__ == "__main__":
    main()
