import pandas as pd

def part1():
  data = pd.read_csv("Day02/data.txt", header = None, names = ["command", "amount"], sep=" ")
  forward = data.loc[data.command == "forward"].amount.sum()
  depth = data.loc[data.command == "down"].amount.sum() - data.loc[data.command == "up"].amount.sum() 
  print(forward * depth)   # 1693300


data = pd.read_csv("Day02/data.txt", header = None, names = ["command", "amount"], sep=" ")
aim = 0
x_pos = 0
depth = 0
for row in data.itertuples(index=True, name='Pandas'):
  if row.command == "down":
    aim += row.amount
  elif row.command == "up":
    aim -= row.amount
  elif row.command == "forward":
    x_pos += row.amount
    depth += aim * row.amount
  print(aim, x_pos, depth)
print(x_pos * depth)
