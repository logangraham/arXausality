from make_spreadsheet import get_paper_spreadsheet
from time_util import days_since_last
import datetime
import sys


def run(*args):
    """
    Flow:
        -> fetch_papers pull supdate
        -> make_spreadsheet turns to spreadsheet
    """
    if args:
        print("ARGS:{}".format(args))
        return get_paper_spreadsheet(int(args[0]))
    else:
        n_days = days_since_last()
        print("Getting papers from the last {} days...".format(n_days))
        return get_paper_spreadsheet(n_days)


if __name__ == "__main__":
    run()