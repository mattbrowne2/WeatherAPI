from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)

@pytest.fixture
def weather_test_response(monkeypatch):
    def mock_get_weather_api(city:str):
        return {
            "daily": [{
                "dt": 1692489600,
                "temp": {
                    "min": 20,
                    "max": 30
                },
                "humidity": 60
            }]
        }
    monkeypatch.setattr("main.get_weather_from_api", weather_test_response)

def weather_test_read(weather_test_response):
    response = client.get("/weather/London/2023-08-19")
    assert response.status_code == 200
    data = response.json()
    assert data["min_temp"] == 20
    assert data["max_temp"] == 30
    assert data["avg_temp"] == 25
    assert data["humidity"] == 60