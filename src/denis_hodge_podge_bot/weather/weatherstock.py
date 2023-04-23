import json
import logging

from aiohttp import ClientSession

from denis_hodge_podge_bot.config import config
from denis_hodge_podge_bot.weather.types import WeatherData

WEATHERSTACK_URL = 'http://api.weatherstack.com/current'

logger = logging.getLogger('HodgepodgeBot')


def weather_data_from_response(response: str) -> WeatherData:
    json_data = json.loads(response)
    return WeatherData(location=json_data['location']['name'],
                       temperature=json_data['current']['temperature'],
                       humidity=json_data['current']['humidity'],
                       wind_speed=json_data['current']['wind_speed'],
                       description='placeholder')


async def get_weather(session: ClientSession, city: str):
    weatherstack_params = {'units': 'm', 'query': city}
    logger.info(f'Requesting Weatherstack with params {weatherstack_params}')
    weatherstack_params['access_key'] = config.weatherstack_api_access_key.get_secret_value()
    async with session.get(WEATHERSTACK_URL, params=weatherstack_params) as response:
        return weather_data_from_response(await response.text())
