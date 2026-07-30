# Cómo agregar un nuevo Provider

## 1. Crear la carpeta del provider

```
providers/<nombre>/
├── __init__.py  (vacío)
├── collector.py
├── diario.py
└── ediario.py
```

## 2. Crear cada endpoint

```python
from config.settings import DEFAULT_TIMEOUT
from utils.helpers import retry
from utils.logger import logger


@retry
def fetch(client) -> dict:
    logger.info("Descargando <nombre>")
    response = client.get("URL", timeout=DEFAULT_TIMEOUT)
    response.raise_for_status()
    data = response.json()
    if not data:
        raise ValueError("Respuesta vacía")
    return data
```

## 3. Crear collector.py

```python
import httpx
import time

from providers.base import ProviderBase
from providers.<nombre> import diario, ediario
from utils.logger import logger


class <Nombre>Provider(ProviderBase):

    def run_all(self) -> dict:
        logger.info("Ejecutando <NOMBRE>")
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
```

## 4. Registrar el provider

Editar `providers/__init__.py`:

```python
from providers.<nombre>.collector import <Nombre>Provider

PROVIDERS = {
    "senamhi": SenamhiProvider,
    "<nombre>": <Nombre>Provider,
}
```

## 5. (Opcional) Configurar URLs en settings.py

Si el provider necesita URLs o timeouts específicos, agregarlos en `config/settings.py`:

```python
<NOMBRE>_DIARIO_URL = os.getenv("<NOMBRE>_DIARIO_URL", "https://...")
<NOMBRE>_TIMEOUT = int(os.getenv("<NOMBRE>_TIMEOUT", "30"))
```

## Resultado

- `main.py` ejecuta automáticamente el nuevo provider
- El workflow de GitHub Actions lo incluye sin cambios
- Las métricas y el storage funcionan igual
