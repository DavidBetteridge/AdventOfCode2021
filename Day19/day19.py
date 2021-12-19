from typing import List
import numpy as np

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

def all_rotations_of_vector(vector: np.array) -> List[np.array]:
  all = []
  for rotation in rotations:
    all.append(np.dot(rotation, vector))
  return all

class Scanner:
  def __init__(self, number: int):
    self.number = number
    self.orientations = [[] for _ in range(24)]
  def add_beacon(self, beacon: str):
    identity = np.array(beacon.split(","), np.int32)
    for i in range(24):
      self.orientations[i].append(np.dot(rotations[i], identity))

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
    return scanners


scanners = parse_file()
print(scanners.beacons)

beacon = np.array([8,0,7])
all = all_rotations_of_vector(beacon)
print(len(all))
