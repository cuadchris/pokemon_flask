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
            'abilities': [ability['ability']['name'] for ability in data['abilities']],
            'f_shiny': data['sprites']['front_shiny'],
            'stats': [{x['stat']['name']: x['base_stat']} for x in data['stats']]
        }
        return pokedict