import pandas as pd
from datetime import datetime

# Вспомогательные функции конвертации
def fahrenheit_to_celsius(f_temp):
    """Конвертация °F в °C"""
    return (f_temp - 32) * 5/9

def unix_to_iso(unix_time):
    """Преобразование Unix времени в ISO 8601"""
    return datetime.utcfromtimestamp(unix_time).isoformat() + 'Z'

# Основная функция трансформации
def transform_weather_data(data):
    """Преобразует сырые данные погоды в структурированный DataFrame"""
    # Создание DataFrame для почасовых данных
    hourly = pd.DataFrame(data['hourly'])
    hourly['time'] = pd.to_datetime(hourly['time'], unit='s')
    hourly['date'] = hourly['time'].dt.date
    
    # Создание DataFrame для ежедневных данных
    daily = pd.DataFrame(data['daily'])
    daily['time'] = pd.to_datetime(daily['time'], unit='s').dt.date
    daily['sunrise_iso'] = daily['sunrise'].apply(unix_to_iso)
    daily['sunset_iso'] = daily['sunset'].apply(unix_to_iso)
    daily['daylight_hours'] = (daily['sunset'] - daily['sunrise']) / 3600
    
    # Конвертация единиц измерения только для температур
    temp_cols = ['temperature_2m', 'apparent_temperature', 'temperature_80m', 'temperature_120m']
    for col in temp_cols:
        if col in hourly.columns:
            hourly[f'{col}_celsius'] = hourly[col].apply(fahrenheit_to_celsius)
    
    # Агрегация за 24 часа только для температур
    agg_24h = {}
    if 'temperature_2m_celsius' in hourly.columns:
        agg_24h['temperature_2m_celsius'] = 'mean'
    if 'apparent_temperature_celsius' in hourly.columns:
        agg_24h['apparent_temperature_celsius'] = 'mean'
    if 'temperature_80m_celsius' in hourly.columns:
        agg_24h['temperature_80m_celsius'] = 'mean'
    if 'temperature_120m_celsius' in hourly.columns:
        agg_24h['temperature_120m_celsius'] = 'mean'
    
    daily_agg_24h = hourly.groupby('date').agg(agg_24h).reset_index()
    
    # Переименование колонок для 24-часовой агрегации
    new_names_24h = {
        'temperature_2m_celsius': 'avg_temperature_2m_24h',
        'apparent_temperature_celsius': 'avg_apparent_temperature_24h',
        'temperature_80m_celsius': 'avg_temperature_80m_24h',
        'temperature_120m_celsius': 'avg_temperature_120m_24h'
    }
    daily_agg_24h = daily_agg_24h.rename(columns=new_names_24h)
    
    # Агрегация за световой день только для температур
    daily_agg_daylight = []
    for _, day in daily.iterrows():
        day_hours = hourly[hourly['date'] == day['time']]
        
        if not day_hours.empty:
            daylight_agg = {'date': day['time']}
            
            if 'temperature_2m_celsius' in hourly.columns:
                daylight_agg['avg_temperature_2m_daylight'] = day_hours['temperature_2m_celsius'].mean()
            if 'apparent_temperature_celsius' in hourly.columns:
                daylight_agg['avg_apparent_temperature_daylight'] = day_hours['apparent_temperature_celsius'].mean()
            if 'temperature_80m_celsius' in hourly.columns:
                daylight_agg['avg_temperature_80m_daylight'] = day_hours['temperature_80m_celsius'].mean()
            if 'temperature_120m_celsius' in hourly.columns:
                daylight_agg['avg_temperature_120m_daylight'] = day_hours['temperature_120m_celsius'].mean()
            
            daily_agg_daylight.append(daylight_agg)
    
    daily_agg_daylight_df = pd.DataFrame(daily_agg_daylight)
    
    # Объединение всех данных
    result = daily
    if not daily_agg_24h.empty:
        result = result.merge(daily_agg_24h, left_on='time', right_on='date', how='left')
    if not daily_agg_daylight_df.empty:
        result = result.merge(daily_agg_daylight_df, on='date', how='left')
    
    # Формирование финального набора колонок
    final_columns = ['date', 'sunrise_iso', 'sunset_iso', 'daylight_hours']
    
    # Добавляем только те колонки, которые существуют
    for col in [
        'avg_temperature_2m_24h', 
        'avg_apparent_temperature_24h',
        'avg_temperature_80m_24h',
        'avg_temperature_120m_24h',
        'avg_temperature_2m_daylight',
        'avg_apparent_temperature_daylight',
        'avg_temperature_80m_daylight',
        'avg_temperature_120m_daylight'
    ]:
        if col in result.columns:
            final_columns.append(col)
    
    return result[final_columns]