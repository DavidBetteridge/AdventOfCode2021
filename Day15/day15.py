import pandas as pd
import networkx as nx

def read_file(filename: str) -> pd.DataFrame:
  with open(filename) as f:
    columns = len(f.readline().strip())

  return pd.read_fwf(filename, widths=[1]*columns, header = None)  


def build_graph(cave: pd.DataFrame, number_of_tiles: int) -> nx.DiGraph:
  G = nx.DiGraph()
  number_of_rows, number_of_columns = cave.shape

  neighbours = [(0,-1), (-1, 0), (1,0), (0,1)]
  weights = {}

  for x_tile in range(number_of_tiles):
    x_tile_offset = x_tile * number_of_columns
    for y_tile in range(number_of_tiles):
      y_tile_offset = y_tile * number_of_rows
      for row in range(number_of_rows):
        for column in range(number_of_columns):
          for col_offset, row_offset in neighbours:
            if (0 <= column + col_offset < number_of_columns) and \
                (0 <= row + row_offset < number_of_rows):
                  from_cell = (column + x_tile_offset, row + y_tile_offset)
                  to_cell = (column + col_offset + x_tile_offset, row + row_offset + y_tile_offset)            
                  weight = (cave[column + col_offset][row + row_offset] + x_tile + y_tile)
                  if weight > 9: weight -= 9
                  weights[to_cell] = weight
                  G.add_edge(from_cell,
                             to_cell,
                             weight = weight)

  for x_tile in range(number_of_tiles):
    x_tile_offset = x_tile * number_of_columns
    for y_tile in range(number_of_tiles):
      y_tile_offset = y_tile * number_of_rows
      for column in range(number_of_columns):
        #UP
        if y_tile > 0:
          row = 0
          from_cell = (column + x_tile_offset, row + y_tile_offset)
          to_cell = (column + x_tile_offset, row + y_tile_offset -1)            
          G.add_edge(from_cell,
                    to_cell,
                    weight = weights[to_cell])

        #DOWN
        if y_tile+1 < number_of_tiles:
          row = number_of_rows-1
          from_cell = (column + x_tile_offset, row + y_tile_offset)
          to_cell = (column + x_tile_offset, row + y_tile_offset +1)            
          G.add_edge(from_cell,
                    to_cell,
                    weight = weights[to_cell])

      for row in range(number_of_rows):
        #LEFT
        if x_tile > 0:
          column = 0
          from_cell = (column + x_tile_offset, row + y_tile_offset)
          to_cell = (column + x_tile_offset - 1, row + y_tile_offset)            
          G.add_edge(from_cell,
                    to_cell,
                    weight = weights[to_cell])

        #RIGHT
        if x_tile+1 < number_of_tiles:
          column = number_of_columns-1
          from_cell = (column + x_tile_offset, row + y_tile_offset)
          to_cell = (column + x_tile_offset + 1, row + y_tile_offset)            
          G.add_edge(from_cell,
                    to_cell,
                    weight = weights[to_cell])                                               


  return G, weights

def solve(number_of_tiles: int) -> int:
  cave = read_file("day15/data.txt")
  G, weights = build_graph(cave, number_of_tiles)
  print(G)


  number_of_rows, number_of_columns = cave.shape
  x_tile_offset = (number_of_tiles-1) * number_of_columns
  y_tile_offset = (number_of_tiles-1) * number_of_rows

  route = (nx.dijkstra_path(G,
                        source=(0,0),
                        target=(x_tile_offset+number_of_columns-1, y_tile_offset+number_of_rows-1),
                        weight='weight'))
  return sum([weights[(col,row)] for col,row in route if col !=0 or row != 0])                       


part_one = solve(1)
assert part_one in [40, 717]

part_two = solve(5)
print(part_two)
assert part_two in [315, 2993]   #2199 too low