# Simple Weather API

This is a barebones RESTful API serving weather data, leveraging the OpenWeather weather API built using FastAPI. Cache is stored on a local database object.

## Installation

Clone this repository to your local machine:
```bash
git clone https://github.com/mattbrowne2/WeatherAPI.git
```

Change into the project directory:

```bash
cd WeatherAPI
```

Install the project dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
uvicorn main:app --reload
```

Alternatively, deploy with Docker:

```bash
docker build -t weatherapi
```

Run the container:

```bash
docker run -d -p 8000:8000 --name weatherapi_container weatherapi
```

Via either method, the application will start and be available at http://localhost:8000 (or on whatever port listed in Dockerfile)

## API Endpoint

```http
GET /weather/{city_name}/{DD-MM-YYYY}
```

Returns the following weather data for the selected city and day provided:

* Minimum temperature (celsius)
* Maximum temperature (celcius)
* Average temperature (celcius)
* Humidity (g/Kg)


### Example API Call:

```http
GET /weather/{city_name}/{DD/MM/YYYY}
```
Returns data for a specific City and Date:

```console
curl http://127.0.0.1:8000/weather/london/12-08-2024 -H "Accept: application/json"
```
Response:
```json
{
    "date":"2024-08-12",
    "max_temp":33.64,
    "humidity":53.0,
    "min_temp":29.87,
    "id":1,
    "city":"london",
    "avg_temp":31.755000000000003
}
```

## Pytests

The following tests included within /tests/test_main.py/:

* test_get_weather_valid_city()
    > Validates entered City is valid using Data Object in schema.py
* test_get_weather_invalid_city()
    > Asserts a status code of 404 for an invalid city in API call
* test_get_weather_invalid_date()
    > Asserts a status code of 400 with an invalid date in API call

To run the tests simply change to the WeatherAPI dir and call:

```bash
pytest
```

While the application is running.

### Thoughts & What didn't work

* I thoroughly enjoyed this task - it was a beneficial opportunity to refamiliarise myself the FastAPI library having only used Flask for over a year.
* I initially tried to use the OneCall API plus the Geocoder API before realising these were pay-walled. Switching to the simple weather API was luckily very swift.