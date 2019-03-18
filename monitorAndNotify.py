import os
import json
import SQLiteLib
import time

from sense_hat import SenseHat


class DataJson:
    def __init__(self, timeslot, temperature, humidity):
        self.timeslot = timeslot
        self.temperature = temperature
        self.humidity = humidity

    def to_string(self):
        print("The temperature and humidity is: %d %d ", self.temperature, self.humidity)


def get_temp_humidity():
    sense = SenseHat()
    sense.clear()
    timeslot = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    temp = format(sense.get_temperature(), '.2f')
    humidity = format(sense.get_humidity(), '.2f')

    newDataJson = DataJson(temp, humidity)

    SQLiteLib.insert_data(timeslot, temp, humidity)


def compare():
    with open('config.json', 'r', encoding='utf-8') as conf:
        conf = json.load(conf)


def get_bound_conf():
    try:
        with open('config.json', 'r', encoding='utf-8') as conf:
            conf_data = json.load(conf)
            minT = conf_data['min_temperature']
            maxT = conf_data['max_temperature']
            maxH = conf_data['min_humidity']
            maxH = conf_data['max_humidity']
    except:
        print('Error with reading config file')
    else:
        return


if __name__ == '__main__':
    SQLiteLib.init_db_file()
    get_temp_humidity()
    SQLiteLib.query()
