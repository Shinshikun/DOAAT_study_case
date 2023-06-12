import datetime
from pandas import DataFrame
from actual_generation import *




if __name__ == '__main__':
    start = datetime.datetime(2022, 12, 1, 0, 0)
    end = datetime.datetime(2022, 12, 4, 0, 0)

    api = ActualGeneration()
    api.get_mean_hour_by_hour(start_date=start, end_date=end, sandbox=False)