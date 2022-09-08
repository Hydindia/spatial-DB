import psycopg2

import urllib.request

import json

import timeit

# start execution timer
start = timeit.default_timer()

# establishing the connection
conn = psycopg2.connect(
    database="Project1", user='bob', password='admin', host='127.0.0.1', port='5432'
)
# Creating a cursor object using the cursor() method
cur = conn.cursor()

# create tables (if do not exist)
cur.execute('''
CREATE TABLE IF NOT EXISTS UFO (
    id TEXT PRIMARY KEY NOT NULL UNIQUE,
    datetime TEXT,
    city TEXT,
    state TEXT,
    country TEXT,
    shape TEXT,
    duration_sec TEXT,
    duration_hrs_min TEXT,
    comments TEXT,
    date_posted TEXT,
    latitude NUMERIC,
    longitude NUMERIC
)
''')

conn.commit()

file_url = "https://cs.msutexas.edu/~griffin/data/UfoData/ufos_export.json"
response = urllib.request.urlopen(file_url)

count = 0

while (True):
    data = response.readline()
    if data == b'':
        break
    data = json.loads(data.decode("utf-8"))
    print(data["_id"]["$oid"])

    # check if id is present in database
    cur.execute("SELECT id FROM UFO WHERE id = %s", (data['_id']['$oid'],))

    if (cur.fetchone() == None):
        count = count + 1
        print(str(count) + " : Inserting data => " + data['_id']['$oid'])
        # print(data)
        try:
            if (float(data['latitude'])):
                cur.execute("""
                            INSERT INTO UFO
                            (
                                id,
                                datetime,
                                city,
                                state,
                                country,
                                shape,
                                duration_sec,
                                duration_hrs_min,
                                comments,
                                date_posted,
                                latitude,
                                longitude
                            ) VALUES
                            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            """,
                            (
                                data['_id']['$oid'],
                                data['datetime'],
                                data['city'],
                                data['state'],
                                data['country'],
                                data['shape'],
                                data['duration (seconds)'],
                                data['duration (hours/min)'],
                                data['comments'],
                                data['date posted'],
                                data['latitude'],
                                data['longitude']
                            ))
                conn.commit()
        except:
            pass


# Closing the connection
conn.close()

## programme execution time ##
stop = timeit.default_timer()
total_time = stop-start
print('\n-----------------------')
print('Time: ', total_time)
print('-----------------------\n')

# Programme
# Execution Time : Time:  1052.9603083849997 Seconds
# No. of Records : 87999
