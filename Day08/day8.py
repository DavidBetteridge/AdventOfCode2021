from os import read
from typing import Counter, List


def parse_line(line:str):
  all_inputs, all_outputs = line.split(" | ")
  return list(all_outputs.strip().split(" "))

def read_file() -> List[List[str]]:
  with open("Day08/data.txt") as f:
    lines = f.readlines()
    return [parse_line(l) for l in lines ]
    

lines = read_file()
running_total = 0
for l in lines:
  lengths = [len(o) for o in l] 
  c = Counter(lengths)
  running_total += c[2] + c[3] + c[4] + c[7]
print(running_total)
  
