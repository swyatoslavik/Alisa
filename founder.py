import requests


def get_city(shirota, dolgota):
    api_url = "https://geocode-maps.yandex.ru/1.x"
    params = dict()
    params["apikey"] = "40d1649f-0493-4b70-98ba-98533de7710b"
    params["format"] = "json"
    params["geocode"] = f"{dolgota},{shirota}"
    response = requests.get(api_url, params=params).json()
    city = response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"][
        "metaDataProperty"
    ]["GeocoderMetaData"]["AddressDetails"]["Country"]["AdministrativeArea"][
        "SubAdministrativeArea"
    ][
        "Locality"
    ][
        "LocalityName"
    ]
    return city


def get_city_coords(city):
    api_url = "https://geocode-maps.yandex.ru/1.x"
    params = dict()
    params["apikey"] = "40d1649f-0493-4b70-98ba-98533de7710b"
    params["format"] = "json"
    params["geocode"] = str(city)
    response = requests.get(api_url, params=params).json()
    return str(
        response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"][
            "Point"
        ]["pos"]
    ).split()[::-1]


def get_hospital(city):
    map_params = {
        "apikey": "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3",
        "text": f"Госпиталь {city}",
        "lang": "ru_RU",
        "results": "10",
    }

    response = requests.get(map_api_server, params=map_params).json()
    if not response["features"]:
        print(1)
        return "error", "error"
    else:
        return (
            response["features"][0]["geometry"]["coordinates"],
            response["features"][0]["properties"]["description"],
        )  # писок с 10 ближайшими объектами


def front(city):
    map_params = {
        "apikey": "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3",
        "text": f"Народный фронт {city}",
        "lang": "ru_RU",
        "results": "10",
    }

    response = requests.get(map_api_server, params=map_params).json()
    return (
        response["features"][0]["geometry"]["coordinates"],
        response["features"][0]["properties"]["description"],
    )  # писок с 10 ближайшими объектами


def bezhenc(city):
    map_params = {
        "apikey": "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3",
        "text": f"Пункты расселения беженцев {city}",
        "lang": "ru_RU",
        "results": "10",
    }

    response = requests.get(map_api_server, params=map_params).json()
    return (
        response["features"][0]["geometry"]["coordinates"],
        response["features"][0]["properties"]["description"],
    )  # писок с 10 ближайшими объектами


def bomba(city):
    map_params = {
        "apikey": "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3",
        "text": f"Бомбоубежища {city}",
        "lang": "ru_RU",
        "results": "10",
    }

    response = requests.get(map_api_server, params=map_params).json()
    return (
        response["features"][0]["geometry"]["coordinates"],
        response["features"][0]["properties"]["description"],
    )  # писок с 10 ближайшими объектами


if __name__ == "__main__":
    map_api_server = "https://search-maps.yandex.ru/v1/"
    print(get_hospital("Ростов на Дону"))
