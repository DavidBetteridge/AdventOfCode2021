from os import read
from typing import List


def read_file() -> List[int]:
  with open("Day06/data.txt") as f:
    return list(map(int, f.read().split(",")))

fish = read_file()

for day in range(1, 81):
  fish = [f-1 for f in fish]
  fish = fish + [8] * len([1 for f in fish if f == -1])
  fish = [6 if f == -1 else f for f in fish]
  # print(f"After {day} day: {fish}")
print(len(fish))  #365131
