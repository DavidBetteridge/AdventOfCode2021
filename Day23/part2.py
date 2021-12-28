import networkx as nx
import copy
from typing import List, Tuple

amphipod_info =[
  ("A", 1),
  ("A", 1),
  ("A", 1),
  ("A", 1),
  ("B", 10),
  ("B", 10),
  ("B", 10),
  ("B", 10),
  ("C", 100),
  ("C", 100),
  ("C", 100),
  ("C", 100),
  ("D", 1000),
  ("D", 1000),
  ("D", 1000),
  ("D", 1000),
]


amphipod_sets = {
  "A" : [0,1,2,3],
  "B" : [4,5,6,7],
  "C" : [8,9,10,11],
  "D" : [12,13,14,15],
}

room_entries = {
  "A" : 2,
  "B" : 4,
  "C" : 6,
  "D" : 8,
}

def find_moves_for(locations, current_state, amphipod_number: int) -> List[Tuple[List[str], int]]:
  current_location = current_state[amphipod_number]
  if len(current_location) == 1: return [] # Room is complete
  in_room = current_location[0] != 'P'
  amphipod_type, amphipod_cost = amphipod_info[amphipod_number]
  possible_moves = []

  if in_room:
    # We are in a room,  so we can move into the corridor or another room.
    room_type = current_location[0]
    room_position = int(current_location[1])

    if amphipod_type == room_type and all([locations[f"{room_type}{r}"] == amphipod_type 
                                           for r in [0,1,2,3]
                                           if r <= room_position]):
      #print(f"Home")
      return []
   
    if in_room and any(locations[f"{room_type}{r}"] != "" for r in [0,1,2,3] if r > room_position):
      #print(f"Blocked in")
      return []

    # We are in the room,  but we can move out into the corridor
    # C0....C10   We cannot stop on 2,4,6,8
    leave_at = room_entries[room_type]

    #Cost to exit the room
    basecost = max([0,1,2,3]) - room_position + 1 # Cost of leaving the room

    # Moving left
    i = leave_at
    cost = basecost
    while i >= 0 and locations[f"P{i}"] == "":
      if i not in (2,4,6,8):
        temp = copy.deepcopy(current_state)
        temp[amphipod_number] = f"P{i}"
        possible_moves.append((temp, amphipod_cost*cost))
      cost+=1
      i -= 1

    # Moving right
    i = leave_at
    cost = basecost
    while i <= 10 and locations[f"P{i}"] == "":
      if i not in (2,4,6,8):
        temp = copy.deepcopy(current_state)
        temp[amphipod_number] = f"P{i}"        
        possible_moves.append((temp, amphipod_cost*cost))
      cost+=1
      i += 1

    current_position = leave_at  # Where do we enter the corridor
  else:
    current_position = int(current_location[1:])
    basecost = 0

  # We are in a corridor.  We can only enter our own rooms if noone else is in it.
  can_enter_room = all([locations[f"{amphipod_type}{r}"] == "" or locations[f"{amphipod_type}{r}"][0] == amphipod_type 
                       for r in [0,1,2,3]])

  if can_enter_room:
    # And there is a path from here?
    enter_at = room_entries[amphipod_type]
    cost = basecost
    blocked = False
    if current_position < enter_at:
      # Move right
      i = current_position + 1
      cost += 1
      while (i < enter_at) and not blocked:
        if locations[f"P{i}"] != "":
          blocked=True
        i += 1
        cost += 1
    else:
      # Move left
      i = current_position - 1
      cost += 1
      while (i > enter_at) and not blocked:
        if locations[f"P{i}"] != "":
          blocked=True
        i -= 1
        cost += 1
    assert blocked or i == enter_at

    if not blocked:
      # We always enter our room if we can
      current_location = 4
      while current_location>0 and locations[f"{amphipod_type}{current_location-1}"] == "":
        cost += 1
        current_location -= 1
      assert current_location != 4

      temp = copy.deepcopy(current_state)
      if current_location == 3:
        # The room is now full
        for a in amphipod_sets[amphipod_type]:
          temp[a] = f"{amphipod_type}"             
      else:
        temp[amphipod_number] = f"{amphipod_type}{current_location}"             
      
      return [(temp, amphipod_cost*cost)]          
      
  return possible_moves


def find_moves(current_state) -> List[Tuple[Tuple, int]]:

  locations = {
    "P0" : "",
    "P1" : "",
    "P2" : "",
    "P3" : "",
    "P4" : "",
    "P5" : "",
    "P6" : "",
    "P7" : "",
    "P8" : "",
    "P9" : "",
    "P10" : "",
    "A0" : "",
    "A1" : "",
    "A2" : "",
    "A3" : "",
    "B0" : "",
    "B1" : "",
    "B2" : "",
    "B3" : "",
    "C0" : "",
    "C1" : "",
    "C2" : "",
    "C3" : "",
    "D0" : "",
    "D1" : "",
    "D2" : "",
    "D3" : "",
  }

  for amphipod_number in range(16):
    amphipod_type, _ = amphipod_info[amphipod_number]
    locations[current_state[amphipod_number]] = amphipod_type

  possible_moves = []
  for amphipod_number in range(16):
    possible_moves = possible_moves + find_moves_for(locations, current_state, amphipod_number)
  return possible_moves



G = nx.DiGraph()

starting_position = [ "A0","C1","D0","D2",  "A3","B1","C2","C3",  "B2","B3","C0","D1",  "A1","A2","B0","D3" ]  #Simple
starting_position = [ "B3", "C0", "C1", "D2",     "B1", "C2", "C3", "D0",   "A3", "B0", "B2", "D1",    "A0", "A1", "A2", "D3" ]  #Real

target_position = ["A","A","A","A", "B", "B","B","B", "C", "C", "C", "C", "D", "D", "D", "D"]
G.add_node("-".join(starting_position))
todo = ["-".join(starting_position)]
processed = set()

while len(todo) > 0:
  next_position = todo.pop()
  if not next_position in processed:
    processed.add(next_position)

    possible_moves = find_moves(next_position.split("-"))
    for possible_move in possible_moves:
      following_state = "-".join(possible_move[0])
    #  print(f"{next_position}=>{following_state} = {possible_move[1]}")
      G.add_edge(next_position, following_state, weight = possible_move[1])
      if not following_state in processed:
        todo.append(following_state)
   # print("")
print(G)
total, route = (nx.single_source_dijkstra(G,
          source="-".join(starting_position),
          target="-".join(target_position),
          weight='weight'))
print(route)
print(total)  #15358
