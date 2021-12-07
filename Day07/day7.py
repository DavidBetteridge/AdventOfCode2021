from functools import lru_cache
from typing import List
import timeit

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





def part2():
  @lru_cache
  def cost(n: int) -> int:
    return (n * ( n + 1 )) / 2

  positions = read_file()
  min_x = min(positions)
  max_x = max(positions)
  
  return min([sum( cost(abs(x - p))
              for p in positions)
              for x in range(min_x, max_x+1)])

def part2b():
  def cost(n: int) -> int:
    return (n * ( n + 1 )) / 2

  positions = read_file()
  min_x = min(positions)
  max_x = max(positions)
  
  return min([sum( cost(abs(x - p))
              for p in positions)
              for x in range(min_x, max_x+1)])


def solve(cost):
  positions = read_file()
  min_x = min(positions)
  max_x = max(positions)
  
  return min([sum( cost(abs(x - p))
              for p in positions)
              for x in range(min_x, max_x+1)])

print(solve(lambda n: n))  #Part 1
print(solve(lambda n: (n * ( n + 1 )) / 2))  #Part 2