from typing import Optional, Dict, Union
from django.core.cache import cache
from configparser import ConfigParser
import requests
from ShipTrackWeather import logger


class WeatherService:
    """
    Provides methods to fetch weather data using an external API and configuration settings.
    """
    CONFIG_FILE : str = "environment.ini"

    @staticmethod
    def read_config() -> Optional[ConfigParser]:
        """
        Reads the configuration settings from the specified configuration file.

        Returns:
            ConfigParser or None: Configuration settings or None if an exception occurs during parsing.
        """
        parser = ConfigParser()
        try:
            parser.read(WeatherService.CONFIG_FILE)
            return parser
        except Exception as e:
            logger.exception(f"{e} occurred!")
            return None

    @staticmethod
    def get_weather_data(location: str, section: str = "API") -> Optional[Dict[str, Union[str, int]]]:
        """
        Fetches weather data for a given location using an external API.

        Parameters:
            location (str): The location for which weather data is requested.
            section (str, optional): The section name in the configuration file containing API settings.
                                     Default is "API".

        Returns:
            dict or None: Weather data as a dictionary or None if the API request was unsuccessful
                          or configuration settings are missing.
        """
        parser = WeatherService.read_config()
        if parser and parser.has_section(section):
            base_url = parser.get(section, "base_url")
            units = parser.get(section, "units")
            APPID = parser.get(section, "APPID")

            cached_weather_data: Optional[Dict[str, Union[str, int]]] = cache.get(location)

            if cached_weather_data:
                return cached_weather_data
            else:
                weather_api_url: str = f"{base_url}?q={location}&units={units}&APPID={APPID}"
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
