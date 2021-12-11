from networkx.classes.function import neighbors
import pandas as pd

def read_file(filename: str) -> pd.DataFrame:
  with open(filename) as f:
    columns = len(f.readline().strip())

  return pd.read_fwf(filename, widths=[1]*columns, header = None)  

neighbours = [ (-1,-1), (0,-1), (1,-1),
               (-1, 0),         (1,0),
               (-1, 1), (0,1),  (1,1) ]


octopuses = read_file('Day11/data.txt')
number_of_rows = octopuses.shape[0]
number_of_columns = octopuses.shape[1]

number_of_flashes = 0
for step in range(100):
  flashed = set()

  for row in range(number_of_rows):
    for column in range(number_of_columns):
      octopuses[column][row] = octopuses[column][row] + 1

  keep_going = True
  while keep_going:
    keep_going = False
    for row in range(number_of_rows):
      for column in range(number_of_columns):
        if octopuses[column][row] > 9:
          if (column, row) not in flashed:
            keep_going = True
            number_of_flashes += 1
            flashed.add((column, row))
            for col_offset, row_offset in neighbours:
              if (0 <= column + col_offset < number_of_columns) and \
                  (0 <= row + row_offset < number_of_rows):
                octopuses[column + col_offset][row + row_offset] = octopuses[column + col_offset][row + row_offset] + 1

  for column, row in flashed:
    octopuses[column][row] = 0

  print("")
  print("")
  print(octopuses)
print(number_of_flashes)

