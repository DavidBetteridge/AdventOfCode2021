import pandas as pd
import numpy as np

def part1():
  data = pd.read_csv("Day02/data.txt", header = None, names = ["command", "amount"], sep=" ")
  forward = data.loc[data.command == "forward"].amount.sum()
  depth = data.loc[data.command == "down"].amount.sum() - data.loc[data.command == "up"].amount.sum() 
  print(forward * depth)   # 1693300


def part2():
  data = pd.read_csv("Day02/data.txt", header = None, names = ["command", "amount"], sep=" ")
  data["aim"] = np.where(data.command == "up", -data.amount, np.where(data.command == "down", data.amount, 0)).cumsum()
  data["x_pos"] = data.loc[data.command == "forward"].amount.cumsum()
  data["depth"] = data[data.command == "forward"].apply(lambda row: row.aim * row.amount, axis=1).cumsum()
  print(data.iloc[-1].x_pos * data.iloc[-1].depth)

part2()

# aim = 0
# x_pos = 0
# depth = 0
# for row in data.itertuples(index=True, name='Pandas'):
#   if row.command == "down":
#     aim += row.amount
#   elif row.command == "up":
#     aim -= row.amount
#   elif row.command == "forward":
#     x_pos += row.amount
#     depth += aim * row.amount
# print(data)
# print(x_pos * depth)   #1857958050

