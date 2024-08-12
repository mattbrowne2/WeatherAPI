from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db, Base, engine
from app.models import Weather
from app.schema import WeatherBase, WeatherResponse
import requests
from datetime import datetime
from contextlib import asynccontextmanager




API_KEY = '2c192805e2247d175f009a452f6d75c5'

BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown Logic
    Base.metadata.drop_all(bind=engine)


app = FastAPI(lifespan=lifespan)


async def get_weather_from_api(city:str) -> dict:
    
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }
    
    response = requests.get(BASE_URL, params=params)
    print(response)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching data from openweather API")
    return response.json()


@app.get("/weather/{city}/{specific_date}")
async def get_weather(city: str, specific_date: str, db: Session = Depends(get_db)):
    # Convert date string to datetime object
    try:
        date_obj = datetime.strptime(specific_date, "%d-%m-%Y").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Date format should be DD-MM-YYYY")

    # Check if data is already stored in cache
    cached_weather = db.query(Weather).filter(
        Weather.city == city,
        Weather.date == date_obj
    ).first()

    if cached_weather:
        print("using cached weather") # print statement to check if cache is being loaded
        return cached_weather

    # Fetch weather data from OpenWeather API
    weather_data = (await get_weather_from_api(city))

    # Extract data from response
    min_temp = weather_data["main"]["temp_min"]
    max_temp = weather_data["main"]["temp_max"]
    avg_temp = (min_temp + max_temp) / 2
    humidity = weather_data["main"]["humidity"]

    # Cache data in db
    weather = Weather(
        city=city,
        date=date_obj,
        min_temp=min_temp,
        max_temp=max_temp,
        avg_temp=avg_temp,
        humidity=humidity
    )
    db.add(weather)
    db.commit()
    db.refresh(weather)

    return WeatherResponse(
        city=weather.city,
        date=weather.date,
        min_temp=weather.min_temp,
        max_temp=weather.max_temp,
        avg_temp=weather.avg_temp,
        humidity=weather.humidity
    )