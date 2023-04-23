from dataclasses import dataclass


@dataclass
class WeatherData:
    location: str
    # Celsius
    temperature: int
    # Percents
    humidity: int
    # Km/h
    wind_speed: int
    description: str
