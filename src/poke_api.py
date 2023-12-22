
class ImagePokemon:
    
    def __init__(self):
        self._image = None 

    def set_image(self, image):
        self._image = image


class ImagePokemonBuilder:

    def __init__(self, pokemon_id, versions, generation, game, is_shiny):
        self.pokemon_id = pokemon_id
        self.versions = versions
        self.generation = generation
        self.game = game
        self.is_shiny = is_shiny

        self.image_pokemon = ImagePokemon()

    def if_generation_one(self):
        if self.generation.value == PokeGeneration.GEN_I.value and self.pokemon_id in range(1, 151):
            image = get_image_of_pokemon(self.versions, generation='generation-i', game='red-blue', is_shiny=False)
            self.image_pokemon.set_image(image)
        return self
    
    def if_generation_two(self):
        if self.generation.value == PokeGeneration.GEN_II.value and self.pokemon_id in range(1, 251):
            image = get_image_of_pokemon(self.versions, generation='generation-ii', game='crystal', is_shiny=self.is_shiny)
            self.image_pokemon.set_image(image)
        return self
    
    def if_generation_three(self):
        if self.generation.value == PokeGeneration.GEN_III.value and self.pokemon_id in range(1, 386):
            image = get_image_of_pokemon(self.versions, generation='generation-iii', game='emerald', is_shiny=self.is_shiny)
            self.image_pokemon.set_image(image)
        return self

    def if_generation_four(self):
        if self.generation.value == PokeGeneration.GEN_IV.value and self.pokemon_id in range(1, 493):
            image = get_image_of_pokemon(self.versions,  generation='generation-iv', game='platinum', is_shiny=self.is_shiny)
            self.image_pokemon.set_image(image)
        return self
    
    def if_generation_five(self):
        if self.generation.value == PokeGeneration.GEN_V.value and self.pokemon_id in range(1, 649):
            image = get_image_of_pokemon(self.versions, generation='generation-v', game='black-white', is_shiny=self.is_shiny)
            self.image_pokemon.set_image(image)
        return self
    
    def if_generation_six(self):
        if self.generation.value == PokeGeneration.GEN_VI.value and self.pokemon_id in range(1, 721):
            image = get_image_of_pokemon(self.versions, generation='generation-vi', game='x-y', is_shiny=self.is_shiny)
            self.image_pokemon.set_image(image)
        return self
    

    def build(self):
        return self.image_pokemon

    def get_image_of_pokemon(self, versions,  generation, game, is_shiny) -> str:
        image = versions[generation][game]['front_default'] if not is_shiny else versions[generation][game]['front_shiny']
        return image


from enum import Enum


class PokeGeneration(Enum):
    GEN_I = 'generation-i'
    GEN_II = 'generation-ii'
    GEN_III = 'generation-iii'
    GEN_IV = 'generation-iv'
    GEN_V = 'generation-v'
    GEN_VI = 'generation-vi'
    # GEN_VII = 'generation-vii'
    # GEN_VIII = 'generation-viii'
    # GEN_IX = 'generation-ix'


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

class Parameters:
    id : int
    is_shiny: bool
    generation: str
    art_style : str

    def __init__(self, id : int, is_shiny: bool, generation : str, art_style :str) -> None:
        self.id = id
        self.is_shiny = is_shiny

        if generation not in PokeGeneration._value2member_map_:
            raise ValueError(f"Generaton input is invalid")

        self.generation = PokeGeneration(generation)
        self.art_style = art_style

import logging

from flask import Flask, jsonify, request
import requests

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

pokemon_species_url = 'https://pokeapi.co/api/v2/pokemon/'

def get_image_of_pokemon(versions, generation, game, is_shiny) -> str:
    image = versions[generation][game]['front_default'] if not is_shiny else versions[generation][game]['front_shiny']
    return image

@app.route('/obs-pokemon/team/species/<int:id>', methods=['POST'])
def get_pokemon_by_id(id : int):
    data = request.json
    params = Parameters(data['id'], data['is_shiny'], data['generation'], data['art_style'])

    if id is None or id == 0:
        status_bad_request = 400
        response = {"status_code" : status_bad_request, "message" : "Bad request no id has been in inputed"}
        return jsonify(response), status_bad_request

    response = requests.get(f'{pokemon_species_url}/{id}')
 
    if response.status_code == 200:
        pokemon = response.json() 

        sprite = pokemon['sprites']
        species = pokemon['species']['name']

        if params.art_style == '' :
            versions = sprite['versions']
            pkmn_image = ImagePokemonBuilder(id, versions, params.generation, "", params.is_shiny).if_generation_one().if_generation_two().if_generation_three().if_generation_four().if_generation_five().if_generation_six().build()

    status_ok = 200
    response = {"status_code" : status_ok, "data" : APIResponse(species, pkmn_image._image).to_dictionary()}

    return jsonify(response), status_ok



@app.errorhandler(ValueError)
def handle_value_error(error):
    response = {
        'error' : 'Invalid Input',
        'message': str(error)
    }
    return jsonify(response), 400



if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True,port='9001')