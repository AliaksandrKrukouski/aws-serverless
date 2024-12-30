import requests

URL = "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"


def get_weather_forecast():
    url = URL
    response = requests.get(url)
    return response.json()


if __name__ == "__main__":
    print(get_weather_forecast())
