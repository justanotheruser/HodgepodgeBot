from denis_hodge_podge_bot.currency_exchange import split_value_source_target


def test_multiword_source_currency():
    value, source, target = split_value_source_target('12 долларов сша в рублях')
    assert value == 12
    assert source == 'долларов сша'
    assert target == 'рублях'


def test_multiword_target_currency():
    value, source, target = split_value_source_target('12 рублей в датских кронах')
    assert value == 12
    assert source == 'рублей'
    assert target == 'датских кронах'


def test_float_value():
    value, source, target = split_value_source_target('12.5 рублей в йенах')
    assert value == 12.5
    assert source == 'рублей'
    assert target == 'йенах'


def test_float_value_with_comma():
    value, source, target = split_value_source_target('13,76 долларов в тугриках')
    assert value == 13.76
    assert source == 'долларов'
    assert target == 'тугриках'


def test_vo():
    value, source, target = split_value_source_target('5 долларов во франках')
    assert value == 5
    assert source == 'долларов'
    assert target == 'франках'


def test_spaces_in_value():
    value, source, target = split_value_source_target('1 000 000 тугриков в рублях')
    assert value == 1000000
    assert source == 'тугриков'
    assert target == 'рублях'


def test_source_currency_symbol():
    value, source, target = split_value_source_target('100$ в рублях')
    assert value == 100
    assert source == '$'
    assert target == 'рублях'


def test_currency_symbols_with_space():
    value, source, target = split_value_source_target('100 € в ₽')
    assert value == 100
    assert source == '€'
    assert target == '₽'
