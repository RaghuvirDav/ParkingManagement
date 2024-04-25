"""
    This script is an external function that add employees to the local database.
    It need to be run seperately
    command: python add_emp_external.py
"""
import json
import requests


def add_characters_to_db(file_name):
    with open(file_name, 'r') as file:
        data = json.load(file)

    api_url = " http://127.0.0.1:8000/emp"

    characters = data.get("characters", [])

    for character in characters:
        character_name = character.get("characterName")
        if character_name:
            request_data = {'name': character_name}

            response = requests.post(api_url, json=request_data)

            if response.status_code == 201:
                print(f"Successfully added {character_name} to the database.")
            else:
                print(
                    f"Failed to add {character_name} to the database. Status code: {response.status_code}, Message: {response.text}")


add_characters_to_db('app/characters.json')
