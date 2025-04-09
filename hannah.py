def fetch_weather_data():
    url = 'http://api.weatherstack.com/current?access_key=114493980920155d0343dfc9594ed16c&query=Anaheim'
    response = requests.get(url)
    data = response.json()['current']

    temperature = data['temperature']
    condition = data['weather_descriptions'][0]
    wind_speed = data['wind_speed'] 
    humidity = data['humidity']
    precipitation = data['precip']
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute('''INSERT INTO Weather (temperature, condition, wind_speed, humidity, precipitation, timestamp)
                   VALUES (?, ?, ?, ?, ?, ?)''', (temperature, condition, wind_speed, humidity, precipitation, timestamp))

    conn.commit()
    conn.close()