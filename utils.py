import matplotlib.pyplot as plt
import pandas as pd

def plot(data: pd.Series):
    print(data.to_frame())
    data.plot.bar()
    
    plt.xlabel("Heure de la journée")
    plt.ylabel("Production")
    plt.show()