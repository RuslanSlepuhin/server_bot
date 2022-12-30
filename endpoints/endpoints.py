import configparser
import os
import psycopg2
from flask import Flask
# from db_operations.scraping_db import DataBaseOperations

config = configparser.ConfigParser()
config.read("./../settings/config.ini")

database = config['DB_local_clone']['database']
user = config['DB_local_clone']['user']
password = config['DB_local_clone']['password']
host = config['DB_local_clone']['host']
port = config['DB_local_clone']['port']

con = psycopg2.connect(
    database=database,
    user=user,
    password=password,
    host=host,
    port=port
)
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello World"

@app.route("/get")
def hello_world2():
    data = get_from_db()
    data = data[0]
    data_dict = {
        'id': data[0],
        'channel': data[1],
    }
    return data_dict

def get_from_db():
    cur = con.cursor()
    query = "SELECT * FROM admin_last_session"
    with con:
        cur.execute(query)
    response = cur.fetchall()
    return response

if __name__ == '__main__':
    app.run(host='localhost', port=int(os.environ.get('PORT', 5000)))
