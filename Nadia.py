def fetch_disneyland_data():
    url = 'https://queue-times.com/parks/16/queue_times.json'
    response = requests.get(url)
    data = response.json()

    conn = sqlite3.connect(NAME)
    cur = conn.cursor()

    for land in data['lands']:
        for ride in land['rides'][:25]: 
            ride_name = ride['name']
            wait_time = ride['wait_time']
            ride_status = ride.get('status', 'Unknown')
            ride_type = ride.get('type', 'Unknown')
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

            cur.execute('''INSERT INTO DisneylandRides (ride_name, wait_time, ride_status, ride_type, timestamp)
                           VALUES (?, ?, ?, ?, ?)''', (ride_name, wait_time, ride_status, ride_type, timestamp))

    conn.commit()
    conn.close()