import json
from transform import transform_weather_data
from extract import fetch_weather_data

def save_to_csv(dataframe, output_path):
    """Сохраняет DataFrame в CSV-файл"""
    dataframe.to_csv(output_path, index=False)


def main():

    lat = 55.0344
    lon = 82.9434
    start = "2025-06-16"
    end = "2025-06-30"
    raw_data = fetch_weather_data(lat, lon, start, end)
    
    OUTPUT_CSV = 'weather_forecast.csv'
    transformed_data = transform_weather_data(raw_data)
    save_to_csv(transformed_data, OUTPUT_CSV)

if __name__ == "__main__":
    main()