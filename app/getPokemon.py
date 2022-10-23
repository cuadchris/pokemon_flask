import requests as r

def getBio(pokemon_id):
    url = f'https://pokeapi.co/api/v2/pokemon-species/{pokemon_id}/'
    response = r.get(url)
    data = response.json()
    bio = data['flavor_text_entries'][1]['flavor_text']
    return bio

def addPokemon(pokemon):
        url = f'https://pokeapi.co/api/v2/pokemon/{pokemon.lower()}'
        response = r.get(url)
        if not response.ok:
            return False
        data = response.json()
        pokedict = {}
        pokedict = {
            'name': data['name'],
            'abilities': data['abilities'][0]['ability']['name'],
            'f_shiny': data['sprites']['other']['official-artwork']['front_default'],
            'stats': [{x['stat']['name']: x['base_stat']} for x in data['stats'][:3]],
            'bio': getBio(data['id']),
            'type': data['types'][0]['type']['name']
        }
        return pokedict