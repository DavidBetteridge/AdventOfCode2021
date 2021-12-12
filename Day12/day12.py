from typing import List, Set
import networkx as nx


def read_file(filename: str) -> List[str]:
  with open(filename) as f:
    return f.readlines()


G = nx.Graph()
for line in read_file("Day12/data.txt"):
  start, end = line.strip().split("-")
  G.add_edge(start, end)


def visit(G, node, path: str, routes: Set):
  for edge in G.edges(node):
    to_edge = edge[1]
    if to_edge == "end":
      routes.add(path + "/" + to_edge)
    else:
      available = to_edge.isupper() or f"/{to_edge}/" not in path
      if f"{node}/{to_edge}" not in path and available:
        visit(G, to_edge, path + "/" + to_edge, routes)


path = "/start"
routes = set()
visit(G, "start", path, routes)

for a in routes:
  print(a)

print(len(routes))

# start,A,b,A,c,A,end
# start,A,b,A,end
# start,A,b,end
# start,A,c,A,b,A,end
# start,A,c,A,b,end
# start,A,c,A,end
# start,A,end
# start,b,A,c,A,end
# start,b,A,end
# start,b,end