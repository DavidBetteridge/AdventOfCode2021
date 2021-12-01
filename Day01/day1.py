from typing import List

def read_file(filename) -> List[int]:
  with open(filename) as f:
    lines = f.readlines()
    return list(map(int, lines))

def part1():
  depths = read_file("Day01/data.txt")
  tuples = zip(depths, depths[1:])
  bigger = len([z for z in tuples if z[1]>z[0]])
  print(bigger)

def part2():
  depths = read_file("Day01/data.txt")
  tuples = zip(depths, depths[1:], depths[2:])
  windows = [sum(z) for z in tuples]
  window_tuples = zip(windows, windows[1:])
  bigger = len([z for z in window_tuples if z[1]>z[0]])
  print(bigger)

part1()
part2()