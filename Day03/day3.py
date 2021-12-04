import pandas as pd
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


data = pd.read_fwf("Day03/data.txt", widths=[1]*12, header = None)
min_number_of_ones = data.shape[0] / 2
result = data.sum().to_frame(name="ones")
result["bit"] = result.apply(lambda row: "1" if row.ones >= min_number_of_ones else "0", axis=1)
lhs = int("".join(result.bit),2)
rhs = lhs ^ int('111111111111', 2)
print(lhs * rhs)


def reduce(data, rule, offset=0):
  rows = data.shape[0]
  if rows == 1:
    return data

  ones = data[offset].sum()
  match = rule(ones, rows)
  return reduce(data.loc[data[offset] == match], rule, offset+1)


data = pd.read_fwf("Day03/data.txt", widths=[1]*12, header = None)
matching_row = reduce(data, rule = lambda ones, rows : 1 if ones >= (rows/2) else 0)
oxygen_generator_rating = int("".join(map(str,matching_row.iloc[0])),2)

matching_row = reduce(data, rule = lambda ones, rows : 1 if ones < (rows/2) else 0)
co2_scrubber_rating = int("".join(map(str,matching_row.iloc[0])),2)

print(oxygen_generator_rating * co2_scrubber_rating)
