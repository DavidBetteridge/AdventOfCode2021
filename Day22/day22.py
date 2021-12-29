import dataclasses
from typing import List

@dataclasses.dataclass(frozen=True)
class RebootStep:
  on: bool
  minX: int
  maxX: int
  minY: int
  maxY: int
  minZ: int
  maxZ: int

  def volume(self) -> int:
    return (self.maxX - self.minX + 1) * (self.maxY - self.minY + 1) * (self.maxZ - self.minZ + 1)

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
  return RebootStep(is_on, int(minX), int(maxX), int(minY), int(maxY), int(minZ), int(maxZ))

def intersects(a: RebootStep, b: RebootStep) -> bool:
  if a.maxX < b.minX: return False
  if a.minX > b.maxX: return False
  if a.maxY < b.minY: return False
  if a.minY > b.maxY: return False
  if a.maxZ < b.minZ: return False
  if a.minZ > b.maxZ: return False
  return True

def split(a: RebootStep, b: RebootStep) -> List[RebootStep]:
  # Split cube A into multiple cubes based on the dimension of b
  remainder = a
  new_cubes = []

  # Left slice
  if remainder.minX < b.minX <= remainder.maxX:
    new_cubes.append(RebootStep(True, remainder.minX, b.minX-1, remainder.minY, remainder.maxY, remainder.minZ, remainder.maxZ))
    remainder = RebootStep(True, b.minX, remainder.maxX, remainder.minY, remainder.maxY, remainder.minZ, remainder.maxZ)

  # right slice
  if remainder.minX <= b.maxX < remainder.maxX:
    new_cubes.append(RebootStep(True, b.maxX+1, remainder.maxX, remainder.minY, remainder.maxY, remainder.minZ, remainder.maxZ))
    remainder = RebootStep(True, remainder.minX, b.maxX, remainder.minY, remainder.maxY, remainder.minZ, remainder.maxZ)

  # Bottom slice
  if remainder.minY < b.minY <= remainder.maxY:
    new_cubes.append(RebootStep(True, remainder.minX, remainder.maxX, remainder.minY, b.minY-1, remainder.minZ, remainder.maxZ))
    remainder = RebootStep(True, remainder.minX, remainder.maxX, b.minY, remainder.maxY, remainder.minZ, remainder.maxZ)

  # Top slice
  if remainder.minY <= b.maxY < remainder.maxY:
    new_cubes.append(RebootStep(True, remainder.minX, remainder.maxX, b.maxY+1, remainder.maxY, remainder.minZ, remainder.maxZ))
    remainder = RebootStep(True, remainder.minX, remainder.maxX, remainder.minY, b.maxY, remainder.minZ, remainder.maxZ)

  # Front slice
  if remainder.minZ < b.minZ <= remainder.maxZ:
    new_cubes.append(RebootStep(True, remainder.minX, remainder.maxX, remainder.minY, remainder.maxY, remainder.minZ, b.minZ-1))
    remainder = RebootStep(True, remainder.minX, remainder.maxX, remainder.minY, remainder.maxY, b.minZ, remainder.maxZ)

  #Back Slice
  if remainder.minZ <= b.maxZ < remainder.maxZ:
    new_cubes.append(RebootStep(True, remainder.minX, remainder.maxX, remainder.minY, remainder.maxY, b.maxZ+1, remainder.maxZ))
    remainder = RebootStep(True, remainder.minX, remainder.maxX, remainder.minY, remainder.maxY, remainder.minZ, b.maxZ)
  return new_cubes, remainder



def parse_file() -> List[RebootStep]:
  with open("day22/data.txt") as f:
    lines = f.readlines()
    return [parse_line(l.strip()) for l in lines]

steps = parse_file()
cubes = [steps[0]]

for step_number, step in enumerate(steps[1:]):
  new_cubes = []
  for cube in cubes:
    if intersects(step, cube) or intersects(cube, step):
      # Existing cube needs splitting so that the new cube is removed.
      to_add, _  = split(cube, step)
      new_cubes += to_add
    else:
      # Existing cube isn't changed
      new_cubes.append(cube)

  if step.on:
    new_cubes.append(step)

  cubes = new_cubes

result = sum(c.volume() for c in cubes)
print(result)




