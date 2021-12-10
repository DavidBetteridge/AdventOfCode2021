from typing import List


def read_file(filename: str) -> List[str]:
  with open(filename) as f:
    return f.readlines()

pairs = {
  ")" : "(",
  "]" : "[",
  "}" : "{",
  ">" : "<"  
}

closing = {
  ")" : 3,
  "]" : 57,
  "}" : 1197,
  ">" : 25137
}

def check_line(line: str) -> int:
  s = []
  for c in line:
    if not c in closing:
      s.append(c)
    else:
      top = s.pop()
      if top != pairs[c]:
        return closing[c]
  return 0


lines = read_file("day10/data.txt")
result = sum(check_line(line) for line in lines)
print(result)