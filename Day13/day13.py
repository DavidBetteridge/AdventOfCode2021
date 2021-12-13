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
        folds.append(line)
    return points, folds

def create_dataframe(points: List[Tuple[int,int]]) -> pd.DataFrame:
  width = max(x for x,y in points) + 1
  height = max(y for x,y in points) + 1
  df = pd.DataFrame(np.zeros((height, width)))
  for x,y in points:
    df[x][y] = 1
  return df

def vertical_fold(df, row_number):
  df_top = df.iloc[:row_number+1,:]
  df_bottom = df.iloc[row_number:,:]

  df_bottom = df_bottom.reindex(index=df_bottom.index[::-1])
  df_bottom.reset_index(drop=True, inplace=True)

  return df_top.add(df_bottom)


def count_visible_dots(df):
  return df[df >= 1].count().sum()


points, folds = read_file("Day13/sample.txt")
paper = create_dataframe(points)
paper = vertical_fold(paper, 7)
print(count_visible_dots(paper))





# columns = df_top.shape[1]
# rows_top = df_top.shape[0]
# rows_bottom = df_bottom.shape[0]

# while rows_top > rows_bottom:
#   # Add rows to bottom
#   df_bottom.loc[-1] = [0] * columns
#   df_bottom.index = df_bottom.index + 1  # shifting index
#   df_bottom.sort_index(inplace=True) 
#   rows_bottom = df_bottom.shape[0]

# while rows_top < rows_bottom:
#   # Add rows to top
#   df_top.loc[-1] = [0] * columns
#   df_top.index = df_top.index + 1  # shifting index
#   df_top.sort_index(inplace=True) 
#   rows_top = df_top.shape[0]


# print(df_top)
# print(df_bottom)

# df = df_top.add(df_bottom)

# visible_dots = df[df >= 1].count().sum()

# print(visible_dots)


# df1 = datasX.iloc[:, :72]
# df2 = datasX.iloc[:, 72:]


# data_frame = data_frame.sort_index(axis=1 ,ascending=True)
# data_frame = data_frame.iloc[::-1]


# data_frame = data_frame.reindex(index=data_frame.index[::-1])
