from typing import List
import pandas as pd

def read_file(filename: str) -> pd.DataFrame:
  with open(filename) as f:
    columns = len(f.readline().strip())

  return pd.read_fwf(filename, widths=[1]*columns, header = None)  

def find_low_points(data: pd.DataFrame) -> List[int]:
  rows = data.shape[0]
  columns = data.shape[1]
  results = []

  for row in range(rows):
    for col in range(columns):
      cell = data[col][row]
      if row > 0 and data[col][row -1] <= cell:
        continue
      if row+1 < rows and data[col][row +1] <= cell:
        continue
      if col > 0 and data[col-1][row] <= cell:
        continue      
      if col+1 < columns and data[col+1][row] <= cell:
        continue
      results.append(cell)

  return results

data = read_file("Day09/data.txt")
low_points = find_low_points(data)
print(low_points)
risk = len(low_points)
result = sum(low_points) + risk
print(result)  #572