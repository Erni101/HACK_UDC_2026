import requests
import time
import json
import urllib3
import os
from pathlib import Path
from dotenv import load_dotenv

# 1. Silenciamos las advertencias molestas

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv(dotenv_path=Path(__file__).with_name(".env"))

# --- RELLENA ESTOS VALORES ---  
LOKI_URL = os.getenv("LOKI_URL", "")
LOKI_USER = os.getenv("LOKI_USER", "")
LOKI_PASSWORD = os.getenv("LOKI_PASSWORD", "")
API_URL = os.getenv("API_URL", "")
INTERVALO_SEGUNDOS = int(os.getenv("INTERVALO_SEGUNDOS", "60"))

def enviar_a_loki(accidente):  
    timestamp = str(time.time_ns())  
    mensaje = json.dumps(accidente)  
    payload = {  
        "streams": [{  
            "stream": {  
                "service_name": "mapa-accidentes",  
                "env": "prod"  
            },  
            "values": [[timestamp, mensaje]]  
        }]  
    }  
    
    try:
        # 2. Creamos una sesión aislada que ignora proxies y firewalls locales
        session = requests.Session()
        session.trust_env = False 
        
        response = session.post(  
            LOKI_URL,  
            json=payload,  
            auth=(LOKI_USER, LOKI_PASSWORD),  
            headers={"Content-Type": "application/json"},
            verify=False, # Ignora certificados rotos
            timeout=15,   # Si Grafana tarda más de 15s, corta
            proxies={"http": None, "https": None} # Salta el proxy de la red
        )  
        return response.status_code
    except Exception as e:
        # 3. ESCUDO ABSOLUTO: Si la red corta, devuelve texto, NO rompe el código
        return f"Bloqueo_Red ({type(e).__name__})"

def main():  
    if not all([LOKI_URL, LOKI_USER, LOKI_PASSWORD, API_URL]):
        print("❌ Faltan variables en .env: LOKI_URL, LOKI_USER, LOKI_PASSWORD o API_URL")
        return

    print("🚀 Iniciando radar de accidentes... (Pulsa Ctrl+C para parar)")
    while True:  
        try:  
            # Cabecera para saltar la pantalla azul de ngrok
            headers = {"ngrok-skip-browser-warning": "true"}
            
            # También ignoramos certificados al hablar con ngrok por si acaso
            r = requests.get(API_URL, headers=headers, timeout=15, verify=False)  
            
            if r.status_code != 200:
                print(f"⚠️ Error de ngrok/Flask: HTTP {r.status_code}")
            else:
                datos = r.json()  
                lista_accidentes = datos.get("incidents", [])
                
                if lista_accidentes:  
                    for acc in lista_accidentes:  
                        status = enviar_a_loki(acc)  
                        print(f"Enviado accidente → Loki [{status}]") 
                        time.sleep(1) 
                else:  
                    print("Tranquilidad absoluta. Sin accidentes activos.")  
                    
        except Exception as e:  
            print(f"⚠️ Fallo de conexión con ngrok: {type(e).__name__}")  
            
        time.sleep(INTERVALO_SEGUNDOS)  

if __name__ == "__main__":  
    print("Iniciando")
    main()