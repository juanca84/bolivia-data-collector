import time

import httpx

from providers.base import ProviderBase
from providers.senamhi import diario, ediario
from utils.logger import logger


class SenamhiProvider(ProviderBase):

    def run_all(self) -> dict:
        logger.info("Ejecutando SENAMHI")

        results = {}

        with httpx.Client() as client:
            endpoints = [
                ("diario", diario.fetch),
                ("ediario", ediario.fetch),
            ]

            for name, fetch_fn in endpoints:
                start = time.perf_counter()
                try:
                    data = fetch_fn(client)
                    elapsed = (time.perf_counter() - start) * 1000
                    results[name] = {"success": True, "data": data, "duration_ms": elapsed}
                except Exception as e:
                    elapsed = (time.perf_counter() - start) * 1000
                    logger.error("Error en %s: %s", name, e)
                    results[name] = {"success": False, "error": str(e), "duration_ms": elapsed}

        return results
