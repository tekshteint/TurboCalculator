import pandas as pd
import seaborn
import matplotlib.pyplot as plt

def generateDataSet(arr: list) -> pd.DataFrame:
    data = pd.DataFrame(arr, columns= ["Horsepower"], dtype=float)

    print(data)
    return data

def generateGraph(arr: list) -> None:
    dataSet = generateDataSet(arr)
    seaborn.lineplot(data= dataSet, x=list(range(len(dataSet))), y="Horsepower")
    plt.show()