import networkx as nx
import copy
from typing import List, Tuple

amphipod_info =[
  ("A", 1, 1),
  ("A", 0, 1),
  ("B", 3, 10),
  ("B", 2, 10),
  ("C", 5, 100),
  ("C", 4, 100),
  ("D", 7, 1000),
  ("D", 6, 1000),
]


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
  amphipod_type, pair_number, amphipod_cost = amphipod_info[amphipod_number]
  possible_moves = []

  if in_room:
    # We are in a room,  so we can move into the corridor or another room.
    room_type = current_location[0]
    room_position = int(current_location[1])
    if amphipod_type == room_type and room_position == 0:
      #print(f"Home")
      return []
   
    if in_room and room_position == 0 and locations[f"{room_type}1"] != "":
      #print(f"Blocked in")
      return []

    # We are in the room,  but we can move out into the corridor
    # C0....C10   We cannot stop on 2,4,6,8
    leave_at = room_entries[room_type]

    #Cost to exit the room
    basecost = 1 if room_position == 1 else 2 # Cost of leaving the room

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
  can_enter_room = (locations[f"{amphipod_type}0"] == "" or locations[f"{amphipod_type}0"][0] == amphipod_type) and \
                    (locations[f"{amphipod_type}1"] == "")
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

    if not blocked:
      assert i == enter_at
      # We always enter our room if we can
      if locations[f"{amphipod_type}0"] == "":
        cost += 2
        temp = copy.deepcopy(current_state)
        temp[amphipod_number] = f"{amphipod_type}0"             
      
        return [(temp, amphipod_cost*cost)]
      else:
        cost += 1
        temp = copy.deepcopy(current_state)
        temp[amphipod_number] = f"{amphipod_type}"           
        temp[pair_number] = f"{amphipod_type}"              
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
    "B0" : "",
    "B1" : "",
    "C0" : "",
    "C1" : "",
    "D0" : "",
    "D1" : "",
  }

  for amphipod_number in range(8):
    amphipod_type, _, _ = amphipod_info[amphipod_number]
    locations[current_state[amphipod_number]] = amphipod_type

  possible_moves = []
  for amphipod_number in range(8):
    possible_moves = possible_moves + find_moves_for(locations, current_state, amphipod_number)
  return possible_moves



G = nx.DiGraph()

#starting_position = ["A0","D0", "A1", "C1", "B1", "C0", "B0", "D1"] # Sample
starting_position = ["B1","C0", "C1", "D0", "A1", "B0", "A0", "D1"]  #Real
#starting_position = ["A0","B1", "B0", "A1", "C", "C", "D", "D"] # Simple
#starting_position = ["P1","P9","B0","D0","P3","C0","A0","D1"]

target_position = ["A","A", "B", "B", "C", "C", "D", "D"]
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
