from typing import Counter, Dict, List, Tuple


def read_file(filename: str) -> Tuple[str, Dict[str, str]]:
  with open(filename) as f:
    lines = f.readlines()
    template = lines[0].strip()
    rules = [line.strip().split(" -> ") for line in lines[2:]]
    return template, {rule[0]:rule[1] for rule in rules}

def step(start_from: str):
  next = ""
  for ind in range(len(start_from)-1):
    key = start_from[ind: ind+2]
    insert_element = rules[key]
    next += start_from[ind] + insert_element
  return next + start_from[-1]

template, rules = read_file('Day14/data.txt')
next = template
for s in range(10):
  next = step(next)

c = Counter(next)
ordered =  c.most_common(None)
most = ordered[0]
least = ordered[-1]
print(most[1] - least[1])


