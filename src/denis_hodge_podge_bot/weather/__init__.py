import os

import pandas as pd


class WeatherCodeConverter:
    def __init__(self, csv_file: str):
        weather_cond_codes_file = os.path.join(os.path.dirname(__file__), csv_file)
        self.weather_codes = pd.read_csv(weather_cond_codes_file, index_col='overhead_code')

    def get_description(self, code: int, is_day: bool):
        col = 'trans_text_day' if is_day else 'trans_text_night'
        try:
            return self.weather_codes.loc[code][col]
        except KeyError:
            return ''


weather_code_ru_converter = WeatherCodeConverter('weather_condition_codes_ru.csv')
