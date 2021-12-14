from collections import defaultdict
from typing import Dict, Tuple


def read_file(filename: str) -> Tuple[str, Dict[str, str]]:
  with open(filename) as f:
    lines = f.readlines()
    template = lines[0].strip()
    rules = [line.strip().split(" -> ") for line in lines[2:]]
    return template, {rule[0]:rule[1] for rule in rules}


template, rules = read_file('Day14/data.txt')

results_cache = {}

def f(result, aa: str, n: int):
  if n == 0:
    result[aa[0]] += 1
    result[aa[1]] += 1
  else:
    if (aa,n) not in results_cache:
      temp = defaultdict(int)
      f(temp, aa[0] + rules[aa], n-1)
      f(temp, rules[aa] + aa[1], n-1)
      temp[rules[aa]] -=1
      results_cache[(aa,n)] = temp

    for l in results_cache[(aa,n)]:
      result[l] += results_cache[(aa,n)][l]

def solve(start_from, n):
  result = defaultdict(int)
  for ind in range(len(start_from)-1):
    key = start_from[ind: ind+2]
    f(result, key, n)
    result[key[1]] -=1
  result[start_from[-1]] +=1
  return result

counts = solve(template, 40)
occurs = sorted(counts, key = lambda k : counts[k], reverse=True)
print(counts[occurs[0]]- counts[occurs[-1]])

