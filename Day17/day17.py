import dataclasses

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


sample_target = Target(20, 30, -10, -5)
real_target = Target(265, 287, -103, -58)
target = real_target

startXVel = 0
x_too_small = True
x_too_big = False
answer = 0
while not x_too_big:
  startYVel = 10
  y_overshot = False
  while not y_overshot:
    probe = PositionAndVelocity(0, 0, startXVel, startYVel)
    fire = True
    highest = probe.pos_y
    while fire:
      probe = step(probe)
      if in_target(target, probe):
        x_too_small = False
        answer = max(answer, highest)
        print(f"Hit target {startXVel}, {startYVel} - Height was {highest}")
        break
      if overshot(sample_target, probe):
        y_overshot = True
        print(f"Missed {startXVel}, {startYVel} x_too_small={x_too_small}  x_too_big={x_too_big}")
        if not x_too_small and startYVel == 0: x_too_big = True
        break
      highest = max(highest, probe.pos_y)
    startYVel+=1
  startXVel+=1
print(answer)