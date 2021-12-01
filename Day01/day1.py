from typing import List

def read_file(filename) -> List[str]:
  with open(filename) as f:
    return f.readlines()


depths = read_file("Day01/data.txt")
depths = list(map(int, depths))
tuples = zip(depths, depths[1:])
bigger = len([z for z in tuples if z[1]>z[0]])
print(bigger)