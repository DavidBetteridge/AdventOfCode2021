from collections import defaultdict
import numpy as np
import dataclasses
from typing import List

@dataclasses.dataclass(frozen=True)
class RebootStep:
  on: bool
  minX: int
  minY: int
  minZ: int
  maxX: int
  maxY: int
  maxZ: int

def in_range(reboot_step: RebootStep) -> bool:
  return reboot_step.minX >= -50 and \
         reboot_step.minY >= -50 and \
         reboot_step.minZ >= -50 and \
         reboot_step.maxX <=  50 and \
         reboot_step.maxY <=  50 and \
         reboot_step.maxZ <=  50

def parse_line(line: str) -> RebootStep:
  on, pos = line.split(" ")
  is_on = on == "on"
  x,y,z = pos.split(",")
  minX, maxX = x[2:].split("..")
  minY, maxY = y[2:].split("..")
  minZ, maxZ = z[2:].split("..")
  return RebootStep(is_on, int(minX), int(minY), int(minZ), int(maxX), int(maxY), int(maxZ))

def parse_file() -> List[RebootStep]:
  with open("day22/data.txt") as f:
    lines = f.readlines()
    return [parse_line(l.strip()) for l in lines]

steps = parse_file()

grid = defaultdict(bool)  #keyed by (x,y,z)


for step in steps:
  if in_range(step):
    for x in range(step.minX, step.maxX+1):
      for y in range(step.minY, step.maxY+1):
        for z in range(step.minZ, step.maxZ+1):
          grid[(x,y,z)] = step.on

result = 0
for x in range(-50, 51):
  for y in range(-50, 51):
    for z in range(-50, 51):
      if grid[(x,y,z)]:
        result+=1
print(result)         



