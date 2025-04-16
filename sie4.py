import requests
import json

# URL de la API
url = "https://makers-challenge.altscore.ai/v1/s1/e5/actions/perform-turn"

# Headers necesarios para la solicitud
headers = {
    "accept": "application/json",
    "API-KEY": "8460cd2858da4598862615915c5ff579",
    "Content-Type": "application/json"
}

# Función para interpretar la lectura del radar y extraer la posición de la nave enemiga
def get_enemy_position(radar_data):
    # El radar_data es un string con la lectura completa del radar
    # Cada fila del radar está separada por "|", y cada celda tiene el formato "a01", "b01", etc.
    rows = radar_data.split('|')
    for row_index, row in enumerate(rows):
        for col_index, cell in enumerate(row):
            if cell == '^':  # La nave enemiga está representada por '^'
                # La posición de la nave enemiga es la columna (col_index) y la fila (row_index)
                return (col_index, row_index)
    return None

# Función para convertir las coordenadas numéricas en coordenadas de letras
def convert_coordinates(x, y):
    # Convertir x, que es un índice (0-7), a una letra (a-h)
    x_letter = chr(97 + x)  # 'a' es el carácter ASCII 97
    return x_letter, y + 1  # Las filas en la cuadrícula son de 1 a 8, no de 0 a 7

# Función para realizar un ataque
def attack_enemy(x, y):
    # Convertir las coordenadas a formato adecuado para la API
    x_letter, y_value = convert_coordinates(x, y)

    # Datos a enviar en el cuerpo de la solicitud
    data = {
        "action": "attack",
        "attack_position": {
            "x": x_letter,
            "y": y_value
        }
    }

    # Hacer la solicitud POST
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Ver la respuesta
    if response.status_code == 200:
        print("Ataque ejecutado correctamente.")
        print(response.json())
    else:
        print(f"Error en la solicitud: {response.status_code}")
        print(response.text)

# Lectura del radar obtenida de la API
radar_data = "a01b01c01d01e01f01g01h01|a02b02c02d$2e02f02g02h02|a03b03c$3d03e03f03g03h03|a04b04c$4d04e04f04g04h04|a05b^5c05d05e05f05g05h05|a06b06c06d$6e06f06g06h06|a07b07c07d07e07f07g07h07|a08b08c08d08e#8f08g08h08|"

# Obtener la posición de la nave enemiga
enemy_position = get_enemy_position(radar_data)

if enemy_position:
    print(f"Nave enemiga detectada en: {enemy_position}")
    # Realizar el ataque en la posición de la nave enemiga
    attack_enemy(enemy_position[0], enemy_position[1])
else:
    print("Nave enemiga no detectada.")
