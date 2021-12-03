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


lines = read_file("Day03/data.txt")
for offset in range(12):
  ones = 0
  for line in lines:
      ones += int(line[offset])
  zeros = len(lines) - ones
  most_common = "1" if ones >= zeros else "0"
  lines = [line for line in lines if line[offset] == most_common]
oxygen_generator_rating = int(lines[0],2)


lines = read_file("Day03/data.txt")
for offset in range(12):
  ones = 0
  for line in lines:
      ones += int(line[offset])
  zeros = len(lines) - ones
  least_common = "0" if zeros <= ones else "1"
  lines = [line for line in lines if line[offset] == least_common]
  if len(lines) == 1:
    break
co2_scrubber_rating = int(lines[0],2)

print(oxygen_generator_rating, co2_scrubber_rating)
print(oxygen_generator_rating * co2_scrubber_rating)


import pandas as pd
data = pd.read_fwf("Day03/data.txt", widths=[1]*12, header = None)
min_number_of_reports = data.shape[0]
result = data.sum().to_frame(name="ones")
result["bit"] = result.apply(lambda row: "1" if row.ones >= (min_number_of_reports/2) else "0", axis=1)
lhs = int("".join(result.bit),2)
rhs = lhs ^ int('111111111111', 2)
print(lhs * rhs)