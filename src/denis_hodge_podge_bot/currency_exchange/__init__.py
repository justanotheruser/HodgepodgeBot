import re
from typing import Optional

# TODO: separate code and data
currencies_in_genitive_case = {'EUR': ['€', 'евро'], 'USD': ['$', 'дол', 'долларов', 'долларов сша'],
                               'RUB': ['₽', 'руб', 'рублей', 'российских рублей'], 'JPY': ['японских йен'], 'CNY': ['китайских юаней'],
                               'GBP': ['фунтов стерлингов'], 'CHF': ['швейцарских франков'],
                               'AUD': ['австралийских долларов'], 'CAD': ['канадских долларов'],
                               'NZD': ['новозеландских долларов'], 'HKD': ['гонконгских долларов'],
                               'SGD': ['сингапурских долларов'], 'KRW': ['вон республики корея'],
                               'INR': ['индийских рупий'], 'TRY': ['турецких лир'], 'ZAR': ['южноафриканских рэндов'],
                               'BRL': ['бразильских реалов'], 'MXN': ['мексиканских песо'], 'THB': ['тайских батов'],
                               'SEK': ['шведских крон'], 'NOK': ['норвежских крон'], 'DKK': ['датских крон'],
                               'CZK': ['чешских крон'], 'HUF': ['венгерских форинтов'], 'PLN': ['польских злотых'],
                               'ILS': ['новых израильских шекелей'], 'AED': ['дирхамов оаэ'],
                               'BHD': ['бахрейнских динаров'], 'OMR': ['оманских риалов'],
                               'KWD': ['кувейтских динаров'], 'QAR': ['катарских риалов'], 'SAR': ['саудовских риялов'],
                               'UAH': ['украинских гривен']}
currencies_in_prepositional_case = {'EUR': ['€', 'евро'], 'USD': ['$', 'дол', 'долларах', 'долларах сша'],
                                    'RUB': ['₽', 'руб', 'рублях'], 'JPY': ['иенах'], 'CNY': ['юанях'],
                                    'GBP': ['фунтах стерлингов'], 'CHF': ['франках'], 'AUD': ['австралийских долларах'],
                                    'CAD': ['канадских долларах'], 'NZD': ['новозеландских долларах'],
                                    'HKD': ['гонконгских долларах'], 'SGD': ['долларах cингапура'], 'KRW': ['вонах'],
                                    'INR': ['рупиях'], 'TRY': ['лирах'], 'ZAR': ['рэндах'], 'BRL': ['реалах'],
                                    'MXN': ['песо'], 'THB': ['батах'], 'SEK': ['шведских кронах'],
                                    'NOK': ['норвежских кронах'], 'DKK': ['датских кронах'], 'CZK': ['чешских кронах'],
                                    'HUF': ['форинтах'], 'PLN': ['злотых'], 'ILS': ['шекелях'], 'AED': ['дирхамах'],
                                    'BHD': ['бахрейнских динарах'], 'OMR': ['риалах'], 'KWD': ['кувейтских динарах'],
                                    'QAR': ['риалах'], 'SAR': ['риялах'], 'UAH': ['гривнах']}
currency_codes = list(currencies_in_prepositional_case.keys())


def identify_source_currency(currency: str):
    currency = currency.upper()
    if currency in currency_codes:
        return currency
    currency = currency.lower()
    for code, genitive_case_names in currencies_in_genitive_case.items():
        if currency in genitive_case_names:
            return code


def identify_target_currency(currency: str) -> Optional[str]:
    currency = currency.upper()
    if currency in currency_codes:
        return currency
    currency = currency.lower()
    for code, prepositional_case_names in currencies_in_prepositional_case.items():
        if currency in prepositional_case_names:
            return code
    return None


exchange_pattern = re.compile(r'(\d[\d\s]+([.,]\d+)?)\s?(₽|€|\$|[а-я\s]+(?=во?\s))(\s?во?\s(₽|€|\$|[а-я\s]+))')


class ExchangeFormatError(Exception):
    """Exception request has invalid format"""


def split_value_source_target(exchange_request: str) -> tuple[float, str, str]:
    match = exchange_pattern.match(exchange_request)
    if not match:
        raise ExchangeFormatError("Неправильный формат")
    value_str = match.group(1)
    source = match.group(3).rstrip()
    target = match.group(5)
    value_str = re.sub(r'\s', '', value_str.replace(',', '.'))
    value = float(value_str)
    return value, source, target
