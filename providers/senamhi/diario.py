from config.settings import DEFAULT_RETRIES, DEFAULT_TIMEOUT, SENAMHI_DIARIO_URL
from utils.helpers import retry
from utils.logger import logger


@retry(max_attempts=DEFAULT_RETRIES)
def fetch(client) -> dict:
    logger.info("Descargando pronóstico diario")
    response = client.get(SENAMHI_DIARIO_URL, timeout=DEFAULT_TIMEOUT)
    response.raise_for_status()
    data = response.json()
    if not data:
        raise ValueError("Respuesta vacía")
    return data
