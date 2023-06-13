import matplotlib.pyplot as plt
import pandas as pd

def plot(data: pd.Series):
    print(data.to_frame())
    data.plot.bar()
    
    plt.xlabel("Heure de la journée")
    plt.ylabel("Production")
    plt.show()

def date_range(start, end, intv):
    from datetime import datetime
    start = datetime.strptime(start,"%Y%m%d")
    end = datetime.strptime(end,"%Y%m%d")
    diff = (end  - start ) / intv
    for i in range(intv):
        yield (start + diff * i).strftime("%Y%m%d")
    yield end.strftime("%Y%m%d")