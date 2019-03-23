import json

try:
    with open('config.json', 'r', encoding='utf-8') as conf:
        conf_data = json.load(conf)
        minT = conf_data['min_temperature']
        maxT = conf_data['max_temperature']
        minH = conf_data['min_humidity']
        maxH = conf_data['max_humidity']
except:
    print('Error with reading config file')


def get_min_temperature():
    return minT


def get_max_temperature():
    return maxT


def get_min_humidity():
    return minH


def ge_max_humidity():
    return maxH
