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
    self.orientations = [
      pd.DataFrame(data=[], columns=["x", "y", "z"])
      for _ in range(24)
    ]

  def add_beacon(self, beacon: str):
    identity = np.array(beacon.split(","), np.int32)
    for i in range(24):
      new_row = np.dot(rotations[i], identity)
      self.orientations[i].loc[len(self.orientations[i])] = new_row

  # def load_complete(self):
  #   for i in range(len(self.orientations)):
  #     self.orientations[i] = self.orientations[i].sort_values(by=['x','y','z'])

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

    # for scanner in scanners:
    #   scanner.load_complete()
    return scanners
#######################################################

scanners = parse_file()

fixed = scanners[0]
compare = scanners[1]

best_number_of_overlaps = 0
n = compare.orientations[0].shape[0]
for fixed_index in range(fixed.orientations[0].shape[0]):
  fixed_b = fixed.orientations[0].loc[fixed_index]
  for orientation in compare.orientations:
    for possible_first_overlap_index in range(n):
      possible_first_overlap = orientation.loc[possible_first_overlap_index]
      diff = fixed_b - possible_first_overlap
      adjusted = orientation + diff
      # number_of_overlaps = pd.merge(fixed.orientations[0], adjusted, how ='inner', on =['x', 'y', 'z']).shape[0]
      # best_number_of_overlaps = max(best_number_of_overlaps, number_of_overlaps)
print(best_number_of_overlaps)