import psycopg2

from fastapi import FastAPI

app = FastAPI()

# establishing the connection
conn = psycopg2.connect(
    database="Project1", user='bob', password='admin', host='127.0.0.1', port='5432'
)
# Creating a cursor object using the cursor() method
cur = conn.cursor()


@app.get("/findAll")
# example : http://127.0.0.1:8000/findAll
def findAll():
    # return all data from database UFO table
    data = cur.execute("SELECT * FROM UFO")
    data = cur.fetchall()
    return data


@app.get("/findOne")
# example : http://127.0.0.1:8000/findOne?id=5d9de49a2ebe2da7d4d8460b
def findOne(id=None,
            city=None,
            state=None,
            country=None,
            shape=None,
            date_posted=None):

    if id is not None:
        data = cur.execute("SELECT * FROM UFO WHERE id = %s", (id,))
        data = cur.fetchone()
        return {
            "id": data[0],
            "datetime": data[1],
            "city": data[2],
            "state": data[3],
            "country": data[4],
            "shape": data[5],
            "duration (seconds)": data[6],
            "duration (hours/min)": data[7],
            "comments": data[8],
            "date posted": data[9],
            "latitude": data[10],
            "longitude": data[11]
        }

    elif city is not None:
        data = cur.execute("SELECT * FROM UFO WHERE city = %s", (city,))
        data = cur.fetchone()
        return {
            "id": data[0],
            "datetime": data[1],
            "city": data[2],
            "state": data[3],
            "country": data[4],
            "shape": data[5],
            "duration (seconds)": data[6],
            "duration (hours/min)": data[7],
            "comments": data[8],
            "date posted": data[9],
            "latitude": data[10],
            "longitude": data[11]
        }

    elif state is not None:
        data = cur.execute("SELECT * FROM UFO WHERE state = %s", (state,))
        data = cur.fetchone()
        return {
            "id": data[0],
            "datetime": data[1],
            "city": data[2],
            "state": data[3],
            "country": data[4],
            "shape": data[5],
            "duration (seconds)": data[6],
            "duration (hours/min)": data[7],
            "comments": data[8],
            "date posted": data[9],
            "latitude": data[10],
            "longitude": data[11]
        }

    elif country is not None:
        data = cur.execute("SELECT * FROM UFO WHERE country = %s", (country,))
        data = cur.fetchone()
        return {
            "id": data[0],
            "datetime": data[1],
            "city": data[2],
            "state": data[3],
            "country": data[4],
            "shape": data[5],
            "duration (seconds)": data[6],
            "duration (hours/min)": data[7],
            "comments": data[8],
            "date posted": data[9],
            "latitude": data[10],
            "longitude": data[11]
        }

    elif shape is not None:
        data = cur.execute("SELECT * FROM UFO WHERE shape = %s", (shape,))
        data = cur.fetchone()
        return {
            "id": data[0],
            "datetime": data[1],
            "city": data[2],
            "state": data[3],
            "country": data[4],
            "shape": data[5],
            "duration (seconds)": data[6],
            "duration (hours/min)": data[7],
            "comments": data[8],
            "date posted": data[9],
            "latitude": data[10],
            "longitude": data[11]
        }

    elif date_posted is not None:
        data = cur.execute(
            "SELECT * FROM UFO WHERE date_posted = %s", (date_posted,))
        data = cur.fetchone()
        return {
            "id": data[0],
            "datetime": data[1],
            "city": data[2],
            "state": data[3],
            "country": data[4],
            "shape": data[5],
            "duration (seconds)": data[6],
            "duration (hours/min)": data[7],
            "comments": data[8],
            "date posted": data[9],
            "latitude": data[10],
            "longitude": data[11]
        }

    else:
        return "Please provide correct parameter (e.g. id, city, state, country, shape, date_posted)"


@app.get("/findClosest")
# example : http://127.0.0.1:8000/findClosest?lat=28%20&lon=-99
def findClosest(lat=None, lon=None):
    if lat is not None and lon is not None:
        data = cur.execute(
            "SELECT * FROM UFO ORDER BY (latitude - %s)^2 + (longitude - %s)^2 LIMIT 1", (lat, lon))
        data = cur.fetchone()
        return {
            "id": data[0],
            "datetime": data[1],
            "city": data[2],
            "state": data[3],
            "country": data[4],
            "shape": data[5],
            "duration (seconds)": data[6],
            "duration (hours/min)": data[7],
            "comments": data[8],
            "date posted": data[9],
            "latitude": data[10],
            "longitude": data[11]
        }
    else:
        return "Please provide correct parameter (e.g. lat & lon)"
