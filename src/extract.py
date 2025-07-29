import requests
import os
from datetime import datetime

def fetch_weather_data(latitude, longitude, start_date, end_date):
    base_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": "sunrise,sunset,daylight_duration",
        "hourly": "temperature_2m,relative_humidity_2m,dew_point_2m,apparent_temperature,"
                  "temperature_80m,temperature_120m,wind_speed_10m,wind_speed_80m,"
                  "wind_direction_10m,wind_direction_80m,visibility,evapotranspiration,"
                  "weather_code,soil_temperature_0cm,soil_temperature_6cm,rain,showers,snowfall",
        "timezone": "auto",
        "timeformat": "unixtime",
        "wind_speed_unit": "kn",
        "temperature_unit": "fahrenheit",
        "precipitation_unit": "inch",
        "start_date": start_date,
        "end_date": end_date
    }

    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        raw_data_dir = "data/raw"
        os.makedirs(raw_data_dir, exist_ok=True)

        filename = f"weather_{latitude}_{longitude}_{start_date}_{end_date}.json"
        filepath = os.path.join(raw_data_dir, filename)

        # Сохраняем JSON для отладки и повторного использования
        with open(filepath, 'w') as f:
            import json
            json.dump(data, f, indent=2)

        return data
    else:
        raise Exception(f"Ошибка при запросе: HTTP {response.status_code} - {response.text}")


