from typing import Tuple
import pandas as pd
import numpy as np

def read_file(filename: str) -> pd.DataFrame:
  with open(filename) as f:
    columns = len(f.readline().strip())

  return pd.read_fwf(filename, widths=[1]*columns, header = None)  

def build_neighbours(octopuses):
  number_of_rows, number_of_columns = octopuses.shape

  neighbours = [ (-1,-1), (0,-1), (1,-1),
                (-1, 0),         (1,0),
                (-1, 1), (0,1),  (1,1) ]

  neighbours_df = {}
  for row in range(number_of_rows):
    for column in range(number_of_columns):
      df = pd.DataFrame(np.zeros((number_of_rows, number_of_columns)))
      for col_offset, row_offset in neighbours:
        if (0 <= column + col_offset < number_of_columns) and \
            (0 <= row + row_offset < number_of_rows):                
          df[column + col_offset][row + row_offset] = 1
      neighbours_df[(column, row)] = df
  return neighbours_df

def iterate(octopuses: pd.DataFrame, flashed, neighbours_dfs) -> Tuple[pd.DataFrame, int]:
  number_of_rows, number_of_columns = octopuses.shape
  number_of_flashes = 0
  for row in range(number_of_rows):
    for column in range(number_of_columns):
      if octopuses[column][row] > 9 and (column, row) not in flashed:
        number_of_flashes += 1
        flashed.add((column, row))
        octopuses = octopuses.add(neighbours_dfs[(column, row)])
  return octopuses, number_of_flashes


def part1(octopuses):
  neighbours_dfs = build_neighbours(octopuses)
  number_of_flashes = 0
  for _ in range(100):

    octopuses+=1 #1

    flashed = set()
    new_flashes = 1
    while new_flashes > 0:
      octopuses, new_flashes = iterate(octopuses, flashed, neighbours_dfs)
      number_of_flashes += new_flashes

    for column, row in flashed: #3
      octopuses[column][row] = 0

  assert number_of_flashes == 1601


def part2(octopuses):
  neighbours_dfs = build_neighbours(octopuses)
  step = 0
  while not all((octopuses == 0).all()):
    step += 1

    octopuses+=1 #1

    flashed = set()
    new_flashes = 1
    while new_flashes > 0:
      octopuses, new_flashes = iterate(octopuses, flashed, neighbours_dfs)

    for column, row in flashed: #3
      octopuses[column][row] = 0

  assert step == 368


octopuses = read_file('Day11/data.txt')
part1(octopuses)

octopuses = read_file('Day11/data.txt')
part2(octopuses)