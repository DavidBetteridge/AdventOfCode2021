import numpy as np
from typing import List
from numba import jit

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
    self.locations = [ np.array([0,0,0]) ]
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
    for orientation_index, orientation in enumerate(scanner_to_test.orientations):
      for possible_first_overlap_index in range(n):
        possible_first_overlap = orientation[possible_first_overlap_index]
        adjusted = orientation + fixed_b - possible_first_overlap

        if overlaps(fixed, adjusted):
          # Any beacons in best_beacons which aren't in fixed need to
          # be added to fixed_scanner
          diff = possible_first_overlap - fixed_b
          for a in scanner_to_test.locations:
            new_a = np.dot(rotations[orientation_index], a)
            fixed_scanner.locations.append(new_a + diff)

          for beacon in adjusted:
            if not np.equal(beacon, fixed).all(axis=1).any():
              fixed_scanner.add_beacon(beacon)
          return True
  return False

@jit
def overlaps(lhs: np.array, rhs: np.array) -> int:
  lookup = [(x[0],x[1],x[2]) for x in rhs]
  count=0
  for x in lhs:
    key = (x[0],x[1],x[2])
    if key in lookup:
      count+=1
      if count == 12: return True
  return False

def next_merge(scanners: List[Scanner]) -> List[Scanner]:
  a: int = 0
  while a < len(scanners) - 1:
    b = a + 1
    while b < len(scanners) :
      if try_merge(scanners[a], scanners[b]):
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

print(scanners[0].locations)
print("")

answer = 0
for a in scanners[0].locations:
  for b in scanners[0].locations:
    md = abs(a[0]-b[0])+abs(a[1]-b[1])+abs(a[2]-b[2])
    answer = max(answer, md)
print(answer)  #3621, 12226