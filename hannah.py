import requests
import time
import sqlite3

DB_NAME = "weathering_the_wait_time.db"
print(DB_NAME)

def fetch_weather_data(timestamp):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": -180,
        "longitude": -180,
        "current": ["temperature_2m", "precipitation", "rain", "cloud_cover"],
        "forecast_days": 1
    }
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute('''SELECT latitude, longitude FROM DisneyParks''')
    results = cur.fetchall()

    for (lat, lon) in results:
        params['latitude'] = lat
        params['longitude'] = lon
        response = requests.get(url, params=params)
        data = response.json()

        cur.execute(''' 
        INSERT INTO Weather (latitude, longitude, temperature, precipitation, rain, cloud_cover, time_accessed)
        VALUES (?, ?, ?, ?, ?, ?, ?)''',
        (lat, lon, data['current']['temperature_2m'], 
         data['current']['precipitation'], data['current']['rain'], data['current']['cloud_cover'], timestamp))

    conn.commit()
    conn.close()
