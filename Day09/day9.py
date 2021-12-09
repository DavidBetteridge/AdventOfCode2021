from typing import List, Tuple
import pandas as pd
import networkx as nx
import math

def read_file(filename: str) -> pd.DataFrame:
  with open(filename) as f:
    columns = len(f.readline().strip())

  data = pd.read_fwf(filename, widths=[1]*columns, header = None)  
  # data = pd.concat([[9] * columns, data, [9] * columns]).reset_index(drop=True)
  return data


def find_low_points(data: pd.DataFrame) -> List[Tuple[(int, int, int)]]:
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
      results.append((col, row, cell))

  return results

def part1():
  data = read_file("Day09/data.txt")
  low_points = find_low_points(data)
  risk = len(low_points)
  result = sum(value for _,_,value in low_points) + risk
  print(result)  #572


def node_id(column, row):
  return f"{column},{row}"

data = read_file("Day09/data.txt")
rows = data.shape[0]
columns = data.shape[1]
G = nx.Graph()

links = []
for row in range(rows):
  for col in range(columns):
    cell = data[col][row]
    if cell != 9:
      G.add_node(node_id(col, row), value=cell)
      if row > 0 and data[col][row -1] != 9:
        links.append((node_id(col, row), node_id(col, row -1)))
      if col > 0 and data[col-1][row] != 9:
        links.append((node_id(col, row), node_id(col -1, row)))

for link in links:
  G.add_edge(*link)

basins = [len(G.subgraph(c)) for c in nx.connected_components(G)]
three_largest = sorted(basins)[-3:]
print(math.prod(three_largest))