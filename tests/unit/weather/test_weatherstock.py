import os

from denis_hodge_podge_bot.weather.weatherstock import weather_data_from_response

this_dir = os.path.dirname(__file__)


def test_weather_data_from_json():
    with open(os.path.join(this_dir, 'moscow_response.json'), mode='r',
              encoding='utf-8') as f:
        response = f.read()
    data = weather_data_from_response(response)
    assert data.location == 'Москва'
    assert data.temperature == 18
    assert data.humidity == 28
    assert data.wind_speed == 19
