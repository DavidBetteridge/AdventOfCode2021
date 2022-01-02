import numpy as np
from typing import List

class direction:
  EMPTY = 0
  DOWN = 1 
  LEFT = 2

def read_file(filename: str) -> List[str]:
  with open(filename) as f:
    return [line.strip() for line in f.readlines()]

def step_left(grid: np.array) -> bool:
  changed = False
  for row_number in range(number_of_rows):
    column_number = 0
    first = grid[row_number][0]
    while column_number < number_of_columns:
      next_column = (column_number + 1) % number_of_columns
      next = first if next_column == 0 else grid[row_number][next_column] 
      if grid[row_number][column_number] == direction.LEFT and next == direction.EMPTY:
        grid[row_number][column_number] = direction.EMPTY
        grid[row_number][next_column] = direction.LEFT
        column_number+=2
        changed = True
      else:
        column_number+=1
  return grid,changed

def step_down(grid: np.array, changed: bool) -> bool:
  for column_number in range(number_of_columns):
    row_number = 0
    first = grid[0][column_number]
    while row_number < number_of_rows:
      next_row = (row_number + 1) % number_of_rows
      next = first if next_row == 0 else grid[next_row][column_number] 
      if grid[row_number][column_number] == direction.DOWN and next == direction.EMPTY:
        grid[row_number][column_number] = direction.EMPTY
        grid[next_row][column_number] = direction.DOWN
        row_number+=2
        changed = True
      else:
        row_number+=1
  return changed

def step(grid: np.array) -> bool:
  return step_down(*step_left(grid))

lines = read_file("Day25/data.txt")
number_of_rows = len(lines)
number_of_columns = len(lines[0])
grid = np.empty((number_of_rows, number_of_columns))

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
  changed = step(grid)
  if not changed:
    break

print(i)