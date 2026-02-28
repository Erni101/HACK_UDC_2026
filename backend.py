import requests
import math
from flask import Flask, jsonify

app = Flask(__name__)

# 1. Pon aquí tu URL exacta de TomTom que ya tenías
TOMTOM_URL = "https://api.tomtom.com/traffic/services/5/incidentDetails?key=o9OiRMAtBAVlYHBE8GgIhfxAH3Urvyx5&bbox=-8.9,42.8,-7.8,43.8&fields={incidents{type,geometry{type,coordinates},properties{magnitudeOfDelay,events{description,code}}}}&zoom=10"

# 2. Base de datos de Hospitales en A Coruña
# 2. Base de datos de Complejos Hospitalarios de Galicia (Red SERGAS)
HOSPITALES = [
    {"nombre": "CHUAC (A Coruña)", "lat": 43.3444, "lon": -8.3813},
    {"nombre": "CHUS (Santiago)", "lat": 42.8647, "lon": -8.5631},
    {"nombre": "Álvaro Cunqueiro (Vigo)", "lat": 42.1986, "lon": -8.7497},
    {"nombre": "HULA (Lugo)", "lat": 43.0360, "lon": -7.5255},
    {"nombre": "CHUO (Ourense)", "lat": 42.3458, "lon": -7.8447},
    {"nombre": "Montecelo (Pontevedra)", "lat": 42.4285, "lon": -8.6231},
    {"nombre": "Arquitecto Marcide (Ferrol)", "lat": 43.5019, "lon": -8.2324}
]

# Fórmula matemática para calcular distancia real en kilómetros
def calcular_distancia(lat1, lon1, lat2, lon2):
    R = 6371.0 # Radio de la Tierra en km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def encontrar_hospital_cercano(accidente_lat, accidente_lon):
    mas_cercano = HOSPITALES[0]
    distancia_minima = float('inf')
    
    for hosp in HOSPITALES:
        # Cálculo de distancia simple
        d = math.sqrt((hosp['lat'] - accidente_lat)**2 + (hosp['lon'] - accidente_lon)**2)
        if d < distancia_minima:
            distancia_minima = d
            mas_cercano = hosp
    return mas_cercano

@app.route('/api/accidentes', methods=['GET'])
def obtener_accidentes():
    try:
        # 1. Definimos los 4 cuadrantes (cada uno < 10,000 km2)
        cuadrantes = [
            "-9.3,43.0,-8.0,43.8", # Noroeste (Coruña/Costa da Morte)
            "-8.0,43.0,-6.7,43.8", # Noreste (Lugo/Marina Lucense)
            "-9.1,41.8,-7.8,42.8", # Suroeste (Pontevedra/Vigo)
            "-7.8,41.8,-6.7,43.0"  # Sudeste (Ourense/Interior)
        ]
        
        todos_los_incidentes = []
        api_key = "o9OiRMAtBAVlYHBE8GgIhfxAH3Urvyx5"

        for bbox in cuadrantes:
            # Construimos la URL para este cuadrante específico
            url = f"https://api.tomtom.com/traffic/services/5/incidentDetails?key={api_key}&bbox={bbox}&fields={{incidents{{type,geometry{{type,coordinates}},properties{{magnitudeOfDelay,events{{description,code}}}}}}}}&zoom=9"
            
            respuesta = requests.get(url)
            if respuesta.status_code == 200:
                datos_cuadrante = respuesta.json()
                incidentes_cuadrante = datos_cuadrante.get('incidents', [])
                
                # Procesamos los incidentes de este cuadrante
                for incidente in incidentes_cuadrante:
                    coordenadas = incidente['geometry']['coordinates']
                    
                    # Normalización de coordenadas
                    if isinstance(coordenadas[0], list):
                        lon_accidente = coordenadas[0][0]
                        lat_accidente = coordenadas[0][1]
                    else:
                        lon_accidente = coordenadas[0]
                        lat_accidente = coordenadas[1]

                    # Tu lógica de hospital más cercano
                    hospital_cercano = min(HOSPITALES, key=lambda h: calcular_distancia(lat_accidente, lon_accidente, h['lat'], h['lon']))

                    # Sustituye tu línea actual por esta exacta:
                    # Busca esta línea en tu bucle for de Python y cámbiala:
                    url_maps = f"https://www.google.com/maps/dir/?api=1&origin={hospital_cercano['lat']},{hospital_cercano['lon']}&destination={lat_accidente},{lon_accidente}&travelmode=driving"
                    
                    # Inyectamos las propiedades extra (CORREGIDO)
                    incidente['propiedades_extra'] = {
                        'hospital_asignado': hospital_cercano['nombre'],
                        'h_lat': str(hospital_cercano['lat']),
                        'h_lon': str(hospital_cercano['lon']),
                        'latitud': str(lat_accidente),
                        'longitud': str(lon_accidente),
                        'url_ruta_rapida': url_maps
                    }
                    
                    todos_los_incidentes.append(incidente)

        # Devolvemos el formato que Grafana espera
        return jsonify({"incidents": todos_los_incidentes})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
if __name__ == '__main__':
    # Arrancamos nuestro propio servidor local
    app.run(port=5000, debug=True)