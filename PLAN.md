# Bolivia Data Collector

## Objetivo

Construir una plataforma automatizada para recolectar, versionar y almacenar datos públicos de Bolivia.

### Objetivos principales

- Consumir APIs públicas de Bolivia.
- Almacenar la respuesta original en formato JSON.
- Mantener un historial completo de cambios.
- Ejecutarse automáticamente mediante GitHub Actions.
- Diseñar una arquitectura escalable para soportar múltiples instituciones (Providers) y múltiples endpoints por institución.

---

# Arquitectura General

```text
GitHub Actions
        │
        ▼
main.py
        │
        ▼
┌──────────────────────────────┐
│ Ejecutar Providers           │
└──────────────────────────────┘
        │
        ▼
SENAMHI Provider
        │
        ├── diario
        ├── ediario
        ├── alertas (futuro)
        ├── estaciones (futuro)
        └── ...
        │
        ▼
Storage
        │
        ├── latest/
        └── history/
                │
                ▼
        Comparación de cambios
                │
        ┌───────┴────────┐
        │                │
   Sin cambios      Con cambios
        │                │
        │          Commit automático
        │
        ▼
      Finalizar
```

---

# Conceptos

## Provider

Un **Provider** representa una institución.

Ejemplos futuros:

- SENAMHI
- BCB
- INE
- SNIS

Cada Provider puede tener uno o varios endpoints.

---

## Endpoint

Cada endpoint conoce únicamente una URL.

Ejemplo para SENAMHI

- `/api/pronostico/diario`
- `/api/pronostico/ediario`

Cada endpoint es completamente independiente.

---

# Estructura del Proyecto

```text
bolivia-data-collector/

.github/
│
└── workflows/
    └── update.yml

config/
│
└── settings.py

providers/
│
├── base.py
│
└── senamhi/
    │
    ├── __init__.py
    ├── provider.py
    │
    └── endpoints/
        ├── diario.py
        └── ediario.py

storage/
│
├── writer.py
├── comparator.py
└── history.py

models/

utils/
│
└── helpers.py

logging/
│
└── logger.py

data/
│
└── senamhi/
    │
    ├── latest/
    │   ├── diario.json
    │   └── ediario.json
    │
    └── history/
        └── 2026/
            └── 07/
                └── 29/
                    └── 080000/
                        ├── diario.json
                        └── ediario.json

tests/

main.py

requirements.txt

README.md
```

---

# Responsabilidades

## main.py

Responsabilidades

- Ejecutar todos los Providers.
- Coordinar el flujo.
- Registrar el resultado general.

No debe conocer detalles internos de ninguna API.

---

## Provider

Responsabilidades

- Coordinar todos sus endpoints.
- Ejecutarlos.
- Consolidar resultados.
- Entregar los datos al módulo Storage.

No debe guardar archivos.

---

## Endpoint

Responsabilidades

- Consumir una URL.
- Validar HTTP.
- Validar JSON.
- Retornar los datos.

Cada endpoint debe ser independiente.

---

## Storage

Responsabilidades

- Guardar JSON.
- Comparar cambios.
- Actualizar latest.
- Crear historial.

No debe consumir APIs.

---

# SENAMHI Provider

## Endpoints iniciales

### Pronóstico Diario

```
https://senamhi.gob.bo/api/pronostico/diario
```

Archivo generado

```
latest/diario.json
```

---

### Pronóstico Extendido

```
https://senamhi.gob.bo/api/pronostico/ediario
```

Archivo generado

```
latest/ediario.json
```

---

## Flujo del Provider

```text
collector.py

↓

Consultar diario

↓

Consultar ediario

↓

Validar respuestas

↓

Consolidar datasets

↓

Enviar al Storage
```

---

# Formato de almacenamiento

## latest

Siempre contendrá la información más reciente.

```text
data/

senamhi/

latest/

diario.json

ediario.json
```

---

## history

Solo se generará cuando existan cambios.

```text
data/

senamhi/

history/

2026/

07/

29/

080000/

diario.json

ediario.json
```

Cada carpeta representa una ejecución.

Esto garantiza que ambos archivos pertenecen exactamente al mismo momento de captura.

---

# Estrategia de cambios

```text
Consultar endpoints

↓

Comparar diario.json

↓

Comparar ediario.json

↓

¿Existe algún cambio?

├── NO
│
│   Finalizar
│
└── SI
    │
    ├── Actualizar latest
    ├── Crear carpeta history
    ├── Guardar todos los datasets
    └── Commit automático
```

---

# Manejo de errores

Los endpoints son independientes.

Ejemplo

```text
diario      ✓

ediario     ✗
```

Resultado

- Se guarda `diario.json`.
- Se registra el error de `ediario`.
- El proceso continúa.
- El workflow finaliza con advertencia.

No se cancela toda la ejecución por el fallo de un endpoint.

---

# Tecnologías

| Componente | Tecnología |
|------------|------------|
| Lenguaje | Python 3.13 |
| Cliente HTTP | httpx |
| Scheduler | GitHub Actions |
| Formato | JSON |
| Control de versiones | Git |
| Repositorio | GitHub |

---

# Roadmap

## Sprint 0 — Diseño

### Objetivos

- Definir arquitectura.
- Definir estructura.
- Definir Providers.
- Definir Storage.
- Definir convenciones.
- Documentar el proyecto.

---

## Sprint 1 — Inicialización

### Objetivos

- Crear repositorio.
- Configurar Python.
- Crear entorno virtual.
- Crear estructura de carpetas.
- Configurar dependencias.

Resultado esperado

```bash
python main.py
```

---

## Sprint 2 — Configuración

Crear un módulo central de configuración.

Contendrá

- URLs
- Timeouts
- Retries
- Paths
- Variables globales

---

## Sprint 3 — Provider SENAMHI

Implementar

- collector.py
- diario.py
- ediario.py

El Provider debe ejecutar ambos endpoints.

---

## Sprint 4 — Validación

Validar

- HTTP 200
- JSON válido
- Timeout
- Respuesta vacía
- Manejo de errores por endpoint

---

## Sprint 5 — Storage

Implementar

- latest/
- history/
- Comparación de cambios
- Escritura de archivos

---

## Sprint 6 — Logs

Agregar logs.

Ejemplo

```
INFO  Ejecutando SENAMHI

INFO  Descargando diario

INFO  Descargando ediario

INFO  Sin cambios

INFO  Historial generado

ERROR Error en ediario
```

---

## Sprint 7 — GitHub Actions

Workflow

```text
Checkout

↓

Instalar Python

↓

Instalar dependencias

↓

Ejecutar main.py

↓

Detectar cambios

↓

Commit

↓

Push
```

---

## Sprint 8 — Testing

Probar

- Ambos endpoints disponibles.
- Solo uno disponible.
- Ambos caídos.
- Timeout.
- JSON inválido.
- Sin cambios.
- Con cambios.

---

## Sprint 9 — Escalabilidad

Agregar nuevos Providers.

Ejemplo

```text
providers/

senamhi/

bcb/

ine/

snis/
```

Sin modificar la arquitectura.

---

## Sprint 10 — Observabilidad

Registrar

- Tiempo de respuesta por endpoint.
- Tiempo total del Provider.
- Tamaño del JSON.
- Cambios detectados.
- Historial generado.

---

# Objetivo Final

Construir una plataforma de recolección de datos públicos de Bolivia basada en **Providers**, donde cada institución pueda contener múltiples endpoints independientes, permitiendo incorporar nuevas fuentes de información sin modificar la arquitectura principal del sistema.

El primer Provider será **SENAMHI**, iniciando con los endpoints:

- `/api/pronostico/diario`
- `/api/pronostico/ediario`

Este Provider servirá como plantilla para futuras integraciones con instituciones como BCB, INE, SNIS y otras APIs públicas.