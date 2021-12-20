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

  def add_beacon_from_string(self, beacon: str):
    identity = np.array(beacon.split(","), np.int32)
    for i in range(24):
      new_row = np.dot(rotations[i], identity)
      self.orientations[i] = np.vstack([self.orientations[i], new_row])

  def add_beacon(self, identity: np.array):
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
        scanner.add_beacon_from_string(line.strip())
    scanners.append(scanner)
    return scanners
#######################################################

def count_matches(lhs: np.array, rhs: np.array) -> int:
  return sum([1 if np.equal(lhs[i], rhs).all(axis=1).any() else 0
         for i in range(len(lhs))])


def try_merge(fixed_scanner: Scanner, scanner_to_test: Scanner) -> bool:
  best_number_of_overlaps = 0
  best_beacons = None

  fixed = fixed_scanner.orientations[0]
  n = len(scanner_to_test.orientations[0])
  for fixed_index in range(len(fixed)):
    fixed_b = fixed[fixed_index]
    for orientation_no, orientation in enumerate(scanner_to_test.orientations):
      for possible_first_overlap_index in range(n):
        possible_first_overlap = orientation[possible_first_overlap_index]
        adjusted = orientation + fixed_b - possible_first_overlap
        number_of_overlaps = count_matches(fixed, adjusted)
        if number_of_overlaps > best_number_of_overlaps:
          best_number_of_overlaps = number_of_overlaps
          # best_orientation = orientation_no
          # best_offset = fixed_b - possible_first_overlap
          best_beacons = adjusted

  if best_number_of_overlaps >= 12:
    # Any beacons in best_beacons which aren't in fixed need to
    # be added to fixed_scanner
    for beacon in best_beacons:
      if not np.equal(beacon, fixed).all(axis=1).any():
        fixed_scanner.add_beacon(beacon)
    return True
  else:
    return False

def next_merge(scanners: List[Scanner]) -> List[Scanner]:
  for a in range(len(scanners)-1):
    for b in range(a+1, len(scanners)):
      if (try_merge(scanners[a], scanners[b])):
        return scanners[:b] + scanners[b+1:]  
  return scanners        


#######################################################

scanners = parse_file()
while len(scanners) > 1:
  print(len(scanners))
  scanners = next_merge(scanners)

print("Scanners")
answer = len(scanners[0].orientations[0])
print(answer)

# print(can_overlap(scanners[0], scanners[1]))
# print(can_overlap(scanners[1], scanners[4]))


