# 🚨 Mapa de Accidentes en Tiempo Real — Galicia

> Proyecto presentado en la **Hackathon 2026**

Sistema de monitorización y visualización de accidentes de tráfico en Galicia en tiempo real. Detecta incidentes activos, asigna automáticamente el hospital SERGAS más cercano mediante cálculo Haversine, y centraliza los datos en Grafana Cloud Loki para su visualización en un dashboard público.

---

## 📐 Arquitectura

```
TomTom Traffic API (4 cuadrantes geográficos)
        │
        ▼
  backend.py  ──────►  Flask REST API  (/api/accidentes)
        │
        │   Enriquecimiento por incidente:
        │     - Coordenadas del accidente
        │     - Hospital SERGAS más cercano (Haversine)
        │     - Enlace directo de ruta en Google Maps
        │
        ▼
accidentes_tu_loki.py  (polling cada 60s)
        │
        ▼
  Grafana Cloud Loki
        │
        ▼
  Dashboard público en tiempo real
```

---

## 🧩 Componentes

### `backend.py` — API Flask

Servidor REST que actúa como intermediario entre TomTom y el agente de monitorización.

- Divide Galicia en **4 cuadrantes geográficos** para superar los límites de área de la TomTom Traffic Incidents API v5 (2 claves API rotadas).
- Calcula el **hospital SERGAS más cercano** a cada incidente usando la fórmula de Haversine.
- Devuelve un JSON enriquecido con hospital asignado, coordenadas y enlace de ruta directa.

**Cuadrantes cubiertos:**

| Cuadrante | Bbox | API Key |
|-----------|------|---------|
| Noroeste | `-9.3,43.0,-8.0,43.8` | `API_KEY_NORTE` |
| Noreste | `-8.0,43.0,-6.7,43.8` | `API_KEY_NORTE` |
| Suroeste | `-8.9,42.0,-7.8,42.8` | `API_KEY_SUR` |
| Sudeste | `-7.8,42.0,-6.8,42.8` | `API_KEY_SUR` |

**Hospitales SERGAS incluidos:**

| Hospital | Ciudad |
|----------|--------|
| CHUAC | A Coruña |
| CHUS | Santiago de Compostela |
| Álvaro Cunqueiro | Vigo |
| HULA | Lugo |
| CHUO | Ourense |
| Montecelo | Pontevedra |
| Arquitecto Marcide | Ferrol |

**Endpoint disponible:**

```
GET /api/accidentes
```

Respuesta:
```json
{
  "incidents": [
    {
      "type": "...",
      "geometry": { "type": "Point", "coordinates": [lon, lat] },
      "properties": { ... },
      "propiedades_extra": {
        "hospital_asignado": "CHUAC (A Coruña)",
        "h_lat": "43.3444",
        "h_lon": "-8.3813",
        "latitud": "43.35",
        "longitud": "-8.40",
        "url_ruta_rapida": "https://www.google.com/maps/dir/..."
      }
    }
  ]
}
```

---

### `accidentes_tu_loki.py` — Agente de Monitorización

Script autónomo que conecta el backend con Grafana Cloud Loki.

- Consulta `/api/accidentes` cada **60 segundos**.
- Serializa cada incidente como log JSON y lo envía a Grafana Loki con los labels:
  - `service_name: mapa-accidentes`
  - `env: prod`
- **Resistente a fallos de red:** captura excepciones sin interrumpir el bucle. Omite proxies corporativos y certificados inválidos para funcionar en redes restrictivas.

---

### `DashboardFinal.json` — Dashboard de Grafana

Definición exportada del dashboard de Grafana Cloud. Importable directamente desde la UI de Grafana.

**🔗 Dashboard público:**
[https://lucasvilanova71.grafana.net/public-dashboards/670fb5756d194ecdad84b83dfd0bf76a](https://lucasvilanova71.grafana.net/public-dashboards/670fb5756d194ecdad84b83dfd0bf76a)

---

## 🚀 Instalación y uso

### Requisitos

```bash
pip install flask requests
```

### 1. Arrancar el backend

```bash
python backend.py
```

Arranca un servidor Flask en `http://localhost:5000`.

### 2. Exponer con ngrok (acceso externo)

```bash
ngrok http 5000
```

Copia la URL generada y actualiza `API_URL` en `accidentes_tu_loki.py`.

> El backend incluye la cabecera `ngrok-skip-browser-warning: true` para evitar la pantalla de aviso de ngrok.

### 3. Lanzar el agente Loki

```bash
python accidentes_tu_loki.py
```

---

## ⚙️ Configuración

Edita las siguientes variables en cada archivo:

**`backend.py`**

| Variable | Descripción |
|----------|-------------|
| `API_KEY_NORTE` | API key de TomTom para cuadrantes norte |
| `API_KEY_SUR` | API key de TomTom para cuadrantes sur |

**`accidentes_tu_loki.py`**

| Variable | Descripción |
|----------|-------------|
| `LOKI_URL` | Endpoint push de Grafana Cloud Loki |
| `LOKI_USER` | ID de usuario de Grafana Cloud |
| `LOKI_PASSWORD` | Token de API (`glc_...`) |
| `API_URL` | URL pública del backend (ngrok o producción) |
| `INTERVALO_SEGUNDOS` | Frecuencia de polling (por defecto: `60`) |

---

## 🛠️ Stack tecnológico

| Tecnología | Uso |
|------------|-----|
| Python 3 + Flask | Backend REST API |
| TomTom Traffic Incidents API v5 | Fuente de datos de incidentes |
| Grafana Cloud Loki | Almacenamiento y consulta de logs |
| Grafana Dashboards | Visualización en tiempo real |
| ngrok | Túnel HTTP para exposición pública |
| Google Maps Directions API | Rutas de emergencia hospital → accidente |

---

## 👥 Equipo

Proyecto desarrollado para la **Hackathon 2026**.
