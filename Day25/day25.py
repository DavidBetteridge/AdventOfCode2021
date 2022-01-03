# Use PyPy
from typing import List

def read_file(filename: str) -> List[str]:
  with open(filename) as f:
    return [line.strip() for line in f.readlines()]

lines = read_file("C:\Personal\AdventOfCode2021\Day25/data.txt")
number_of_rows = len(lines)
number_of_columns = len(lines[0])
grid = {}

for row_number in range(number_of_rows):
  line = lines[row_number]
  for column_number in range(number_of_columns):
    if line[column_number] == ">":
      grid[(row_number,column_number)] = ">"
    elif line[column_number] == "v":
      grid[(row_number,column_number)] = "v"
    else:
      grid[(row_number,column_number)] = "."

i = 0
changed = True
while changed:
  changed = False
  for row_number in range(number_of_rows):
    column_number = 0
    first = grid[(row_number, 0)]
    while column_number < number_of_columns:
      next_column = (column_number + 1) % number_of_columns
      next = first if next_column == 0 else grid[(row_number, next_column)]
      if grid[(row_number, column_number)] == ">" and next == ".":
        grid[(row_number, column_number)] = "."
        grid[(row_number, next_column)] = ">"
        column_number+=2
        changed = True
      else:
        column_number+=1

  for column_number in range(number_of_columns):
    row_number = 0
    first = grid[(0, column_number)]
    while row_number < number_of_rows:
      next_row = (row_number + 1) % number_of_rows
      next = first if next_row == 0 else grid[(next_row,column_number)] 
      if grid[(row_number,column_number)] == "v" and next == ".":
        grid[(row_number,column_number)] = "."
        grid[(next_row,column_number)] = "v"
        row_number+=2
        changed = True
      else:
        row_number+=1
  i += 1

print(i)