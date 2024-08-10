from pydantic import BaseModel
from datetime import date


class WeatherBase(BaseModel):
    city: str
    date: date

class WeatherResponse(WeatherBase):
    min_temp: float
    max_temp: float
    avg_temp: float
    humidity: float