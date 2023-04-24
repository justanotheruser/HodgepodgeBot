from denis_hodge_podge_bot.currency_exchange import currency_code_converter, UnknownCurrencyError
import pytest


def test_valid_source_currency():
    currency_map = {
        '$': 'USD',
        'долларов': 'USD',
        '€': 'EUR',
        'руб': 'RUB',
        'rub': 'RUB',
        'рублей': 'RUB',
        'кувейтских динаров': 'KWD'
    }
    for user_input, currency_code in currency_map.items():
        assert currency_code == currency_code_converter.identify_source_currency(user_input)


def test_valid_target_currency():
    currency_map = {
        '$': 'USD',
        'долларах': 'USD',
        '€': 'EUR',
        'руб': 'RUB',
        'rub': 'RUB',
        'рублях': 'RUB',
        'кувейтских динарах': 'KWD'
    }
    for user_input, currency_code in currency_map.items():
        assert currency_code == currency_code_converter.identify_target_currency(user_input)


def test_invalid_source_currency():
    currency = 'мартышек'
    with pytest.raises(UnknownCurrencyError, match=f'Неизвестная валюта: "{currency}"'):
        currency_code_converter.identify_source_currency(currency)


def test_invalid_target_currency():
    currency = 'межгалактических кредитах'
    with pytest.raises(UnknownCurrencyError, match=f'Неизвестная валюта: "{currency}"'):
        currency_code_converter.identify_target_currency(currency)
