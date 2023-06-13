import datetime
from pandas import DataFrame
from api.api import *
from utils import *




if __name__ == '__main__':
    start = datetime.datetime(2022, 12, 1, 0, 0)
    end = datetime.datetime(2022, 12, 3, 0, 0)

    api = ActualGeneration()
    plot(api.get_mean_hour_by_hour(start_date=start, end_date=end, sandbox=False))