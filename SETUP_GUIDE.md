# 🗺️ Guía de Setup: API de Coordenadas + Grafana + Ngrok

## 1️⃣ Instalación Local

### Requisitos
- Python 3.8+
- pip

### Pasos
```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

## 2️⃣ Ejecutar la API

```bash
python app.py
```

La API estará disponible en `http://localhost:5000`

## 3️⃣ Endpoints Disponibles

### 📍 GET `/api/location`
Obtiene la ubicación actual:
```json
{
  "status": "success",
  "data": {
    "latitude": 43.3733,
    "longitude": -8.3888,
    "timestamp": "2026-02-28T10:30:45.123456",
    "accuracy": 5.0
  }
}
```

### 🎲 POST `/api/location/simulate`
Simula movimiento aleatorio alrededor del centro de A Coruña:
```bash
curl -X POST http://localhost:5000/api/location/simulate \
  -H "Content-Type: application/json" \
  -d '{"radius": 0.001}'
```

Parámetros opcionales:
- `radius`: Radio de variación en grados (default: 0.001 ≈ 111 metros)

### ✏️ POST `/api/location/update`
Actualiza la ubicación con coordenadas específicas:
```bash
curl -X POST http://localhost:5000/api/location/update \
  -H "Content-Type: application/json" \
  -d '{
    "latitude": 43.3750,
    "longitude": -8.3900,
    "accuracy": 5.0
  }'
```

### 🔄 POST `/api/location/reset`
Reinicia la ubicación al centro de A Coruña:
```bash
curl -X POST http://localhost:5000/api/location/reset
```

### ❤️ GET `/api/health`
Health check para monitoreo:
```bash
curl http://localhost:5000/api/health
```

## 4️⃣ Exponer con Ngrok

### Instalación de Ngrok
1. Descarga desde: https://ngrok.com/download
2. Descomprime y añade a PATH o usa la ruta completa

### Ejecutar Ngrok (con API corriendo)
```bash
ngrok http 5000
```

Te mostrará algo como:
```
Forwarding     https://abc123.ngrok.io -> http://localhost:5000
```

**Copia esa URL** (ej: `https://abc123.ngrok.io`)

## 5️⃣ Conectar con Grafana

### Setup Básico
1. Abre Grafana (por defecto en http://localhost:3000)
2. Ve a **Configuration > Data Sources > Add Data Source**
3. Selecciona **JSON API** o **SimpleJson**

### Configurar Data Source
- **Name**: "Coordenadas A Coruña"
- **URL**: `https://abc123.ngrok.io/api/location` (la URL de Ngrok)
- **Access**: Public
- **HTTP Method**: GET
- **Skip TLS Verify**: ON (para desarrollo)

### Crear Dashboard
1. **Create > Dashboard**
2. **Add Panel**
3. **Queries**: Selecciona tu Data Source
4. **Transformations**: Configura para extraer `latitude` y `longitude`
5. **Visualization**: 
   - **Geomap** (si Grafana >= 7.0)
   - O usa **Custom** plugin para mapas

### Ejemplo de configuración en Grafana
Para mostrar el punto en un mapa, puedes:
- Usar **Geomap** panel con campos `latitude` y `longitude`
- O crear alertas si sale de cierta zona

## 6️⃣ Testing Rápido

Con Ngrok ejecutándose:
```bash
# Test la API local
curl http://localhost:5000/api/location

# Test a través de Ngrok
curl https://abc123.ngrok.io/api/location

# Simular movimiento
curl -X POST https://abc123.ngrok.io/api/location/simulate
```

## 7️⃣ Tips para Desarrollo

### Simular Movimiento Continuo
Puedes crear un script que actualice continuamente:
```python
import requests
import time

url = "https://abc123.ngrok.io/api/location/simulate"

for i in range(100):
    requests.post(url, json={"radius": 0.001})
    time.sleep(2)  # Cada 2 segundos
    print(f"Actualización {i+1}")
```

### Coordenadas de Referencia en A Coruña
- **Centro**: 43.3733, -8.3888
- **Torre de Hércules**: 43.3826, -8.2476
- **Playa de Riazor**: 43.3665, -8.2447
- **Playa del Orzán**: 43.3710, -8.2455

### Variables de Entorno (Opcional)
Puedes editar `app.py` para usar variables:
```python
import os
BASE_LATITUDE = float(os.getenv('LAT', '43.3733'))
BASE_LONGITUDE = float(os.getenv('LON', '-8.3888'))
```

## 🐛 Troubleshooting

**Puerto 5000 ya en uso:**
```bash
# Cambiar puerto en app.py
app.run(port=5001)  # O cualquier otro
```

**Ngrok expira:**
- Usa versión gratuita (válida 2 horas) o actualiza a Premium
- Alterna entre reiniciar

**Grafana no ve datos:**
- Verifica CORS en app.py (ya está configurado)
- Comprueba que Ngrok está activo
- Mira logs de Grafana en el navegador (F12)

---

**¡Listo! 🚀** Tu API de ubicaciones está lista para Grafana en tiempo real.
