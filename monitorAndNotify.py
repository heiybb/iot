import datetime
import logging
import os
import re
from decimal import Decimal
from pytz import timezone

from sense_hat import SenseHat

import jsonlib
import push_service
import sqlite_lib


def get_cpu_temp():
    res = os.popen('vcgencmd measure_temp').readline()
    return float(re.search('\\d+\\.\\d+', res).group(0))


class MonitorData:
    def __init__(self):
        sense = SenseHat()
        self.time_stamp = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        self.temperature = float(Decimal(self.get_act_temp()).quantize(Decimal('.00')))
        self.humidity = float(Decimal(sense.get_humidity()).quantize(Decimal('.00')))
        try:
            sqlite_lib.insert_data(self.time_stamp, self.temperature, self.humidity)
        except IOError as io_error:
            logging.error('Error with reading config file: %s', io_error)

    def to_string(self):
        return 'Time:' + str(self.time_stamp) + '\n' + \
               'Temperature: {0:0.2f} ℃'.format(self.temperature) + '\n' + \
               'Humidity: {0:0.2f} %'.format(self.humidity)

    def try_push(self):
        notify_msm = jsonlib.get_notify_msg(self.temperature, self.humidity)

        if notify_msm is not '':
            today_utc = datetime.datetime.utcnow().strftime('%Y-%m-%d')
            push = push_service.PushThreadWithCK(today_utc, notify_msm)
            push.start()

    @staticmethod
    def get_act_temp():
        temp_f_hum = SenseHat().get_temperature_from_humidity()
        temp_f_pre = SenseHat().get_temperature_from_pressure()
        t_cpu = get_cpu_temp()
        temp_average = (temp_f_hum + temp_f_pre) / 2
        # calculates the real temperature compensating CPU heating
        # minus 10 to make it more close to the real temperature according to the records before
        temperature_corr = temp_average - ((t_cpu - temp_average) / 1.5) - 10
        return temperature_corr

    # use moving average to smooth readings

    @staticmethod
    def get_mel_time():
        mel_zone = timezone('Australia/Melbourne')
        return datetime.datetime.now(mel_zone)


if __name__ == '__main__':
    sqlite_lib.initialize()
    MON = MonitorData()
    MON.try_push()
    # sqlite_lib.query_all_th_data()
