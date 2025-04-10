import requests
import time
import sqlite3

DB_NAME = "weathering_the_wait_time.db"
print(DB_NAME)

def fetch_disneyland_data(timestamp):
    parks = []
    url = 'https://queue-times.com/parks.json'
    response = requests.get(url)
    data = response.json()
    for park in data:
        if park['id'] == 2:
            for org in park['parks']:
                parks.append(org)
    
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    for org in parks:
        cur.execute('''
        INSERT OR IGNORE INTO DisneyParks (name, country, continent, latitude, longitude, timezone, api_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?)''', 
                    (org['name'], org['country'], org['continent'], org['latitude'], org['longitude'], org['timezone'], org['id'])
                    )
    conn.commit()

    cur.execute('''SELECT api_id, id FROM DisneyParks''')
    ids = cur.fetchall()
    inserted_count = 0
    done = False
    for id in ids:
        park_url = f'https://queue-times.com/parks/{id[0]}/queue_times.json'
        response = requests.get(park_url)
        data = response.json()

        for land in data['lands']:
            for ride in land['rides'][:25]:
                if inserted_count >= 25:
                    done = True
                    break

                cur.execute('''INSERT OR IGNORE INTO DisneyRides (name, park_id, status, wait_time, time_accessed)
                        VALUES (?, ?, ?, ?, ?)''',
                        (ride['name'], id[1], ride['is_open'], ride['wait_time'], timestamp)
                        )
                
                if cur.rowcount > 0:
                    inserted_count += 1
            if done:
                break

    conn.commit()
    conn.close()
