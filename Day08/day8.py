from typing import Counter, List, Tuple

def sort_values(values: List[str]) -> str:
  return ["".join(sorted(value)) for value in values]

def parse_line(line:str) -> Tuple[List[str], List[str]]:
  all_inputs, all_outputs = line.split(" | ")
  return sort_values(all_inputs.strip().split(" ")), sort_values(all_outputs.strip().split(" "))

def read_file() -> List[Tuple[List[str], List[str]]]:
  with open("Day08/data.txt") as f:
    lines = f.readlines()
    return [parse_line(l) for l in lines ]
    
def part1():
  line = read_file()
  running_total = 0
  for _, outputs in line:
    lengths = [len(o) for o in outputs] 
    c = Counter(lengths)
    running_total += c[2] + c[3] + c[4] + c[7]
  print(running_total)  #456
  

def where(all_possibilities: List[str],
          length_is: int, 
          must_contain: List[str] = [],
          must_not_contain: List[str] = []):
  possible = [o for o in all_possibilities 
              if len(o) == length_is and \
                 all(must in o for must in must_contain) and \
                 not any(must in o for must in must_not_contain)]
  return possible[0]

def solve_line(inputs, outputs):
  all_possibilities = set(inputs + outputs)
  counts = Counter("".join(all_possibilities))  

  # b is the letter which is in exactly 6 segments
  segment_b = [k for k in counts if counts[k] == 6][0]

  # e is the letter which is in exactly 4 segments
  segment_e = [k for k in counts if counts[k] == 4][0]

  mapping = {}
  mapping[1] = where(all_possibilities, length_is=2)
  mapping[2] = where(all_possibilities, length_is=5, must_contain=[segment_e], must_not_contain=[segment_b])
  mapping[3] = where(all_possibilities, length_is=5, must_not_contain=[segment_b, segment_e])
  mapping[4] = where(all_possibilities, length_is=4)
  mapping[5] = where(all_possibilities, length_is=5, must_contain=[segment_b])
  mapping[7] = where(all_possibilities, length_is=3)
  mapping[8] = where(all_possibilities, length_is=7)
  mapping[9] = where(all_possibilities, length_is=6, must_not_contain=[segment_e])
  segment_d = set(mapping[4]).difference(set(mapping[1])).difference([segment_b]).pop()
  mapping[0] = where(all_possibilities, length_is=6, must_not_contain=[segment_d])
  mapping[6] = all_possibilities.difference([mapping[0], mapping[1], mapping[2], mapping[3],
                                              mapping[4], mapping[5], mapping[7],
                                              mapping[8], mapping[9]]).pop()
  mapping = {v:str(k) for k,v in mapping.items()}

  return int("".join(mapping[o] for o in outputs))


def part2():
  lines = read_file()
  running_total = sum(solve_line(inputs, outputs) for inputs, outputs in lines)
  print(running_total)  #1091609