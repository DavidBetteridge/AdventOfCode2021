import pandas as pd

data = pd.read_csv("Day02/data.txt", header = None, names = ["command", "amount"], sep=" ")

forward = data.loc[data.command == "forward"].amount.sum()
depth = data.loc[data.command == "down"].amount.sum() - data.loc[data.command == "up"].amount.sum() 

print(forward * depth)