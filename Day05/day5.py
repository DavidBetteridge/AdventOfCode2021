import pandas as pd
from typing import Tuple


def parse_line(line: str) -> Tuple:
  lhs, rhs = line.split(" -> ")
  x1, y1 = lhs.split(",")
  x2, y2 = rhs.split(",")
  return int(x1), int(y1), int(x2), int(y2.rstrip())

def read_file() -> pd.DataFrame:
  with open("Day05/sample.txt") as f:
    data = [parse_line(line) for line in f.readlines()]
    return pd.DataFrame(data, columns =['x1', 'y1', 'x2', 'y2'])

lines = read_file()
horizontal_size = max(lines.x1.max(), lines.x2.max())+1
vertical_size = max(lines.y1.max(), lines.y2.max())+1
overlaps = [[0] * horizontal_size for _ in range(vertical_size)]

for index, row in lines.iterrows():
  if row["x1"] == row["x2"]:
    ystart = min(row["y1"], row["y2"])
    yend = max(row["y1"], row["y2"])
    for y in range(ystart, yend+1):
      overlaps[y][row["x1"]] += 1

  elif row["y1"] == row["y2"]:
    xstart = min(row["x1"], row["x2"])
    xend = max(row["x1"], row["x2"])    
    for x in range(xstart, xend+1):
      overlaps[row["y1"]][x] += 1

  else:
    ystep = 1 if row["y2"] >= row["y1"] else -1
    xstep = 1 if row["x2"] >= row["x1"] else -1

    offset = 0
    x = row["x1"]
    y = row["y1"]
    while x != (row["x2"] + xstep):
      overlaps[y][x] += 1
      x += xstep
      y += ystep


danger = 0
for row in range(vertical_size):
  for column in range(horizontal_size):
    if overlaps[row][column] >= 2:
      danger +=1

print(danger)  #18605
