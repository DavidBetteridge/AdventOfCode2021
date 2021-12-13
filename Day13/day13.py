import pandas as pd
import numpy as np
from typing import List, Tuple

def read_file(filename: str):
  with open(filename) as f:
    lines = f.readlines()
    loading_points = True
    points = []
    folds = []
    for line in lines:
      if line.strip() == "":
        loading_points = False
      elif loading_points:
        x,y = line.strip().split(",")
        points.append((int(x),int(y)))
      else:
        rubbish, action = line.strip().split("fold along ")
        direction, distance = action.split("=")
        folds.append((direction, distance))
    return points, folds

def create_dataframe(points: List[Tuple[int,int]]) -> pd.DataFrame:
  width = max(x for x,y in points) + 1
  height = max(y for x,y in points) + 1
  df = pd.DataFrame(np.zeros((height, width)))
  for x,y in points:
    df[x][y] = 1
  return df

def fold_up(df, row_number):
  # Tear the paper on the folder line
  df_top = df.iloc[:row_number,:]
  df_bottom = df.iloc[row_number+1:,:]

  # Flip all the rows on the bottom half vertically
  df_bottom = df_bottom.reindex(index=df_bottom.index[::-1])
  df_bottom.reset_index(drop=True, inplace=True)

  # Make sure both bits of paper are the same size
  while df_bottom.shape[0] < df_top.shape[0]:
    df_bottom.loc[-1] = [0] * df.shape[1]
    df_bottom.index = df_bottom.index + 1
  df_bottom.sort_index(inplace=True) 

  while df_top.shape[0] < df_bottom.shape[0]:
    df_top.loc[-1] = [0] * df.shape[1]
    df_top.index = df_top.index + 1
  df_top.sort_index(inplace=True) 

  # Combine the dots
  return df_top.add(df_bottom)

def fold_left(df, column_number):
  df = df.T
  df = fold_up(df, column_number)
  df = df.T
  return df


def count_visible_dots(df):
  return df[df >= 1].count().sum()


points, folds = read_file("Day13/data.txt")
paper = create_dataframe(points)

for direction, distance in folds:
  if direction == "x":
    paper = fold_left(paper, int(distance))
  else:
    paper = fold_up(paper, int(distance))

rows, cols = paper.shape
for row in range(rows):
  p = ""
  for col in range(cols):
    if paper[col][row] == 0:
      p += " "
    else:
      p += "*"
  print(p) 
