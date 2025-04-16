from typing import Tuple
import requests
import json

url = "https://swapi.py4e.com/api/people/{people}/"
all_people = []

def get_people(count: int):
    try:
        response = requests.get(url.format(people=count))
        data = response.json()
        if len(data) > 0:
            people = {
                'name': data.get("name"),
                "planet": data.get("homeworld")
            }
            return people
        else:
            raise ValueError('No data found')
        
    except Exception as ex:
        raise ex

for i in range(1, 1000):
    people = get_people(count=i)
    
    all_people.append(people)
    
with open('people.json', mode='w') as file:
    file.write(json.dumps(all_people))
    