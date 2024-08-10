from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schema import UserCreate, UserUpdate
import requests
from datetime import datetime
from . import models, schema, database


app = FastAPI()

API_KEY = '2c192805e2247d175f009a452f6d75c5'

BASE_URL = 'https://api.openweathermap.org/data/3.0/onecall'

def get_weather_from_api(city:str):
    # using OpenWeather's Geocode API, fetch the lon and lat for a city:
    geocode_url = f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}'
    geocode_response = requests.get(geocode_url).json()
    if not geocode_response:
        raise HTTPException(status_code=404, detail="City Provided Not Found")
    
    lat = geocode_response[0]["lat"]
    lon = geocode_response[0]["lon"]
    
    weather_url = f"{BASE_URL}?lat={lat}&lon={lon}&exclude=hourly,minutely,current&appid={API_KEY}&units=metric"
    weather_response = requests.get(weather_url).json()
    return weather_response

def get_weather_data(city:str, date:datetime, db:Session):
    # check if data has already been cached:
    
    weather = db.query(models.Weather).filter(models.Weather.city == city, models.Weather.date == date.date()).first()
    if weather:
        return weather
    
    # fetch data from OpenWeather API if not cached:
    
    weather_response = get_weather_from_api(city)
    
    day_data = next((day for day in weather_response['daily'] if datetime.fromtimestamp(day['dt']).date() == date.date()), None)
    
    if not day_data:
        raise HTTPException(status_code=404, detail="No data for the given date")  

    min_temp = day_data["temp"]["min"]
    max_temp = day_data['temp']['max']
    avg_temp = (min_temp + max_temp) / 2
    humidity = day_data['humidity']
    
    weather = models.Weather(city=city, date=date.date(), min_temp=min_temp, max_temp=max_temp, avg_temp=avg_temp, humidity=humidity)
    db.add(weather)
    db.commit()
    db.refresh(weather)
    return weather

@app.get("/weather/{city}/{date}", response_model=schema.WeatherResponse)
def read_weather(city:str, date:str, db: Session = Depends(database.get_db)):
    date_obj = datetime.strftime(date, '%Y%m-%d')
    weather = get_weather_data(city, date_obj, db)
    return weather


