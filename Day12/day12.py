from typing import List, Set
import networkx as nx


def read_file(filename: str) -> List[str]:
  with open(filename) as f:
    return f.readlines()


G = nx.Graph()
for line in read_file("Day12/data.txt"):
  start, end = line.strip().split("-")
  G.add_edge(start, end)


def visit(G, node, path: str, routes: Set, small_cave_visited_twice: bool):
  for edge in G.edges(node):
    scvt = small_cave_visited_twice
    to_edge = edge[1]
    if to_edge == "end":
      routes.add(path + "/" + to_edge)
    else:
      is_start = to_edge == "start"
      is_small_cave = to_edge.islower()
      already_visited = f"/{to_edge}/" in path

      if is_start:
        available = False
      else:
        if is_small_cave:
          if scvt:
            available = not already_visited
          else:
            available = True
            scvt = already_visited
        else: 
          available = True

      if available:
        visit(G, to_edge, path + "/" + to_edge, routes, scvt)


path = "/start"
routes = set()
visit(G, "start", path, routes, small_cave_visited_twice = True)
print(len(routes))


path = "/start"
routes = set()
visit(G, "start", path, routes, small_cave_visited_twice = False)
print(len(routes))
