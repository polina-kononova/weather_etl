import unittest
import requests

class TestOpenMeteoAPI(unittest.TestCase):
    BASE_URL = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 55.0344,
        "longitude": 82.9434,
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
        "start_date": "2025-05-16",
        "end_date": "2025-05-30"
    }

    def test_api_response_status(self):
        response = requests.get(self.BASE_URL, params=self.params)
        self.assertEqual(response.status_code, 200, "API did not respond with status 200")

    def test_response_contains_expected_keys(self):
        response = requests.get(self.BASE_URL, params=self.params)
        data = response.json()
        self.assertIn("hourly", data, "Response JSON missing 'hourly' key")
        self.assertIn("daily", data, "Response JSON missing 'daily' key")

    def test_hourly_keys_exist(self):
        response = requests.get(self.BASE_URL, params=self.params)
        data = response.json()
        expected_hourly_keys = [
            "temperature_2m","relative_humidity_2m","dew_point_2m","apparent_temperature",
            "temperature_80m","temperature_120m","wind_speed_10m","wind_speed_80m",
            "wind_direction_10m","wind_direction_80m","visibility","evapotranspiration",
            "weather_code","soil_temperature_0cm","soil_temperature_6cm","rain","showers","snowfall"
        ]
        for key in expected_hourly_keys:
            self.assertIn(key, data["hourly"], f"Missing key '{key}' in hourly data")

    def test_daily_keys_exist(self):
        response = requests.get(self.BASE_URL, params=self.params)
        data = response.json()
        expected_daily_keys = ["sunrise", "sunset", "daylight_duration"]
        for key in expected_daily_keys:
            self.assertIn(key, data["daily"], f"Missing key '{key}' in daily data")

    def test_time_intervals(self):
        response = requests.get(self.BASE_URL, params=self.params)
        data = response.json()
        daily_times = data["daily"]["time"]
        # Проверяем, что даты в daily соответствуют ожидаемому интервалу (2025-05-16 по 2025-05-30)
        # Даты в unixtime, проверяем крайние значения
        start_unix = min(daily_times)
        end_unix = max(daily_times)
        import datetime
        start_date_expected = datetime.datetime(2025,5,16).timestamp()
        end_date_expected = datetime.datetime(2025,5,30).timestamp()

        self.assertGreaterEqual(start_unix, start_date_expected, "Start date in response is earlier than requested")
        self.assertLessEqual(end_unix, end_date_expected, "End date in response is later than requested")

if __name__ == "__main__":
    unittest.main()
