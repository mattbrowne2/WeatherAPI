from fastapi.testclient import TestClient
from main import app
from app.schema import WeatherResponse

client = TestClient(app)

def test_get_weather_valid_city():
    
    '''
        Validate entered city is valid using Data Object in Schema
    '''
    
    response = client.get('/weather/London/09-08-2024')
    assert response.status_code == 200
    
    # Validate response schema:
    
    data = response.json()
    weather_response = WeatherResponse(**data)
    
    assert weather_response.city == "London"
    assert isinstance(weather_response.min_temp, float)
    assert isinstance(weather_response.max_temp, float)
    assert isinstance(weather_response.avg_temp, float)
    assert isinstance(weather_response.humidity, float)

def weather_test_read(weather_test_response):
    response = client.get("/weather/London/2023-08-11")
    assert response.status_code == 200
    data = response.json()
    assert "city" in data
    assert data["city"] == "London"
    assert "min_temp" in data
    assert "max_temp" in data
    assert "avg_temp" in data
    assert "humidity" in data
    
def test_get_weather_invalid_city():
    response = client.get("/weather/InvalidCity/11-08-2024")
    assert response.status_code == 404

def test_get_weather_invalid_date():
    response = client.get("/weather/London/invalid-date")
    assert response.status_code == 400
    assert response.json() == {"detail": "Date format should be DD-MM-YYYY"}

