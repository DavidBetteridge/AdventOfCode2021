import pandas as pd
import networkx as nx

def read_file(filename: str) -> pd.DataFrame:
  with open(filename) as f:
    columns = len(f.readline().strip())

  return pd.read_fwf(filename, widths=[1]*columns, header = None)  


def build_graph(cave: pd.DataFrame) -> nx.DiGraph:
  G = nx.DiGraph()
  number_of_rows, number_of_columns = cave.shape

  neighbours = [(0,-1), (-1, 0), (1,0), (0,1)]

  for row in range(number_of_rows):
    for column in range(number_of_columns):
      for col_offset, row_offset in neighbours:
        if (0 <= column + col_offset < number_of_columns) and \
            (0 <= row + row_offset < number_of_rows):                
              G.add_edge( (column,row),
                          (column + col_offset,row + row_offset),
                          weight = cave[column + col_offset][row + row_offset])
  return G

def solve(repeats: int) -> int:
  cave = read_file("day15/sample.txt")
  G = build_graph(cave)
  print(G)

  number_of_rows, number_of_columns = cave.shape
  route = (nx.dijkstra_path(G,
                        source=(0,0),
                        target=(number_of_columns-1, number_of_rows-1),
                        weight='weight'))

  return sum([cave[col][row] for col,row in route if col !=0 or row != 0])                       


part_one = solve(1)
assert part_one in [40, 717]

part_two = solve(5)
print(part_two)
assert part_two in [315, 717]