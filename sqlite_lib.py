import logging
import os
import sqlite3
from sqlite3 import Error

DB_FILE = './tmDB.db'
INIT_TABLE = """CREATE TABLE IF NOT EXISTS TM_DATA (timestamp TEXT primary key, temperature REAL, humidity REAL)"""


def initialize():
    """ Create the database file and initialize the table if not exist """
    global conn
    if not os.path.isfile(DB_FILE):
        try:
            conn = sqlite3.connect(DB_FILE)
            conn.cursor().execute(INIT_TABLE)
            conn.commit()
        except Error as e:
            print(e)
        finally:
            conn.close()
    else:
        pass


# Insert data to the project database file
def insert_data(timestamp, temperature, humidity):
    connection = sqlite3.connect(DB_FILE)
    try:
        with connection:
            connection.execute(
                """INSERT INTO TM_DATA (timestamp, temperature, humidity) 
                VALUES (?, ?, ?)""", (timestamp, temperature, humidity))
    except sqlite3.Error as error:
        logging.error("Database Error: %s", error)
    finally:
        connection.close()


def query_all_th_data():
    global conn
    try:
        conn = sqlite3.connect(DB_FILE)
        exe = conn.cursor()
        c = exe.execute('select * from TM_DATA')
        for row in c:
            print('TimeSlot:' + row[0])
            print('Temperature:' + str(row[1]))
            print('Humidity:' + str(row[2]))

    except Error as e:
        print(e)
    finally:
        conn.close()


# Query min max temperature and humidity and order by data
def get_csv_data():
    data = []
    global conn
    try:
        conn = sqlite3.connect(DB_FILE)
        exe = conn.cursor()
        c = exe.execute(
            """SELECT strftime('%Y-%m-%d',timestamp),MIN(temperature),MAX(temperature),MIN(humidity),MAX(humidity)
            FROM TM_DATA
            GROUP BY DATE(timestamp)
            ORDER BY DATE(timestamp)""")

        for row in c:
            data.append(row)
    except Error as e:
        print(e)
    finally:
        conn.close()
        return data
