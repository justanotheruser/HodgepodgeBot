import json
import logging

from aiohttp import ClientSession

from denis_hodge_podge_bot.config import config

EXCHANGE_RATES_DATA_URL = 'https://api.apilayer.com/exchangerates_data/convert'

logger = logging.getLogger('HodgepodgeBot')


def parse_response(response: str) -> float:
    json_data = json.loads(response)
    if json_data['success']:
        return float(json_data['result'])


async def convert(session: ClientSession, amount: float, from_currency: str, to_currency: str) -> float:
    params = {'amount': amount, 'from': from_currency, 'to': to_currency}
    logger.info(f'Requesting Exchange Rates Data API with params {params}')
    headers = {
        'apikey': config.exchange_rate_data_api_access_key.get_secret_value()
    }
    async with session.get(EXCHANGE_RATES_DATA_URL, params=params, headers=headers) as response:
        return parse_response(await response.text())
