from flask import Flask
import os
import psycopg2
# from dotenv 

CREATE_ROOM_TABLES = (
    """CREATE TABLE IF NOT EXISTS rooms (id SERIAL PRIMARY KEY, name TEXT)"""
)

app = Flask(__name__)
url = os.getenv("DB_URL")
connection = psycopg2.connect(url)

@app.route('/')
def home():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run()
