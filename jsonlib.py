"""Include all needed operation of the json file in project"""

import json
import logging

MIN_TEMP = -1
MAX_TEMP = -1
MIN_HUM = -1
MAX_HUM = -1

try:
    with open('config.json', 'r', encoding='utf-8') as conf:
        CONF_DATA = json.load(conf)
        MIN_TEMP = CONF_DATA['min_temperature']
        MAX_TEMP = CONF_DATA['max_temperature']
        MIN_HUM = CONF_DATA['min_humidity']
        MAX_HUM = CONF_DATA['max_humidity']
except IOError as io_error:
    logging.error("Error with reading config file: %s", io_error)


def get_min_temperature():
    """Return the minimum temperature."""
    return MIN_TEMP


def get_max_temperature():
    """Return the maximum temperature."""
    return MAX_TEMP


def get_min_humidity():
    """Return the minimum humidity."""
    return MIN_HUM


def get_max_humidity():
    """Return the pathname humidity."""
    return MAX_HUM


def get_notify_msg(temperature, humidity):
    msg = ''
    if temperature < MIN_TEMP:
        msg += "Temperature: {temp:0.2f}℃\n {diff:0.2f}℃ below minimum {min_temp}℃\n" \
            .format(temp=temperature, diff=MIN_TEMP - temperature, min_temp=MIN_TEMP)

    if temperature > MAX_TEMP:
        msg += "Temperature: {temp:0.2f}℃\n {diff:0.2f}℃ above maximum {max_temp}℃\n" \
            .format(temp=temperature, diff=temperature - MAX_TEMP, max_temp=MAX_TEMP)

    if humidity < MIN_HUM:
        msg += "Humidity: {hum:0.2f}%\n {diff:0.2f}% below minimum {min_hum}%\n" \
            .format(hum=humidity, diff=MIN_HUM - humidity, min_hum=MIN_HUM)

    if humidity > MAX_HUM:
        msg += "Humidity: {hum:0.2f}%\n {diff:0.2f}% above maximum {max_hum}%\n" \
            .format(hum=humidity, diff=humidity - MAX_HUM, max_hum=MAX_HUM)
    return msg


def get_report_msg(min_temp, max_temp, min_hum, max_hum):
    """
    Compare the data read queried from the database file with the json bounds
    and return appropriate message
    """
    msg = ''
    if min_temp < MIN_TEMP:
        msg += "{diff:0.2f}℃ below minimum temperature; ".format(diff=MIN_TEMP - min_temp)
    if max_temp > MAX_TEMP:
        msg += "{diff:0.2f}℃ above maximum temperature; ".format(diff=max_temp - MAX_TEMP)
    if min_hum < MIN_HUM:
        msg += "{diff:0.2f}% below minimum temperature; ".format(diff=MIN_HUM - min_hum)
    if max_hum > MAX_HUM:
        msg += "{diff:0.2f}% above maximum temperature; ".format(diff=max_hum - MAX_HUM)
    return msg
