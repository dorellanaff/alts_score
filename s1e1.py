import requests
import time as t 
import re 

# URLs de la API
url_get = "https://makers-challenge.altscore.ai/v1/s1/e1/resources/measurement"
url_post = "https://makers-challenge.altscore.ai/v1/s1/e1/solution"

# Encabezados con la API-KEY
headers = {
    "accept": "application/json",
    "API-KEY": "64462b944b7e4d458009596b5bc5611e"
}

def obtener_medicion():
    """ Intenta obtener una medición válida del escáner. """
    while True:
        response = requests.get(url_get, headers=headers)
        if response.status_code == 200:
            data = response.json()
            distance_str = data.get("distance", "")
            time_str = data.get("time", "")

            try:
                # Extraer solo los números de las cadenas
                distance = float(re.search(r"[\d.]+", distance_str).group())
                time_observed = float(re.search(r"[\d.]+", time_str).group())

                if time_observed > 0:  # Evitar división por cero
                    return distance, time_observed
                
            except (ValueError, AttributeError):
                pass  # Si falla, volvemos a intentar

        print("Medición fallida. Reintentando...")
        t.sleep(1)  # Esperar 1 segundo antes de reintentar

def enviar_solucion(velocity):
    """ Envía la velocidad orbital calculada a la API. """
    payload = {"speed": velocity}  # Corrección aquí
    response = requests.post(url_post, json=payload, headers=headers)
    print("Respuesta del POST:", response.text)

# PASOS:
distance, time_observed = obtener_medicion()  # Paso 1: Obtener medición válida
velocity = round(distance / time_observed)  # Paso 2: Calcular velocidad y redondear
print(velocity)
enviar_solucion(velocity)  # Paso 3: Enviar solución