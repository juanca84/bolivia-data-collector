import httpx

from providers.senamhi import diario, ediario
from utils.logger import logger


class SenamhiProvider:

    def run_all(self) -> dict:
        logger.info("Ejecutando SENAMHI")

        results = {}

        with httpx.Client() as client:
            endpoints = [
                ("diario", diario.fetch),
                ("ediario", ediario.fetch),
            ]

            for name, fetch_fn in endpoints:
                try:
                    data = fetch_fn(client)
                    results[name] = {"success": True, "data": data}
                except Exception as e:
                    logger.error("Error en %s: %s", name, e)
                    results[name] = {"success": False, "error": str(e)}

        return results
