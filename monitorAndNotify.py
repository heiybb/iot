import datetime
import json
import SQLiteLib
import virtual_sense_hat
from virtual_sense_hat import VirtualSenseHat


class DataJson:
    def __init__(self, timeslot, temperature, humidity):
        self.timeslot = timeslot
        self.temperature = temperature
        self.humidity = humidity


def get_temp_humidity():
    sense = VirtualSenseHat.getSenseHat()
    sense.clear()
    timeslot = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

    temperature = sense.get_temperature()
    # sense.show_message('Temperature: {0:0.2f} ℃'.format(temperature))

    humidity = sense.get_humidity()
    # sense.show_message('Humidity: {0:0.2f} %'.format(humidity))
    SQLiteLib.insert_data(timeslot, temperature, humidity)


def compare():
    with open('config.json', 'r', encoding='utf-8') as conf:
        conf = json.load(conf)


if __name__ == '__main__':
    SQLiteLib.initialize()
    get_temp_humidity()
    SQLiteLib.query_all()
