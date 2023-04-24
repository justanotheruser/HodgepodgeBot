class CurrencyExchangeError(Exception):
    """Basic exception for error in the process of currency conversion"""


class ExchangeFormatError(CurrencyExchangeError):
    """Exchange request has invalid format"""


class UnknownCurrencyError(CurrencyExchangeError):
    """Failed to identify currency"""
