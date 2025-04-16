import requests
import base64
from collections import defaultdict
from tqdm import tqdm
import time

API_KEY = '8460cd2858da4598862615915c5ff579'
ORACLE_URL = 'https://makers-challenge.altscore.ai/v1/s1/e3/resources/oracle-rolodex'
SUBMIT_URL = 'https://makers-challenge.altscore.ai/v1/s1/e3/solution'
HEADERS = {'accept': 'application/json', 'API-KEY': API_KEY}

def get_all_people():
    people = []
    url = 'https://swapi.py4e.com/api/people/'
    while url:
        res = requests.get(url).json()
        people.extend(res['results'])
        url = res.get('next')
    return people

def get_planet_name(planet_url):
    res = requests.get(planet_url)
    if res.status_code == 200:
        return res.json()['name']
    return 'Unknown'

def decode_oracle(name):
    url = f"{ORACLE_URL}?name={name.replace(' ', '%20')}"
    res = requests.get(url, headers=HEADERS)
    if res.status_code == 200:
        encoded = res.json().get('oracle_notes', '')
        try:
            decoded = base64.b64decode(encoded).decode('utf-8').lower()
            if 'light side' in decoded:
                return 'light'
            elif 'dark side' in decoded:
                return 'dark'
            else:
                return 'neutral'
        except Exception as e:
            print(f"Error decoding for {name}: {e}")
    return 'neutral'

def calculate_ibf():
    people = get_all_people()
    planet_data = defaultdict(lambda: {'light': 0, 'dark': 0, 'total': 0})
    planet_cache = {}

    print("Consultando al oráculo Jedi...")
    for person in tqdm(people):
        name = person['name']
        homeworld_url = person['homeworld']

        if homeworld_url not in planet_cache:
            planet_cache[homeworld_url] = get_planet_name(homeworld_url)
        planet_name = planet_cache[homeworld_url]

        side = decode_oracle(name)
        planet_data[planet_name]['total'] += 1
        if side in ['light', 'dark']:
            planet_data[planet_name][side] += 1
        
        time.sleep(0.3)  # Para evitar sobrecargar el servidor

    for planet, data in planet_data.items():
        light = data['light']
        dark = data['dark']
        total = data['total']
        ibf = round((light - dark) / total, 4)
        data['ibf'] = ibf

    return planet_data

def find_balanced_planet(planet_data):
    for planet, data in planet_data.items():
        if data['ibf'] == 0:
            return planet
    return None

def submit_solution(planet_name):
    response = requests.post(SUBMIT_URL, json={"planet_name": planet_name}, headers=HEADERS)
    if response.status_code == 200:
        print("✅ ¡Respuesta enviada correctamente!")
        print("🔓 Respuesta del servidor:", response.json())
    else:
        print("❌ Error al enviar la respuesta.")
        print(response.text)

if __name__ == "__main__":
    print("🌌 Iniciando búsqueda del planeta en equilibrio...")
    planet_data = calculate_ibf()
    balanced_planet = find_balanced_planet(planet_data)

    if balanced_planet:
        print(f"\n🌗 Planeta en equilibrio encontrado: {balanced_planet}")
        # submit_solution(balanced_planet)
    else:
        print("🛑 No se encontró un planeta con IBF = 0.")
