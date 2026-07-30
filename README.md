# Bolivia Data Collector

Plataforma automatizada para recolectar, versionar y almacenar datos públicos de Bolivia.

## Providers

| Provider | Endpoints |
|---|---|
| SENAMHI | diario, ediario |

## Datos

```
data/{provider}/
├── latest/{endpoint}.json                             # dato más reciente
└── history/{YYYY}/{MM}/{DD}/{HHMMSS}/{endpoint}.json  # solo si hay cambios

data/metrics/
└── metrics.json    # historial de ejecuciones
```

## Automatización

El workflow de GitHub Actions ejecuta `main.py` todos los días a las **05:00 Bolivia (09:00 UTC)**. Si hay cambios en `data/`, se commitean y pushean automáticamente con el mensaje `data: update`.

## Agregar un nuevo Provider

Ver [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Requisitos

- Python 3.13+
- `httpx`

## Licencia

MIT
