from typing import Counter, List
from functools import lru_cache

def read_file() -> List[int]:
  with open("Day06/data.txt") as f:
    return list(map(int, f.read().split(",")))

@lru_cache()
def solve_for_single_fish(start_value, days_remaining):
  if days_remaining == 0: return 1

  start_value = start_value - 1
  if start_value == -1:
    start_value = 6
    return solve_for_single_fish(start_value, days_remaining - 1) + solve_for_single_fish(8, days_remaining - 1)
  else:
    return solve_for_single_fish(start_value, days_remaining - 1)

def solve(fish, days_remaining):
  quantities = Counter(fish)
  total = 0
  for start_number in range (1,6):
    total += (quantities[start_number] * solve_for_single_fish(start_number, days_remaining))
  return total

fish = read_file()
print(solve(fish, 256))   #1650309278600



# Dynamic programming
dp = {(value,0): 1 for value in range(0,9)}
for day in range (1,257):
  for value in range(0,9):
    if value == 0:
      dp[(value,day)] = dp[(6,day-1)] + dp[(8,day-1)]
    else:
      dp[(value,day)] = dp[(value-1,day-1)]

print(sum( [dp[(start_number, 256)] for start_number in fish]))



counts = Counter(fish)
qty = [0] * 9
for i in range(9):
  qty[i] = counts[i]

for day in range(256):
  qty[(day+7)%9] += qty[day%9]

print(sum(qty))




