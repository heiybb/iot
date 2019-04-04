"""
Wrap all the function the project need as a simple library
"""

import logging
import os
import sqlite3
from sqlite3 import Error

DB_FILE = './tmDB.db'
INIT_TABLE = """CREATE TABLE IF NOT EXISTS TM_DATA
            (timestamp TEXT primary key, temperature REAL, humidity REAL)"""


def initialize():
    """ Create the database file and initialize the table if not exist """
    if not os.path.isfile(DB_FILE):
        connection = sqlite3.connect(DB_FILE)
        try:
            with connection:
                connection.execute(INIT_TABLE)
        except Error as error:
            print(error)
        finally:
            connection.close()
    else:
        pass


def insert_data(timestamp, temperature, humidity):
    """
    Insert timestamp temperature humidity to database
    :param timestamp: time in datetime format
    :param temperature: float with precision 00.00
    :param humidity: float with precision 00.00
    :return: None
    """
    connection = sqlite3.connect(DB_FILE)
    try:
        with connection:
            connection.execute(
                """INSERT INTO TM_DATA (timestamp, temperature, humidity)
                VALUES (?, ?, ?)""", (timestamp, temperature, humidity))
    except sqlite3.Error as error:
        logging.error("Database Error: %s", error)
    finally:
        connection.close()


def query_all_th_data():
    """
    Query all data from the database file and print them out
    :return: None
    """
    connection = sqlite3.connect(DB_FILE)
    try:
        with connection:
            result = connection.execute("""select * from TM_DATA""")
        for row in result:
            print('TimeSlot:' + row[0])
            print('Temperature:' + str(row[1]))
            print('Humidity:' + str(row[2]))

    except Error as error:
        print(error)
    finally:
        connection.close()


def get_csv_data():
    """
    Query min max temperature and humidity and order by data
    :return: None
    """
    data = []
    connection = sqlite3.connect(DB_FILE)
    try:
        with connection:
            result = connection.execute(
                """SELECT strftime('%Y-%m-%d',timestamp),
                MIN(temperature),MAX(temperature),MIN(humidity),MAX(humidity)
                FROM TM_DATA
                GROUP BY DATE(timestamp)
                ORDER BY DATE(timestamp)""")

        for row in result:
            data.append(row)
    except Error as error:
        print(error)
    finally:
        connection.close()
    return data


def get_analytics_data():
    """
    Query the data used for the matplotlib library
    :return: List format
    """
    data = []
    connection = sqlite3.connect(DB_FILE)
    try:
        with connection:
            result = connection.execute(
                """SELECT DISTINCT(strftime('%Y-%m-%d %H:%M',datetime(timestamp,'localtime')))
                as MEL,temperature,humidity FROM TM_DATA
                WHERE (MEL LIKE '%2019-04-02%')
                AND strftime('%M', MEL)% 15 = 0""")
        for row in result:
            data.append(row)
    except Error as error:
        print(error)
    finally:
        connection.close()
    return data


def get_analytics_echart_data():
    """
    Query data used for the pyechart library
    :return: List format
    """
    data = []
    connection = sqlite3.connect(DB_FILE)
    try:
        with connection:
            result = connection.execute(
                """SELECT  DISTINCT(strftime('%Y-%m-%d %H:%M',datetime(timestamp,'localtime')))
                as MEL,temperature,humidity FROM TM_DATA
                WHERE (MEL LIKE '%2019-04-02%' OR MEL LIKE '%2019-04-03%')
                AND strftime('%M', MEL)% 15 = 0""")
        for row in result:
            data.append(row)
    except Error as error:
        print(error)
    finally:
        connection.close()
    return data
