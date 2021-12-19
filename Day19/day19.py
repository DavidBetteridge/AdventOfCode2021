from typing import List
import numpy as np
import pandas as pd

rotations = []

rotations.append(np.array([
  [1, 0, 0],
  [0, 1, 0],
  [0, 0, 1]
], np.int32))

rotations.append(np.array([
  [0, 0, 1],
  [0, 1, 0],
  [-1, 0, 0]
], np.int32))

rotations.append(np.array([
  [-1, 0, 0],
  [0, 1, 0],
  [0, 0, -1]
], np.int32))

rotations.append(np.array([
  [0, 0, -1],
  [0, 1, 0],
  [1, 0, 0]
], np.int32))

rotations.append(np.array([
  [0, -1, 0],
  [1, 0, 0],
  [0, 0, 1]
], np.int32))

rotations.append(np.array([
  [0, 0, 1],
  [1, 0, 0],
  [0, 1, 0]
], np.int32))

rotations.append(np.array([
  [0, 1, 0],
  [1, 0, 0],
  [0, 0, -1]
], np.int32))

rotations.append(np.array([
  [0, 0, -1],
  [1, 0, 0],
  [0, -1, 0]
], np.int32))

rotations.append(np.array([
  [0, 1, 0],
  [-1, 0, 0],
  [0, 0, 1]
], np.int32))

rotations.append(np.array([
  [0, 0, 1],
  [-1, 0, 0],
  [0, -1, 0]
], np.int32))

rotations.append(np.array([
  [0, -1, 0],
  [-1, 0, 0],
  [0, 0, -1]
], np.int32))

rotations.append(np.array([
  [0, 0, -1],
  [-1, 0, 0],
  [0, 1, 0]
], np.int32))

rotations.append(np.array([
  [1, 0, 0],
  [0, 0, -1],
  [0, 1, 0]
], np.int32))

rotations.append(np.array([
  [0, 1, 0],
  [0, 0, -1],
  [-1, 0, 0]
], np.int32))

rotations.append(np.array([
  [-1, 0, 0],
  [0, 0, -1],
  [0, -1, 0]
], np.int32))

rotations.append(np.array([
  [0, -1, 0],
  [0, 0, -1],
  [1, 0, 0]
], np.int32))

rotations.append(np.array([
  [1, 0, 0],
  [0, -1, 0],
  [0, 0, -1]
], np.int32))

rotations.append(np.array([
  [0, 0, -1],
  [0, -1, 0],
  [-1, 0, 0]
], np.int32))

rotations.append(np.array([
  [-1, 0, 0],
  [0, -1, 0],
  [0, 0, 1]
], np.int32))

rotations.append(np.array([
  [0, 0, 1],
  [0, -1, 0],
  [1, 0, 0]
], np.int32))

rotations.append(np.array([
  [1, 0, 0],
  [0, 0, 1],
  [0, -1, 0]
], np.int32))

rotations.append(np.array([
  [0, -1, 0],
  [0, 0, 1],
  [-1, 0, 0]
], np.int32))

rotations.append(np.array([
  [-1, 0, 0],
  [0, 0, 1],
  [0, 1, 0]
], np.int32))

rotations.append(np.array([
  [0, 1, 0],
  [0, 0, 1],
  [1, 0, 0]
], np.int32))

#######################################################
class Scanner:
  def __init__(self, number: int):
    self.number = number
    self.orientations = [ np.empty([0, 3]) for _ in range(24)
    ]

  def add_beacon(self, beacon: str):
    identity = np.array(beacon.split(","), np.int32)
    for i in range(24):
      new_row = np.dot(rotations[i], identity)
      self.orientations[i] = np.vstack([self.orientations[i], new_row])

def parse_file() -> List[Scanner]:
  with open("day19/sample.txt") as f:
    lines = f.readlines()
    scanner_number = -1
    scanner = None
    scanners = []
    for line in lines:
      #--- scanner 0 ---
      if line.startswith("---"):
        if scanner is not None:
          scanners.append(scanner)
        scanner = Scanner(scanner_number)
      elif line.strip() != "":
        scanner.add_beacon(line.strip())
    scanners.append(scanner)
    return scanners
#######################################################

def count_matches(lhs: np.array, rhs: np.array) -> int:
  return sum([len(np.where((rhs[:,0] == lhs[i][0]) & (rhs[:,1]==lhs[i][1]) & (rhs[:,2]==lhs[i][2]))[0])
         for i in range(len(lhs))])

#######################################################

scanners = parse_file()

fixed = scanners[0].orientations[0]
compare = scanners[1]

best_number_of_overlaps = 0
n = len(compare.orientations[0])
m = len(fixed)
for fixed_index in range(m):
  fixed_b = fixed[fixed_index]
  for orientation in compare.orientations:
    for possible_first_overlap_index in range(n):
      possible_first_overlap = orientation[possible_first_overlap_index]
      diff = fixed_b - possible_first_overlap
      adjusted = orientation + diff
      number_of_overlaps = count_matches(fixed, adjusted)
      best_number_of_overlaps = max(best_number_of_overlaps, number_of_overlaps)
print(best_number_of_overlaps)