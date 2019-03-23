import sqlite3
from sqlite3 import Error
import os
import datetime

""" check if the db file exist otherwise init with a new one """

DB_FILE = 'tmDB.db'
INIT_TABLE = 'CREATE TABLE IF NOT EXISTS TM_DATA (timeslot TEXT primary key, temperature REAL, humidity REAL);'


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


def insert_data(time, temp, humi):
    global conn
    try:
        conn = sqlite3.connect(DB_FILE)
        para = (time, temp, humi)
        conn.cursor().execute('INSERT INTO TM_DATA (timeslot, temperature, humidity) VALUES (?, ?, ?)', para)
        conn.commit()
        print('success')
    except Error as e:
        print(e)
    finally:
        conn.close()


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
