# 🚨 Mapa de Accidentes en Tiempo Real — Galicia

> Proyecto presentado en la **Hackathon 2026**

Sistema de monitorización y visualización de accidentes de tráfico en Galicia en tiempo real, con asignación automática del hospital más cercano y envío de logs a Grafana Cloud.

---

## ¿Qué hace este proyecto?

Detecta incidentes de tráfico activos en toda Galicia, identifica el hospital SERGAS más cercano a cada accidente y centraliza los datos en Grafana Loki para su análisis y visualización en tiempo real.

---

## Arquitectura

```
TomTom Traffic API
        │
        ▼
  backend.py  ──────►  Flask REST API  (/api/accidentes)
        │                      │
        │              Datos enriquecidos:
        │              - Coordenadas del accidente
        │              - Hospital más cercano (cálculo Haversine)
        │              - Enlace ruta Google Maps
        │
        ▼
accidentes_tu_loki.py
        │
        ▼
  Grafana Cloud Loki
  (Dashboard en tiempo real)
```

---

## Componentes

### `backend.py` — API Flask

- Consulta la **TomTom Traffic Incidents API v5** dividiendo Galicia en 4 cuadrantes geográficos para superar los límites de área de la API.
- Para cada incidente, calcula el **hospital SERGAS más cercano** usando la fórmula de Haversine.
- Devuelve un JSON enriquecido con hospital asignado, coordenadas y enlace de ruta directa a Google Maps.

**Hospitales incluidos:**
| Hospital | Ciudad |
|----------|--------|
| CHUAC | A Coruña |
| CHUS | Santiago de Compostela |
| Álvaro Cunqueiro | Vigo |
| HULA | Lugo |
| CHUO | Ourense |
| Montecelo | Pontevedra |
| Arquitecto Marcide | Ferrol |

### `accidentes_tu_loki.py` — Agente de Monitorización

- Consulta el endpoint `/api/accidentes` cada 60 segundos.
- Envía cada incidente como log a **Grafana Cloud Loki** con los labels `service_name: mapa-accidentes` y `env: prod`.
- Resistente a fallos de red: captura excepciones sin interrumpir el bucle.

---

## Instalación y uso

### Requisitos

```bash
pip install flask requests
```

### 1. Arrancar el backend

```bash
python backend.py
```

Arranca un servidor Flask en `http://localhost:5000`.

### 2. Exponer con ngrok (para acceso externo)

```bash
ngrok http 5000
```

Copia la URL generada y actualiza `API_URL` en `accidentes_tu_loki.py`.

### 3. Lanzar el agente Loki

```bash
python accidentes_tu_loki.py
```

---

## Configuración

Edita las siguientes variables en `accidentes_tu_loki.py`:

| Variable | Descripción |
|----------|-------------|
| `LOKI_URL` | URL del endpoint push de Grafana Cloud Loki |
| `LOKI_USER` | ID de usuario de Grafana Cloud |
| `LOKI_PASSWORD` | Token de API (`glc_...`) |
| `API_URL` | URL pública del backend (ngrok o producción) |
| `INTERVALO_SEGUNDOS` | Frecuencia de polling (por defecto: 60s) |

---

## Stack tecnológico

- **Python 3** + Flask
- **TomTom Traffic Incidents API v5**
- **Grafana Cloud Loki** — almacenamiento y visualización de logs
- **ngrok** — túnel HTTP para exposición pública del backend
- **Google Maps Directions API** — generación de rutas de emergencia

---

## Equipo

Proyecto desarrollado para la **Hackathon 2026**.
