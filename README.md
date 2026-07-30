# Bolivia Data Collector

Plataforma automatizada para recolectar, versionar y almacenar datos públicos de Bolivia.

## Providers

| Provider | Estado | Endpoints |
|---|---|---|
| SENAMHI | ✅ | diario, ediario |
| BCB | ❌ | — |
| INE | ❌ | — |
| SNIS | ❌ | — |

## Uso

```bash
python main.py
```

Los datos se guardan en `data/`:

```
data/{provider}/
├── latest/{endpoint}.json          # siempre el dato más reciente
└── history/{YYYY}/{MM}/{DD}/{HHMMSS}/{endpoint}.json  # solo cuando hay cambios
```

## Requisitos

- Python 3.13+
- `httpx`

## Licencia

MIT
