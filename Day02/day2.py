import pandas as pd

def part1():
  data = pd.read_csv("Day02/data.txt", header = None, names = ["command", "amount"], sep=" ")
  forward = data.loc[data.command == "forward"].amount.sum()
  depth = data.loc[data.command == "down"].amount.sum() - data.loc[data.command == "up"].amount.sum() 
  print(forward * depth)   # 1693300


def part2():
  data = pd.read_csv("Day02/data.txt", header = None, names = ["command", "amount"], sep=" ")
  data["depth_down"] = data.loc[data.command == "down"].amount 
  data["depth_up"] = data.loc[data.command == "up"].amount
  data["forward_distance"] = data.loc[data.command == "forward"].amount
  data = data.fillna(0)
  data["aim_change"] = data.depth_down - data.depth_up
  data["aim"] = data.aim_change.cumsum()
  data["x_pos"] = data.forward_distance.cumsum()
  data["depth_change"] = data[data.command == "forward"].apply(lambda row: row.aim * row.amount, axis=1)
  data = data.fillna(0)
  data["depth"] = data.depth_change.cumsum()
  print(data.iloc[-1].x_pos * data.iloc[-1].depth)



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
print(data)
print(x_pos * depth)   #1857958050

