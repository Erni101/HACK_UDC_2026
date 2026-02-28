from flask import Flask, jsonify, request
from flask_cors import CORS
import random
from datetime import datetime

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


if __name__ == '__main__':
    print("🚀 API iniciada en http://localhost:5000")
    print(f"📍 Centro de A Coruña: {BASE_LATITUDE}, {BASE_LONGITUDE}")
    app.run(debug=True, host='0.0.0.0', port=5000)
