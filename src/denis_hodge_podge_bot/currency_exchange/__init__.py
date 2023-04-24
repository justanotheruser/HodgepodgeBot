import os
import re
from typing import Optional

import pandas as pd


class CurrencyCodeConverter:
    def __init__(self, currencies_csv: str):
        currencies_csv = os.path.join(os.path.dirname(__file__), currencies_csv)
        self.currencies_df = pd.read_csv(currencies_csv, index_col=0)
        self.currency_codes = list(self.currencies_df.index)

    def identify_source_currency(self, currency: str):
        currency = currency.upper()
        if currency in self.currency_codes:
            return currency
        currency = currency.lower()
        for code in self.currency_codes:
            if currency in self.currencies_df['genitive_case'][code]:
                return code
        # TODO: check Levenshtein distance of 1 for russian words

    def identify_target_currency(self, currency: str) -> Optional[str]:
        currency = currency.upper()
        if currency in self.currency_codes:
            return currency
        currency = currency.lower()
        for code in self.currency_codes:
            if currency in self.currencies_df['prepositional_case'][code]:
                return code
        # TODO: check Levenshtein distance of 1 for russian words


currency_code_converter = CurrencyCodeConverter('currencies.csv')

# TODO: allow three-letter codes
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
