import requests
import math
from flask import Flask, jsonify

app = Flask(__name__)

# 1. Pon aquí tu URL exacta de TomTom que ya tenías
TOMTOM_URL = "https://api.tomtom.com/traffic/services/5/incidentDetails?key=o9OiRMAtBAVlYHBE8GgIhfxAH3Urvyx5&bbox=-8.45,43.30,-8.35,43.40&fields={incidents{type,geometry{type,coordinates},properties{id,iconCategory,magnitudeOfDelay,events{description},startTime,endTime,from,to,length,delay}}}&language=es-ES"

# 2. Base de datos de Hospitales en A Coruña
# 2. Base de datos de Complejos Hospitalarios de Galicia (Red SERGAS)
HOSPITALES = [
    {"nombre": "CHUAC (A Coruña)", "lat": 43.3411, "lon": -8.3813},
    {"nombre": "CHUS (Santiago de Compostela)", "lat": 42.8695, "lon": -8.5656},
    {"nombre": "CHUF - Arquitecto Marcide (Ferrol)", "lat": 43.5042, "lon": -8.2285},
    {"nombre": "HULA (Lugo)", "lat": 43.0031, "lon": -7.5250},
    {"nombre": "CHUO (Ourense)", "lat": 42.3275, "lon": -7.8540},
    {"nombre": "CHOP - Montecelo (Pontevedra)", "lat": 42.4331, "lon": -8.6148},
    {"nombre": "Hospital Álvaro Cunqueiro (Vigo)", "lat": 42.1889, "lon": -8.7150}
]

# Fórmula matemática para calcular distancia real en kilómetros
def calcular_distancia(lat1, lon1, lat2, lon2):
    R = 6371.0 # Radio de la Tierra en km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

@app.route('/api/accidentes', methods=['GET'])
def obtener_accidentes():
    try:
        # Descargamos los datos de TomTom
        respuesta = requests.get(TOMTOM_URL)
        datos = respuesta.json()
        
        # Procesamos cada accidente para buscar su hospital
        for incidente in datos.get('incidents', []):
            coordenadas = incidente['geometry']['coordinates']
            # Si el incidente es un tramo (lista de listas), cogemos el primer punto de inicio
            if isinstance(coordenadas[0], list):
                lon_accidente = coordenadas[0][0]
                lat_accidente = coordenadas[0][1]
            else:
                lon_accidente = coordenadas[0]
                lat_accidente = coordenadas[1]
            
            # Buscamos el hospital con la distancia mínima
            hospital_cercano = min(HOSPITALES, key=lambda h: calcular_distancia(lat_accidente, lon_accidente, h['lat'], h['lon']))
            
            # Le inyectamos al JSON la URL exacta de Google Maps ya calculada
            url_maps = f"https://www.google.com/maps/dir/{hospital_cercano['lat']},{hospital_cercano['lon']}/{lat_accidente},{lon_accidente}"
            incidente['propiedades_extra'] = {
                'hospital_asignado': hospital_cercano['nombre'],
                'url_ruta_rapida': url_maps,
                'latitud': lat_accidente,   # Añadimos esto
                'longitud': lon_accidente   # Añadimos esto
            }
            
        return jsonify(datos)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Arrancamos nuestro propio servidor local
    app.run(port=5000, debug=True)