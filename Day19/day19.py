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

def parse_file() -> List[Scanner]:
  with open("day19/small.txt") as f:
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

scanners = parse_file()
print(len(scanners))