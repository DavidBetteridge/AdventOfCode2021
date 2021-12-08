from typing import Counter, List, Tuple


def parse_line(line:str) -> Tuple[List[str], List[str]]:
  all_inputs, all_outputs = line.split(" | ")
  return all_inputs.strip().split(" "), all_outputs.strip().split(" ")

def read_file() -> List[Tuple[List[str], List[str]]]:
  with open("Day08/data.txt") as f:
    lines = f.readlines()
    return [parse_line(l) for l in lines ]
    
def part1():
  line = read_file()
  running_total = 0
  for inputs, outputs in line:
    lengths = [len(o) for o in outputs] 
    c = Counter(lengths)
    running_total += c[2] + c[3] + c[4] + c[7]
  print(running_total)  #456
  


lines = read_file()
running_total = 0
for inputs, outputs in lines:
  all = inputs + outputs
  unique = set(["".join(sorted(set(a))) for a in all])
  unique_joined = "".join(unique)
  counts = Counter(unique_joined)  

  # b is the letter which is in exactly 6 segments
  for k in counts:
    if counts[k] == 6:
      segment_b = k
      break

  # e is the letter which is in exactly 4 segments
  for k in counts:
    if counts[k] == 4:
      segment_e = k
      break

  
  # Number 1 - has length 2
  digits_for_number_one = "".join(sorted(set(next(o for o in all if len(o) == 2))))

  # Number 2 - has length 5 and contains e but not b
  digits_for_number_two = "".join(sorted(set(next(o for o in all if len(o) == 5 and segment_e in o and segment_b not in o)) ))

  # Number 3 - has length 5 and no e or b
  digits_for_number_three = "".join(sorted(set(next(o for o in all if len(o) == 5 and segment_e not in o and segment_b not in o)) ))

  # Number 4 - has length 4
  digits_for_number_four = "".join(sorted(set(next(o for o in all if len(o) == 4))))

  # Number 5 - has length 5 and contains b
  digits_for_number_five = "".join(sorted(set(next(o for o in all if len(o) == 5 and segment_b in o))))

  # Number 7 - has length 3
  digits_for_number_seven = "".join(sorted(set(next(o for o in all if len(o) == 3))))

  # Number 8 - has length 7
  digits_for_number_eight = "".join(sorted(set(next(o for o in all if len(o) == 7))))

  # Number 9 - has length 8 and no segment_e
  digits_for_number_nine = "".join(sorted(set(next(o for o in all if len(o) == 6 and segment_e not in o))))

  segment_d = set(digits_for_number_four).difference(set(digits_for_number_one)).difference([segment_b]).pop()

  digits_for_number_zero = "".join(sorted(set(next(o for o in all if len(o) == 6 and segment_d not in o))))

  digits_for_number_six = unique.difference([digits_for_number_zero, digits_for_number_one, digits_for_number_two, digits_for_number_three,
                                             digits_for_number_four, digits_for_number_five, digits_for_number_seven,
                                             digits_for_number_eight, digits_for_number_nine]).pop()


  m = {
    digits_for_number_zero: "0",
    digits_for_number_one: "1",
    digits_for_number_two: "2",
    digits_for_number_three: "3",
    digits_for_number_four: "4",
    digits_for_number_five: "5",
    digits_for_number_six: "6",
    digits_for_number_seven: "7",
    digits_for_number_eight: "8",
    digits_for_number_nine: "9",
  }

  result = ""
  for o in outputs:
    result += m["".join(sorted(o))]
  running_total += int(result)

print(running_total)
