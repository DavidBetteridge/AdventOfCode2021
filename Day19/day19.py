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
  with open("day19/data.txt") as f:
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

def try_merge(fixed_scanner: Scanner, scanner_to_test: Scanner) -> bool:
  fixed = fixed_scanner.orientations[0]
  n = len(scanner_to_test.orientations[0])
  for fixed_index in range(len(fixed)):
    fixed_b = fixed[fixed_index]
    for orientation in scanner_to_test.orientations:
      for possible_first_overlap_index in range(n):
        possible_first_overlap = orientation[possible_first_overlap_index]
        adjusted = orientation + fixed_b - possible_first_overlap

        if sum([1 if np.equal(fixed[i], adjusted).all(axis=1).any() else 0
            for i in range(len(fixed))]) >= 12:
          # Any beacons in best_beacons which aren't in fixed need to
          # be added to fixed_scanner
          for beacon in adjusted:
            if not np.equal(beacon, fixed).all(axis=1).any():
              fixed_scanner.add_beacon(beacon)
          return True
  return False

def next_merge(scanners: List[Scanner]) -> List[Scanner]:
  a = 0
  while a < len(scanners) - 1:
    b = a + 1
    while b < len(scanners) :
      if (try_merge(scanners[a], scanners[b])):
        # Remove B from the list of scanners,  but don't advance the index
        scanners = scanners[:b] + scanners[b+1:]
        print(len(scanners))
      else:
        b += 1
    a += 1
  return scanners        


#######################################################

scanners = parse_file()
while len(scanners) > 1:
  scanners = next_merge(scanners)

print("Scanners")
answer = len(scanners[0].orientations[0])
print(answer)
