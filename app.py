from flask import Flask, jsonify, request
from flask_cors import CORS
import random
from datetime import datetime
import requests
from math import radians, sin, cos, atan2, sqrt
from math import radians, cos, sin, atan2, sqrt

app = Flask(__name__)
CORS(app)

# Coordenadas del centro de A Coruña
BASE_LATITUDE = 43.3733
BASE_LONGITUDE = -8.3888

# Estado actual de la ubicación
current_location = {
    "latitude": BASE_LATITUDE,
    "longitude": BASE_LONGITUDE,
    "timestamp": datetime.now().isoformat(),
    "accuracy": 5.0
}


@app.route('/api/location', methods=['GET'])
def get_location():
    """Obtiene la ubicación actual simulada"""
    return jsonify({
        "status": "success",
        "data": current_location
    }), 200


@app.route('/api/location/simulate', methods=['POST'])
def simulate_location():
    """
    Simula movimento aleatoria alrededor del centro de A Coruña.
    Parámetro opcional: radius (en km, default: 0.1 km)
    """
    global current_location
    
    # Obtener radio de variación (por defecto 100 metros)
    radius = request.json.get('radius', 0.001) if request.json else 0.001
    
    # Generar pequeñas variaciones (simulando movimiento)
    lat_variation = random.uniform(-radius, radius)
    lon_variation = random.uniform(-radius, radius)
    
    current_location['latitude'] = BASE_LATITUDE + lat_variation
    current_location['longitude'] = BASE_LONGITUDE + lon_variation
    current_location['timestamp'] = datetime.now().isoformat()
    
    return jsonify({
        "status": "success",
        "message": "Ubicación actualizada",
        "data": current_location
    }), 200


@app.route('/api/location/update', methods=['POST'])
def update_location():
    """Actualiza la ubicación con coordenadas específicas"""
    global current_location
    
    data = request.get_json()
    
    if not data or 'latitude' not in data or 'longitude' not in data:
        return jsonify({
            "status": "error",
            "message": "Se requieren latitude y longitude"
        }), 400
    
    current_location['latitude'] = data['latitude']
    current_location['longitude'] = data['longitude']
    current_location['accuracy'] = data.get('accuracy', 5.0)
    current_location['timestamp'] = datetime.now().isoformat()
    
    return jsonify({
        "status": "success",
        "message": "Ubicación actualizada correctamente",
        "data": current_location
    }), 200


@app.route('/api/location/reset', methods=['POST'])
def reset_location():
    """Reinicia la ubicación al centro de A Coruña"""
    global current_location
    
    current_location = {
        "latitude": BASE_LATITUDE,
        "longitude": BASE_LONGITUDE,
        "timestamp": datetime.now().isoformat(),
        "accuracy": 5.0
    }
    
    return jsonify({
        "status": "success",
        "message": "Ubicación reiniciada",
        "data": current_location
    }), 200


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check para monitoreo"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }), 200


def haversine(lat1, lon1, lat2, lon2):
    """Calcula la distancia entre dos puntos usando la fórmula haversine (en km)"""
    R = 6371  # Radio de la Tierra en km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    return 2 * R * atan2(sqrt(a), sqrt(1-a))


@app.route('/api/proximity', methods=['GET'])
def proximity():
    """Calcula la distancia al accidente más cercano"""
    global current_location
    
    # Tu ubicación actual
    my_lat = current_location['latitude']
    my_lon = current_location['longitude']
    
    try:
        # Obtener accidentes desde tu API (o ajusta según tu implementación)
        accidents = requests.get('http://localhost:5000/api/accidentes', timeout=5).json()
        incidents = accidents.get('incidents', [])
        
        if not incidents:
            return jsonify({
                "status": "success",
                "nearest_accident_km": None,
                "message": "No hay incidentes registrados"
            }), 200
        
        min_dist = float('inf')
        nearest_incident = None
        
        for inc in incidents:
            coords = inc.get('geometry', {}).get('coordinates', [])
            if coords:
                # Manejo de diferentes formatos de coordenadas
                if isinstance(coords[0], list):
                    acc_lon = coords[0][0]
                    acc_lat = coords[0][1]
                else:
                    acc_lon = coords[0]
                    acc_lat = coords[1]
                
                distance = haversine(my_lat, my_lon, acc_lat, acc_lon)
                
                if distance < min_dist:
                    min_dist = distance
                    nearest_incident = inc
        
        return jsonify({
            "status": "success",
            "nearest_accident_km": round(min_dist, 2) if min_dist != float('inf') else None,
            "nearest_incident": nearest_incident,
            "my_location": {
                "latitude": my_lat,
                "longitude": my_lon
            }
        }), 200
    
    except requests.exceptions.RequestException as e:
        return jsonify({
            "status": "error",
            "message": f"No se pudo conectar a la API de accidentes: {str(e)}"
        }), 500
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error al calcular proximidad: {str(e)}"
        }), 500


if __name__ == '__main__':
    print("🚀 API iniciada en http://localhost:5000")
    print(f"📍 Centro de A Coruña: {BASE_LATITUDE}, {BASE_LONGITUDE}")
    app.run(debug=True, host='0.0.0.0', port=5000)
