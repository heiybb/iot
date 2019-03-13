import os
import json
import sqlite3
from sqlite3 import Error
from sense_hat import SenseHat

""" check if the db file exist otherwise init with a new one """

DB_FILE_NAME = 'monitorDB'


def init_db_file(db_file):
    if not os.path.isfile(DB_FILE_NAME):
        """ create a database connection to a SQLite database """
        try:
            conn = sqlite3.connect(db_file)
            print(sqlite3.version)
        except Error as e:
            print(e)
        finally:
            conn.close()
    else:
        pass


class DataJson:
    def __init__(self, temperature, humidity):
        self.temperature = temperature
        self.humidity = humidity

    def to_string(self):
        print("The temperature and humidity is: %d %d", self.temperature, self.humidity)


def get_temp_humidity():
    sense = SenseHat()
    sense.clear()
    temp = sense.get_temperature()
    humidity = sense.get_humidity()
    newDataJson = DataJson(temp, humidity)


def compare():
    with open('config.json','r',encoding='utf-8') as conf:
        conf = json.load(conf)

if __name__ == '__main__':
    init_db_file(DB_FILE_NAME)
