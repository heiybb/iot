"""
Create a thread to push the notification to devices
date time will be checked
sending message is limited to 1 time per day
"""

import logging
import os
import threading

from pushbullet import Pushbullet, PushbulletError

PUSH_CHECK_FILE = './PUSHCK'
PUSHBULLET_API_KEY = 'o.HyVkzj8lKJWZ4t0i8fzGijVDwnkDKonS'

if not os.path.isfile(PUSH_CHECK_FILE):
    open(PUSH_CHECK_FILE, 'w', encoding='utf-8').close()


class PushThread(threading.Thread):
    """
    This class extends Thread used for push notification asynchronously without time send check
    """

    def __init__(self, pb_title, pb_content):
        threading.Thread.__init__(self)
        self.pb_title = pb_title
        self.pb_content = pb_content
        self.service = Pushbullet(PUSHBULLET_API_KEY)

    def push(self):
        """
        Push via pushbullet service
        :return: None
        """
        try:
            self.service.push_note(self.pb_title, self.pb_content)
        except PushbulletError as push_error:
            logging.error('Error with pushing to Pushbullet: %s', push_error)

    def run(self):
        self.push()


class PushThreadWithCK(PushThread):
    """
    This class extends Thread used for push notification asynchronously with the time send check
    """
    def __init__(self, pb_title, pb_content, pre_ck_time):
        PushThread.__init__(self, pb_title, pb_content)
        self.pre_ck_time = pre_ck_time

    def run(self):
        is_send_today = self.ck_is_sent(self.pre_ck_time)

        if not is_send_today:
            self.push()
            self.mk_is_sent(self.pre_ck_time)

    @staticmethod
    def ck_is_sent(pre_ck_time):
        """
        Check the time if was sent before or not
        :param pre_ck_time: time that need to be checked if sent
        :return: None
        """
        with open(PUSH_CHECK_FILE, 'r', encoding='utf-8') as ck_file:
            if pre_ck_time in ck_file.read():
                return True
        return False

    @staticmethod
    def mk_is_sent(date_time):
        """
        Write the data_time into the file and mark it was sent this day
        :param date_time: time that need to marked as sent
        :return:None
        """
        try:
            with open(PUSH_CHECK_FILE, 'w', encoding='utf-8') as ck_file:
                ck_file.write(date_time)
        except IOError as error:
            logging.error('Error with writing status to check file: %s', error)
