from typing import Tuple
import requests

url = "https://makers-challenge.altscore.ai/v1/s1/e2/resources/stars"
headers = {
    "accept": "application/json",
    "API-KEY": "8460cd2858da4598862615915c5ff579"
}

def get_starts_resonance(page: int, count: int) -> Tuple[int, bool]:
    params = {
        "page": page,
        "sort-by": "resonance",
        "sort-direction": "asc"
    }
    resonances = 0
    stop = False

    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    if len(data) > 0:
        count = count + len(data)
        resonances = sum([star['resonance'] for star in data])
    else:
        stop = True
    return resonances, stop, count
        

total = 0
count = 0
for i in range(1, 200):
    values = get_starts_resonance(page=i, count=count)
    
    resonances, stop, count = values
    total = total + resonances
    if stop:
        print(f'Se detuvo en la pagina {i}')
        break
print(total)
print(count)
print(total / count)