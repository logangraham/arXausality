from datetime import datetime, date
import os
import numpy as np


def days_since_last(filepath='../weekly_pulls/'):
    today = date.today()
    latest_file, latest_date = get_last_created(filepath, '.csv')
    return (today - latest_date).days

def get_last_created(filepath="../weekly_pulls/", extension_filter=None):
    files = os.listdir(filepath)
    if extension_filter is not None:
        files = [f for f in files if extension_filter in f and "fetch" in f]
    else:
        files = [f for f in files if "fetch" in f]
    y_m_d = [i for i in map(lambda x: " ".join(x.split("_")[:3]), files)]
    y_m_d = [i for i in map(lambda x: datetime.strptime(x, "%Y %m %d"), y_m_d)]
    index_of_latest = np.argmax(y_m_d)
    latest_created_file = filepath + files[index_of_latest]
    latest_created_date = y_m_d[index_of_latest].date()
    return latest_created_file, latest_created_date

if __name__ == "__main__":
    print(days_since_last())
