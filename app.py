from flask import Flask, request
import os
import psycopg2
from dotenv import load_dotenv
from datetime import datetime, timezone


CREATE_ROOM_TABLES = (
    """CREATE TABLE IF NOT EXISTS rooms (id SERIAL PRIMARY KEY, name TEXT);"""
)

CREATE_TEMPS_TABLE = """CREATE TABLE IF NOT EXISTS temperatures (
    room_id INTEGER,
    temperature REAL,
    date TIMESTAMP,
    FOREIGN KEY (room_id) REFERENCES rooms (id) ON DELETE CASCADE
);"""


INSERT_ROOM_RETURN_ID = "INSERT INTO rooms (name) VALUES (%s) RETURNING id;"

INSERT_TEMP = (
    "INSERT INTO temperatures (room_id, temperature, date) VALUES (%s, %s, %s);"
)


GLOBAL_NUMBER_OF_DAYS = {
    "query": "SELECT COUNT(DISTINCT DATE(date)) AS days FROM temperatures;"
}

GLOBAL_AVG = {
    "query": "SELECT AVG(temperature) as average FROM temperatures;"
}


load_dotenv()

app=Flask(__name__)
url=os.getenv("DB_URL")
connection = psycopg2.connect(url)

app = Flask(__name__)

@app.route("/api/api/room", methods=["POST"])
def create_room():
    data = request.get_json()
    name = data["name"]

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_ROOM_TABLES)
            cursor.execute(INSERT_ROOM_RETURN_ID, (name,))
            room_id = cursor.fetchone()[0]
    return {"id": room_id, "message": f"Room {name} created."}, 201


@app.route("/api/api/room", methods=["POST"])
def add_temp():
    data = request.get_json()
    temp = data["name"]
    room_id = data["room"]

    try:
        date = datetime.strptime(data["date"], "%m-%d-%y %H:%M:%S")

    except KeyError:
        date = datetime.now(timezone.utc)

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_TEMPS_TABLE)
            cursor.execute(INSERT_TEMP, (room_id, temp, date))

    return {"message": "Temperature added"}, 201

if __name__ == '__main__':
    app.run()