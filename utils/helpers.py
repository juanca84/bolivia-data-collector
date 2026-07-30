import time
from functools import wraps

from utils.logger import logger


def retry(max_attempts: int = 3, delay: float = 1.0):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        logger.warning("Intento %d/%d falló: %s — reintentando...", attempt, max_attempts, e)
                        time.sleep(delay)
            raise last_exc
        return wrapper
    return decorator
