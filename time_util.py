import datetime
import os
import numpy as np


def days_since_last(filepath='../weekly_pulls/'):
    today = datetime.date.today()
    latest_file, latest_date = get_last_created(filepath, '.csv')
    return (today - latest_date).days

def get_last_created(filepath, extension_filter=None):
    files = os.listdir(filepath)
    if extension_filter is not None:
        files = [f for f in files if extension_filter in f]
    creation_times = [os.path.getctime(filepath + f) for f in files]
    index_of_latest = np.argmax(creation_times)
    latest_created_file = filepath + files[index_of_latest]
    latest_created_date = datetime.datetime.fromtimestamp(creation_times[index_of_latest]).date()
    return latest_created_file, latest_created_date