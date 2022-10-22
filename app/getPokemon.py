import requests as r

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
            'stats': [{x['stat']['name']: x['base_stat']} for x in data['stats'][:3]]
        }
        return pokedict