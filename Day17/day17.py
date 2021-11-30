import math
import dataclasses
from typing import Optional

sample = "target area: x=20..30, y=-10..-5"
data  = "target area: x=265..287, y=-103..-58"


@dataclasses.dataclass(frozen=True)
class Target:
  x1 : int
  x2 : int
  y1 : int
  y2 : int


@dataclasses.dataclass(frozen=True)
class PositionAndVelocity:
  pos_x : int
  pos_y : int
  vel_x : int
  vel_y : int


def step(current: PositionAndVelocity) -> PositionAndVelocity:
  pos_x = current.pos_x + current.vel_x
  pos_y = current.pos_y + current.vel_y
  if current.vel_x > 0:
    vel_x = current.vel_x - 1
  elif current.vel_x < 0:
    vel_x = current.vel_x + 1
  else:
    vel_x = current.vel_x
  vel_y = current.vel_y - 1
  return PositionAndVelocity(pos_x, pos_y, vel_x, vel_y)


def in_target(target: Target, current: PositionAndVelocity ):
  return target.x1 <= current.pos_x <= target.x2 and \
         target.y1 <= current.pos_y <= target.y2

def overshot(target: Target, current: PositionAndVelocity ):
  return current.pos_x > target.x2 or \
         current.pos_y < target.y1

def inverse_triangular_number(x: int) -> int:
  return math.floor(math.sqrt(x * 2))

def fire_probe(startXVel: int, startYVel: int) -> Optional[int]:
  """
    Either returns it's highest position, or None if it misses
  """
  probe = PositionAndVelocity(0, 0, startXVel, startYVel)
  highest = probe.pos_y
  while True:
    probe = step(probe)
    highest = max(highest, probe.pos_y)
    if in_target(target, probe):
      return highest
    if overshot(target, probe):
      return None

sample_target = Target(20, 30, -10, -5)
real_target = Target(265, 287, -103, -58)
target = real_target

answer = 0
hits = 0
misses = 0
x_start = inverse_triangular_number(target.x1)
for startXVel in range(x_start, target.x2+1):
  for startYVel in range(target.y1, 400):
    result = fire_probe(startXVel, startYVel)
    if result is not None:
      answer = max(answer, result)
      hits+=1
    else:
      misses+=1

print(answer)
print(hits)
print(misses)   #131525
assert answer == 5253   #Part 1
assert hits == 1770     #Part 2
