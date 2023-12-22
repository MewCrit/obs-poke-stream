
import logging

from flask import Flask, jsonify, request
import requests

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)



class APIResponse:
    species : str
    image : str

    def __init__(self, species : str, image : str) -> None:
        self.species = species
        self.image = image

    def to_dictionary(self):
        return {
            'species' : self.species,
            'image' : self.image
        }
    


pokemon_species_url = 'https://pokeapi.co/api/v2/pokemon/'

PKMN_HOME = 'home'
PKMN_ART = "art"

@app.route('/obs-pokemon/simple/team/species/<int:id>', methods=['POST'])
def get_pokemon_by_id(id : int):

    style = request.args.get('style')

    if style not in [PKMN_ART, PKMN_HOME]:
        response = {"status_code": status_bad_request, "message": "Bad request: invalid style"}
        return jsonify(response), status_bad_request
    
    
    if id is None or id == 0:
        status_bad_request = 400
        response = {"status_code" : status_bad_request, "message" : "Bad request no id has been in inputed"}
        return jsonify(response), status_bad_request

    response = requests.get(f'{pokemon_species_url}/{id}')

    if response.status_code == 200:
        pokemon = response.json() 

        art_style = ''

        if style == PKMN_HOME:
            art_style=pokemon['sprites']['other']['home']['front_default']
        else:
            art_style=pokemon['sprites']['other']['official-artwork']['front_default']

    species = pokemon['species']['name']

    status_ok = 200
    response = {"status_code" : status_ok, "data" :art_style, "species" : species}

    return jsonify(response), 200


@app.errorhandler(ValueError)
def handle_value_error(error):
    response = {
        'error' : 'Invalid Input',
        'message': str(error)
    }
    return jsonify(response), 400



if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True,port='9001')