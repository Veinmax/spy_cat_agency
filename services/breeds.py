import requests


def validate_breed(breed: str) -> bool:
    response = requests.get("https://api.thecatapi.com/v1/breeds")
    breeds = response.json()
    return any(breed.lower() == breed_name["name"].lower() for breed_name in breeds)

