from os import read
from typing import List


def read_file(filename) -> List[str]:
  with open(filename) as f:
    return f.readlines()

lines = read_file("Day03/data.txt")

lhs = ""
for offset in range(12):
  ones = 0
  for line in lines:
      ones += int(line[offset])
  zeros = len(lines) - ones
  lhs += "1" if ones > zeros else "0"
lhs = int(lhs, 2)
rhs = lhs ^ int('111111111111', 2)
print(lhs * rhs)

