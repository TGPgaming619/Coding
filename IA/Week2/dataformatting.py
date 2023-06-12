import pandas as pd
import matplotlib.pyplot as plt
data = pd.read_csv("C:\Coding\IA\Week2\predictions2.csv")

data = data.drop(["Unnamed: 0"], axis=1)
data["date"] = pd.to_datetime(data["date"])
data = data[["date","team","opponent","predicted"]]
data["predicted"] = data["predicted"].map({1:"win",0:"lose or draw"})
data.to_csv("C:\Coding\IA\Week2\FormattedDF.csv")

