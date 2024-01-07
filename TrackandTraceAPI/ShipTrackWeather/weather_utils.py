from django.core.cache import cache
from configparser import ConfigParser
import requests
from ShipTrackWeather import logger


class WeatherService:
    CONFIG_FILE = "environment.ini"

    @staticmethod
    def read_config():
        parser = ConfigParser()
        try:
            parser.read(WeatherService.CONFIG_FILE)
            return parser
        except Exception as e:
            logger.exception(f"{e} occurred!")
            return None

    @staticmethod
    def get_weather_data(location, section="API"):
        parser = WeatherService.read_config()
        if parser and parser.has_section(section):
            base_url = parser.get(section, "base_url")
            units = parser.get(section, "units")
            APPID = parser.get(section, "APPID")

            cached_weather_data = cache.get(location)

            if cached_weather_data:
                return cached_weather_data
            else:
                weather_api_url = f"{base_url}?q={location}&units={units}&APPID={APPID}"
                response = requests.get(weather_api_url)

                if response.status_code == 200:
                    weather_data = response.json()
                    cache.set(location, weather_data, timeout=7200)
                    logger.info(f"Weather data is: {weather_data}")
                    return weather_data
                else:
                    logger.warning(f"Not successful api request with code: {response.status_code}")
                    return None
        else:
            logger.warning(f"There is either no {WeatherService.CONFIG_FILE} file or no {section} section!")
            return None
