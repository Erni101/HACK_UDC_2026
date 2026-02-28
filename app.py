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

# Datos simulados de accidentes en A Coruña
sample_accidents = [
    {
        "id": 1,
        "name": "Accidente en Plaza María Pita",
        "description": "Colisión entre dos vehículos",
        "severity": "medium",
        "geometry": {
            "coordinates": [[43.3745, -8.3875]]
        }
    },
    {
        "id": 2,
        "name": "Accidente en Calle Real",
        "description": "Atropello",
        "severity": "high",
        "geometry": {
            "coordinates": [[43.3720, -8.3900]]
        }
    },
    {
        "id": 3,
        "name": "Accidente en Avenida de la Marina",
        "description": "Vuelco de vehículo",
        "severity": "high",
        "geometry": {
            "coordinates": [[43.3750, -8.3850]]
        }
    },
    {
        "id": 4,
        "name": "Accidente en Paseo Marítimo",
        "description": "Choque múltiple",
        "severity": "medium",
        "geometry": {
            "coordinates": [[43.3690, -8.3920]]
        }
    },
    {
        "id": 5,
        "name": "Accidente en Plaza del Humor",
        "description": "Fuerte colisión",
        "severity": "low",
        "geometry": {
            "coordinates": [[43.3760, -8.3860]]
        }
    }
]


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


@app.route('/api/accidentes', methods=['GET'])
def get_accidents():
    """Obtiene todos los accidentes simulados"""
    return jsonify({
        "status": "success",
        "incidents": sample_accidents,
        "total": len(sample_accidents)
    }), 200


@app.route('/api/proximity', methods=['GET'])
def proximity():
    """Calcula la distancia a accidentes cercanos (dentro de un radio)
    Parámetro opcional: radius (en km, default: 5 km)
    """
    global current_location
    
    # Tu ubicación actual
    my_lat = current_location['latitude']
    my_lon = current_location['longitude']
    
    # Radio de búsqueda (en km)
    radius = request.args.get('radius', 5, type=float)
    
    try:
        # Usar los accidentes simulados
        incidents = sample_accidents
        
        if not incidents:
            return jsonify({
                "status": "success",
                "nearby_accidents": [],
                "message": "No hay incidentes registrados"
            }), 200
        
        nearby = []
        
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
                
                # Solo incluir si está dentro del radio
                if distance <= radius:
                    nearby.append({
                        "id": inc.get('id'),
                        "name": inc.get('name'),
                        "description": inc.get('description'),
                        "severity": inc.get('severity'),
                        "distance_km": round(distance, 2),
                        "coordinates": {
                            "latitude": acc_lat,
                            "longitude": acc_lon
                        }
                    })
        
        # Ordenar por distancia
        nearby.sort(key=lambda x: x['distance_km'])
        
        return jsonify({
            "status": "success",
            "search_radius_km": radius,
            "nearby_accidents": nearby,
            "total_nearby": len(nearby),
            "my_location": {
                "latitude": my_lat,
                "longitude": my_lon
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error al calcular proximidad: {str(e)}"
        }), 500


if __name__ == '__main__':
    print("🚀 API iniciada en http://localhost:5000")
    print(f"📍 Centro de A Coruña: {BASE_LATITUDE}, {BASE_LONGITUDE}")
    app.run(debug=True, host='0.0.0.0', port=5000)
