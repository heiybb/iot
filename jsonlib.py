"""Include all needed operation of the json file in project"""

import json
import logging

try:
    with open('config.json', 'r', encoding='utf-8') as conf:
        CONF_DATA = json.load(conf)
        MIN_TEMP = CONF_DATA['min_temperature']
        MAX_TEMP = CONF_DATA['max_temperature']
        MIN_HUM = CONF_DATA['min_humidity']
        MAX_HUM = CONF_DATA['max_humidity']
except IOError as io_error:
    logging.error("Error with reading config file: %s", io_error)
    MIN_TEMP = -1
    MAX_TEMP = -1
    MIN_HUM = -1
    MAX_HUM = -1


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
