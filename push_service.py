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
    This class extends Thread used for push notification asynchronously
    """

    def __init__(self, utc_date, str_content):
        threading.Thread.__init__(self)
        self.utc_date = utc_date
        self.str_content = str_content

    def run(self):
        is_send_today = False
        with open(PUSH_CHECK_FILE, 'r', encoding='utf-8') as ck_file:
            if self.utc_date in ck_file.read():
                is_send_today = True
        if not is_send_today:
            try:
                pushbullet_service = Pushbullet(PUSHBULLET_API_KEY)
                pushbullet_service.push_note("Raspberry Notify", self.str_content)
                with open(PUSH_CHECK_FILE, 'w', encoding='utf-8') as ck_file:
                    ck_file.write(self.utc_date)
            except PushbulletError as push_error:
                logging.error('Error with pushing to Pushbullet: %s', push_error)
            except IOError as error:
                logging.error('Error with writing status to check file: %s', error)
