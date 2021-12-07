from functools import lru_cache
from typing import List


def read_file() -> List[int]:
  with open("Day07/data.txt") as f:
    return list(map(int, f.read().split(",")))

def part1():
  positions = read_file()
  min_x = min(positions)
  max_x = max(positions)

  best_score = 99999999
  for x in range(min_x, max_x+1):
    score = sum( abs(x - p) for p in positions )
    best_score = min(best_score, score)

  print(best_score)   #343468



@lru_cache
def cost(n: int) -> int:
  return (n * ( n + 1 )) / 2

def part2():
  positions = read_file()
  min_x = min(positions)
  max_x = max(positions)

  best_score = 99999999
  for x in range(min_x, max_x+1):
    score = sum( cost(abs(x - p)) for p in positions )
    best_score = min(best_score, score)

  print(best_score)   #96086265


part2()



