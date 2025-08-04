from transform import transform_weather_data
from extract import fetch_weather_data
import os

def main():

    lat = 54.860357
    lon = 83.078579
    start = "2025-07-20"
    end = "2025-07-22"

    raw_data = fetch_weather_data(lat, lon, start, end)
    transformed_data = transform_weather_data(raw_data)
    filename = f"weather_data_{lat}_{lon}_{start}_{end}.csv"
    data_dir = "data/transform"
    os.makedirs(data_dir, exist_ok=True)
    transformed_data.to_csv(filename, index=False, encoding="utf-8", float_format="%.2f")

if __name__ == "__main__":
    main()


    