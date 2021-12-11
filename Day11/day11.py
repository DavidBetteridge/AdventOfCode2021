import pandas as pd

def read_file(filename: str) -> pd.DataFrame:
  with open(filename) as f:
    columns = len(f.readline().strip())

  return pd.read_fwf(filename, widths=[1]*columns, header = None)  

neighbours = [ (-1,-1), (0,-1), (1,-1),
               (-1, 0),         (1,0),
               (-1, 1), (0,1),  (1,1) ]


def iterate(octopuses, flashed) -> int:
  number_of_rows, number_of_columns = octopuses.shape
  number_of_flashes = 0
  for row in range(number_of_rows):
    for column in range(number_of_columns):
      if octopuses[column][row] > 9:
        if (column, row) not in flashed:
          number_of_flashes += 1
          flashed.add((column, row))
          for col_offset, row_offset in neighbours:
            if (0 <= column + col_offset < number_of_columns) and \
                (0 <= row + row_offset < number_of_rows):
              octopuses[column + col_offset][row + row_offset] += 1
  return number_of_flashes


def part1(octopuses):
  number_of_flashes = 0
  for _ in range(100):

    octopuses+=1 #1

    flashed = set()
    while (x := iterate(octopuses, flashed)) > 0:
      number_of_flashes += x

    for column, row in flashed: #3
      octopuses[column][row] = 0

  assert number_of_flashes == 1601


def part2(octopuses):
  step = 0
  while not all((octopuses == 0).all()):
    step += 1

    octopuses+=1 #1

    flashed = set()
    while iterate(octopuses, flashed) > 0:
      pass

    for column, row in flashed: #3
      octopuses[column][row] = 0

  assert step == 368


octopuses = read_file('Day11/data.txt')
part1(octopuses)

octopuses = read_file('Day11/data.txt')
part2(octopuses)