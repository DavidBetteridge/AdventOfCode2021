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
