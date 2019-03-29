import datetime
import logging
import os
import re

from sense_hat import SenseHat

import jsonlib
import push_service
import sqlite_lib


def get_cpu_temp():
    res = os.popen('vcgencmd measure_temp').readline()
    return float(re.search('\\d+\\.\\d+', res).group(0))


def get_smooth(temperature):
    if not hasattr(get_smooth, "t"):
        get_smooth.t = [temperature, temperature, temperature]
    get_smooth.t[2] = get_smooth.t[1]
    get_smooth.t[1] = get_smooth.t[0]
    get_smooth.t[0] = temperature
    smoothed = (get_smooth.t[0] + get_smooth.t[1] + get_smooth.t[2]) / 3
    return smoothed


class MonitorData:
    def __init__(self):
        sense = SenseHat()
        self.time_stamp = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        self.temperature = float(format(get_smooth(self.get_act_temp()), '.2f'))
        self.humidity = float(format(sense.get_humidity(), '.2f'))
        try:
            sqlite_lib.insert_data(self.time_stamp, self.temperature, self.humidity)
        except IOError as io_error:
            logging.error('Error with reading config file: %s', io_error)

    def to_string(self):
        return 'Time:' + str(self.time_stamp) + '\n' + \
               'Temperature: {0:0.2f} ℃'.format(self.temperature) + '\n' + \
               'Humidity: {0:0.2f} %'.format(self.humidity)

    def try_push(self):
        notify_msm = jsonlib.generate_msg(self.temperature, self.humidity)

        if notify_msm is not '':
            today_utc = datetime.datetime.utcnow().strftime('%Y-%m-%d')
            push = push_service.PushThread(today_utc, notify_msm)
            push.start()

    @staticmethod
    def get_act_temp():
        temp_f_hum = SenseHat().get_temperature_from_humidity()
        temp_f_pre = SenseHat().get_temperature_from_pressure()
        t_cpu = get_cpu_temp()
        temp_average = (temp_f_hum + temp_f_pre) / 2
        # calculates the real temperature compensating CPU heating
        temperature_corr = temp_average - ((t_cpu - temp_average) / 1.5)
        return temperature_corr

    # use moving average to smooth readings


if __name__ == '__main__':
    sqlite_lib.initialize()
    MON = MonitorData()
    MON.try_push()
    # SQLiteLib.query_all_th_data()
