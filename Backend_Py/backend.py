import requests
import math
from flask import Flask, jsonify
import time 

app = Flask(__name__)


##EJECUTAR ESTE  BACKEND PRIMERO ANTES DE HACER NGROK HTTP 5000



# --- Configuración de API Keys ---
API_KEY_NORTE = "o9OiRMAtBAVlYHBE8GgIhfxAH3Urvyx5"
API_KEY_SUR   = "AZ2ibh4j2bp6LqNjeljk0MMdEeKthfpo"

# --- Base de datos de Hospitales en Galicia ---
HOSPITALES = [
    {"nombre": "CHUAC (A Coruña)",            "lat": 43.3444, "lon": -8.3813},
    {"nombre": "CHUS (Santiago)",              "lat": 42.8647, "lon": -8.5631},
    {"nombre": "Álvaro Cunqueiro (Vigo)",      "lat": 42.1986, "lon": -8.7497},
    {"nombre": "HULA (Lugo)",                  "lat": 43.0360, "lon": -7.5255},
    {"nombre": "CHUO (Ourense)",               "lat": 42.3458, "lon": -7.8447},
    {"nombre": "Montecelo (Pontevedra)",       "lat": 42.4285, "lon": -8.6231},
    {"nombre": "Arquitecto Marcide (Ferrol)",  "lat": 43.5019, "lon": -8.2324},
]

# --- Cuadrantes: cada entrada es (bbox, api_key) ---
CUADRANTES = [
    ("-9.3,43.0,-8.0,43.8", API_KEY_NORTE),  # Noroeste
    ("-8.0,43.0,-6.7,43.8", API_KEY_NORTE),  # Noreste
    ("-8.9,42.0,-7.8,42.8", API_KEY_SUR),    # Suroeste
    ("-7.8,42.0,-6.8,42.8", API_KEY_SUR),    # Sudeste
]
TOMTOM_URL = "https://api.tomtom.com/traffic/services/5/incidentDetails?key={key}&bbox={bbox}&fields={{incidents{{type,geometry{{type,coordinates}},properties{{magnitudeOfDelay,events{{description,code}}}}}}}}&zoom=9"

def calcular_distancia(lat1, lon1, lat2, lon2):
    R = 6371.0 #radio tierra
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2
         + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2))
         * math.sin(dlon / 2) ** 2)
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

def enriquecer_incidente(incidente):
    
    coordenadas = incidente["geometry"]["coordinates"]
    if isinstance(coordenadas[0], list):
        lon_acc, lat_acc = coordenadas[0][0], coordenadas[0][1]
    else:
        lon_acc, lat_acc = coordenadas[0], coordenadas[1]

    hospital = min(
        HOSPITALES,
        key=lambda h: calcular_distancia(lat_acc, lon_acc, h["lat"], h["lon"])
    )
    incidente["propiedades_extra"] = {
        "hospital_asignado": hospital["nombre"],
        "h_lat": str(hospital["lat"]),
        "h_lon": str(hospital["lon"]),
        "latitud":  str(lat_acc),
        "longitud": str(lon_acc),
        "url_ruta_rapida": (
            f"https://www.google.com/maps/dir/?api=1"
            f"&origin={hospital['lat']},{hospital['lon']}"
            f"&destination={lat_acc},{lon_acc}"
            f"&travelmode=driving"
        ),
    }
    return incidente

@app.route("/api/accidentes", methods=["GET"])

def obtener_accidentes():
    try:
        todos_los_incidentes = []

        for bbox, api_key in CUADRANTES:
            url = TOMTOM_URL.format(key=api_key, bbox=bbox)
            respuesta = requests.get(url, timeout=20)

            if respuesta.status_code != 200:
                app.logger.warning(
                    "Cuadrante %s devolvió HTTP %s", bbox, respuesta.status_code
                )
                continue

            for incidente in respuesta.json().get("incidents", []):
                todos_los_incidentes.append(enriquecer_incidente(incidente))
            time.sleep(0.5)

        return jsonify({"incidents": todos_los_incidentes})

    except Exception as e:
        app.logger.error("Error en obtener_accidentes: %s", e)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
