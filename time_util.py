import datetime
import os

def days_since_last():
    today = datetime.date.today()
    filepath = '../weekly_pulls/'
    files = [f for f in os.listdir(filepath) if '.csv' in f]
    last_created = max([os.path.getctime(filepath + f) for f in files])
    last_created = datetime.datetime.fromtimestamp(last_created).date()
    return (today - last_created).days