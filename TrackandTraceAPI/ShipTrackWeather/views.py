from django.shortcuts import render
from django.core.cache import cache
from configparser import ConfigParser
import requests

parser = ConfigParser()
parser.read("environment.ini")
base_url = parser["API"]["base_url"]
units = parser["API"]["units"]
APPID = parser["API"]["APPID"]


def get_weather_data(location):
    cached_weather_data = cache.get(location)

    if cached_weather_data:
        # If data exists in cache, return cached data
        return cached_weather_data
    else:
        # If not in cache, fetch data from the weather API
        weather_api_url = f"{base_url}?q={location}&units={units}&APPID={APPID}"
        response = requests.get(weather_api_url)

        if response.status_code == 200:
            weather_data = response.json()
            cache.set(location, weather_data, timeout=7200)
            return weather_data
        else:
            return None
