import datetime
from pandas import DataFrame
from actual_generation import *




if __name__ == '__main__':
    start = datetime.datetime(2022, 12, 1, 0, 0)
    end = datetime.datetime(2022, 12, 7, 0, 0)

    api = ActualGeneration()
    actual_gen_per_unit = DataFrame(api.get_per_unit(start, end))
    print(actual_gen_per_unit.head())