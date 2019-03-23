import datetime
import PushCheck
import SQLiteLib

from virtual_sense_hat import VirtualSenseHat
from pushbullet import Pushbullet

pb = Pushbullet('o.HyVkzj8lKJWZ4t0i8fzGijVDwnkDKonS')


class DataJson:
    def __init__(self, timeslot, temperature, humidity):
        self.timeslot = timeslot
        self.temperature = float(format(temperature, '.2f'))
        self.humidity = float(format(humidity, '.2f'))

    def to_string(self):
        return 'Time:' + str(self.timeslot) + '\n' + \
               'Temperature: {0:0.2f} ℃'.format(self.temperature) + '\n' + \
               'Humidity: {0:0.2f} %'.format(self.humidity)


def get_temp_humidity():
    sense = VirtualSenseHat.getSenseHat()
    sense.clear()
    timeslot = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    temperature = sense.get_temperature()
    # sense.show_message('Temperature: {0:0.2f} ℃'.format(temperature))
    humidity = sense.get_humidity()
    # sense.show_message('Humidity: {0:0.2f} %'.format(humidity))
    newSege = DataJson(timeslot, temperature, humidity)
    SQLiteLib.insert_data(newSege.timeslot, newSege.temperature, newSege.humidity)
    try_push(newSege)


def try_push(segemant: DataJson):
    today_utc = datetime.datetime.utcnow().strftime('%Y-%m-%d')
    if not PushCheck.query_send(today_utc):
        pb.push_note("Raspberry Notify", segemant.to_string())


if __name__ == '__main__':
    SQLiteLib.initialize()
    get_temp_humidity()
    SQLiteLib.query_all_th_data()
