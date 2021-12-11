import re
import statistics
from typing import List

def read_file(filename: str) -> List[str]:
  with open(filename) as f:
    lines = f.readlines()
    return [line.strip() for line in lines]

opening = {
    "(" : 1,
    "[" : 2,
    "{" : 3,
    "<" : 4
  }

closing = {
  ")" : ("(", 3),
  "]" : ("[", 57),
  "}" : ("{", 1197),
  ">" : ("<",  25137)
}

def part1(lines: List[str]):

  def score_corrupted_line(line: str) -> int:
    s = []
    for c in line:
      if c in opening:
        s.append(c)
      else:
        expected_opening, score = closing[c]
        if s.pop() != expected_opening:
          return score
    return 0

  result = sum(score_corrupted_line(line) for line in lines)
  print(result)     #389589


def part2(lines: List[str]):
  def score_to_complete_line(line: str) -> int:
    s = []
    for c in line:
      if c in opening:
        s.append(c)
      else:
        expected_opening, score = closing[c]
        if s.pop() != expected_opening:
          return 0
    
    score = 0
    while len(s) > 0:
      score *= 5
      score += opening[s.pop()]
    return score

  results = [score for line in lines if (score := score_to_complete_line(line)) != 0]
  print(statistics.median(results))  #1190420163

lines = read_file("day10/data.txt")
part1(lines)
part2(lines)


def part1_no_stack(line):
  while line != (line := re.sub('(\[])|({})|(\(\))|(<>)', '', line)):
    pass
  
  first_close = min([location for c in closing
                     if (location := line.find(c)) != -1],
                    default=None)
  if first_close:
    return closing[line[first_close]][1]
  return 0

print(sum(part1_no_stack(line) for line in lines))


def part2_no_stack(line):
  while line != (line := re.sub('(\[])|({})|(\(\))|(<>)', '', line)):
    pass
  
  if not any([c in line for c in [")","]","}",">"]]):
    return sum([["", "(","[","{","<"].index(t) * 5**i for i, t in enumerate(line)])
  return 0

results = [score for line in lines if (score := part2_no_stack(line)) != 0]
print(statistics.median(results))  #1190420163





