import os

CKFILE = './PUSHCK'
if not os.path.isfile(CKFILE):
    open(CKFILE, 'w', encoding='utf-8').close()


def query_send(utc_date):
    is_send_today = False
    with open(CKFILE, 'r', encoding='utf-8') as f:
        if utc_date in f.read():
            is_send_today = True
    if not is_send_today:
        with open(CKFILE, 'w', encoding='utf-8') as f:
            f.write(utc_date)
    return is_send_today
