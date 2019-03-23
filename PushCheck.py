def query_send(utc_date):
    is_send_today = False
    with open('PUSHCK', 'w+', encoding='utf-8') as f:
        if utc_date in f.read().split('#'):
            is_send_today = True
        else:
            f.seek(0)
            f.write(utc_date)
    return is_send_today
