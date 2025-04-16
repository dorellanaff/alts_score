import requests
import json

url_post = "https://makers-challenge.altscore.ai/v1/s1/e6/solution"

headers = {
    'accept': 'application/json',
    'API-KEY': '64462b944b7e4d458009596b5bc5611e'
}

# URL base de la API
url_base = "https://pokeapi.co/api/v2/type/"

# Tipos de Pokémon en el juego
types = [
    "bug", "dark", "dragon", "electric", "fairy", "fighting", "fire", 
    "flying", "ghost", "grass", "ground", "ice", "normal", "poison", 
    "psychic", "rock", "steel", "water"
]

# Diccionario para almacenar la suma de las alturas y el conteo de los Pokémon por tipo
type_dict = {}

# Obtener los Pokémon de cada tipo y sus alturas
for type_name in types:
    print(f"Procesando tipo: {type_name}")
    
    # Hacer la consulta para obtener todos los Pokémon de ese tipo
    url = f"{url_base}{type_name}/"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        
        # Inicializar la suma de alturas y el contador para este tipo
        sum_height = 0
        count = 0
        
        # Iterar sobre los Pokémon de este tipo
        for pokemon_info in data["pokemon"]:
            # Obtener el URL del Pokémon para consultar su altura
            pokemon_url = pokemon_info["pokemon"]["url"]
            response_pokemon = requests.get(pokemon_url)
            
            if response_pokemon.status_code == 200:
                data_pokemon = response_pokemon.json()
                
                # Obtener la altura del Pokémon
                height = data_pokemon["height"]
                
                # Sumar la altura al tipo correspondiente
                sum_height += height
                count += 1

        # Guardar la información en el diccionario type_dict
        type_dict[type_name] = {
            "sum_height": sum_height,
            "count": count
        }

# Crear el diccionario final para el payload
height_payload = {"heights": {}}

# Procesar el diccionario para calcular el promedio de alturas
for type_name, data in type_dict.items():
    if data["count"] > 0:
        # Calcular el promedio de altura
        avg_height = data["sum_height"] / data["count"]
        avg_height = f"{avg_height:.3f}"
        # Guardar en el diccionario final con 3 decimales
        height_payload["heights"][type_name] = float(avg_height)
    else:
        height_payload["heights"][type_name] = 0  # Si no hay Pokémon de este tipo, poner 0

# Ordenar los tipos alfabéticamente
sorted_heights = {k: height_payload["heights"][k] for k in sorted(height_payload["heights"].keys())}

# Mostrar el resultado final
height_payload["heights"] = sorted_heights
print(json.dumps(height_payload, indent=4))

response = requests.post(url_post, json=height_payload, headers=headers)
print("Alturas promedio enviadas correctamente:", response.text)