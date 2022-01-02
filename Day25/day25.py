import numpy as np
from typing import List


def read_file(filename: str) -> List[str]:
  with open(filename) as f:
    return [line.strip() for line in f.readlines()]

def step_left(grid: np.array) -> np.array:
  new_grid = np.zeros((number_of_rows, number_of_columns))
  for row_number in range(number_of_rows):
    for column_number in range(number_of_columns):
      next_column = (column_number + 1) % number_of_columns
      previous_column = (column_number - 1) % number_of_columns
      if grid[row_number][column_number] == direction.LEFT and grid[row_number][next_column] == direction.EMPTY:
        new_grid[row_number][column_number] = direction.EMPTY
      elif grid[row_number][column_number] == direction.EMPTY and grid[row_number][previous_column] == direction.LEFT:
        new_grid[row_number][column_number] = direction.LEFT
      else:
        new_grid[row_number][column_number] = grid[row_number][column_number]  
  return new_grid

def step_down(grid: np.array) -> np.array:
  new_grid = np.zeros((number_of_rows, number_of_columns))
  for row_number in range(number_of_rows):
    next_row = (row_number + 1) % number_of_rows
    previous_row = (row_number - 1) % number_of_rows
    for column_number in range(number_of_columns):
      if grid[row_number][column_number] == direction.DOWN and grid[next_row][column_number] == direction.EMPTY:
        new_grid[row_number][column_number] = direction.EMPTY
      elif grid[row_number][column_number] == direction.EMPTY and grid[previous_row][column_number] == direction.DOWN:
        new_grid[row_number][column_number] = direction.DOWN
      else:
        new_grid[row_number][column_number] = grid[row_number][column_number]  
  return new_grid

def step(grid: np.array) -> np.array:
  return step_down(step_left(grid))

lines = read_file("Day25/data.txt")
number_of_rows = len(lines)
number_of_columns = len(lines[0])
grid = np.empty((number_of_rows, number_of_columns))

class direction:
  EMPTY = 0
  DOWN = 1 
  LEFT = 2

for row_number in range(number_of_rows):
  line = lines[row_number]
  for column_number in range(number_of_columns):
    if line[column_number] == ">":
      grid[row_number][column_number] = direction.LEFT
    elif line[column_number] == "v":
      grid[row_number][column_number] = direction.DOWN
    else:
      grid[row_number][column_number] = direction.EMPTY

i = 0
while True:
  i += 1
  grid2 = step(grid)
  if (grid == grid2).all():
    break
  else:
    grid=grid2

print(i)