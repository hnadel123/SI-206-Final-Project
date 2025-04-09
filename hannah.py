def fetch_weather_data(timestamp):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 34.0522,
        "longitude": -118.2437,
        "hourly": "temperature_2m,precipitation,relative_humidity_2m",
        "timezone": "America/Los_Angeles"
    }

    response = requests.get(url, params=params)
    data = response.json()

    now = datetime.now().strftime("%Y-%m-%dT%H:00")
    times = data["hourly"]["time"]

    try:
        idx = times.index(now)
    except ValueError:
        print("Current hour's weather not available.")
        return

    temperature = data["hourly"]["temperature_2m"][idx]
    precipitation = data["hourly"]["precipitation"][idx]
    humidity = data["hourly"]["relative_humidity_2m"][idx]
    condition = "Rainy" if precipitation > 0 else "Clear"

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute('''INSERT INTO Weather (temperature, condition, humidity, precipitation, timestamp)
                   VALUES (?, ?, ?, ?, ?)''', 
                   (temperature, condition, humidity, precipitation, timestamp))

    conn.commit()
    conn.close()
