# from typing import List

# sample_amphipods = {
#     "A0": {
#         "Type": "A",
#         "Location": "A0"
#     },
#     "A1": {
#         "Type": "A",
#         "Location": "D0"
#     },
#     "B0": {
#         "Type": "B",
#         "Location": "A1"
#     },
#     "B1": {
#         "Type": "B",
#         "Location": "C1"
#     },
#     "C0": {
#         "Type": "C",
#         "Location": "B1"
#     },
#     "C1": {
#         "Type": "C",
#         "Location": "C0"
#     },
#     "D0": {
#         "Type": "D",
#         "Location": "B0"
#     },
#     "D1": {
#         "Type": "D",
#         "Location": "D1"
#     }
# }

# real_amphipods = {
#     "A0": {
#         "Type": "A",
#         "Location": "B1"
#     },
#     "A1": {
#         "Type": "A",
#         "Location": "C0"
#     },
#     "B0": {
#         "Type": "B",
#         "Location": "C1"
#     },
#     "B1": {
#         "Type": "B",
#         "Location": "D0"
#     },
#     "C0": {
#         "Type": "C",
#         "Location": "A1"
#     },
#     "C1": {
#         "Type": "C",
#         "Location": "B0"
#     },
#     "D0": {
#         "Type": "D",
#         "Location": "A0"
#     },
#     "D1": {
#         "Type": "D",
#         "Location": "D1"
#     }
# }

# amphipods = real_amphipods

# amphipods = {
#     "A0": {
#         "Type": "A",
#         "Location": "A0"
#     },
#     "A1": {
#         "Type": "A",
#         "Location": "B1"
#     },
#     "B0": {
#         "Type": "B",
#         "Location": "B0"
#     },
#     "B1": {
#         "Type": "B",
#         "Location": "A1"
#     },
#     "C0": {
#         "Type": "C",
#         "Location": "C0"
#     },
#     "C1": {
#         "Type": "C",
#         "Location": "C1"
#     },
#     "D0": {
#         "Type": "D",
#         "Location": "D0"
#     },
#     "D1": {
#         "Type": "D",
#         "Location": "D1"
#     }
# }


# locations_lookup = [
#   ["C0"],
#   ["C1"],
#   ["C2"],
#   ["C3"],
#   ["C4"],
#   ["C5"],
#   ["C6"],
#   ["C7"],
#   ["C8"],
#   ["C9"],
#   ["C10"],
#   ["A0"],
#   ["A1"],
#   ["B0"],
#   ["B1"],
#   ["C0"],
#   ["C1"],
#   ["D0"],
#   ["D1"]
# ]

# locations = {
#   "C0" : "",
#   "C1" : "",
#   "C2" : "",
#   "C3" : "",
#   "C4" : "",
#   "C5" : "",
#   "C6" : "",
#   "C7" : "",
#   "C8" : "",
#   "C9" : "",
#   "C10" : "",
#   "A0" : "",
#   "A1" : "",
#   "B0" : "",
#   "B1" : "",
#   "C0" : "",
#   "C1" : "",
#   "D0" : "",
#   "D1" : "",
# }

# room_entries = {
#   "A" : 2,
#   "B" : 4,
#   "C" : 6,
#   "D" : 8,
# }

# costs = [1,1,10,10,100,100,1000,1000]

# amphipod_locations = []
# amphipod_types = []
# amphipod_names = []

# for amphipod_name, amphipod in amphipods.items():
#   amphipod_location = amphipod["Location"]
#   locations[amphipod_location] = amphipod_name
#   amphipod_locations.append(amphipod_location)
#   amphipod_types.append(amphipod["Type"])
#   amphipod_names.append(amphipod_name)

# import functools

# # @functools.lru_cache(maxsize=None)
# def get_valid_moves(locations, amphipod_locations, amphipod_number) -> List[str]:
#   amphipod_type = amphipod_types[amphipod_number]
#   amphipod_location = amphipod_locations[amphipod_number]
#   in_room = not amphipod_location.startswith("C")
#   if in_room:
#     room_type = amphipod_location[0]
#     room_position = int(amphipod_location[1])
#     if amphipod_type == room_type and room_position == 0:
#       #print(f"Home")
#       return []

#     if amphipod_type == room_type and room_position == 1 and locations[f"{amphipod_type}0"].startswith(amphipod_type):
#       #print(f"Both home")
#       return []
    
#     if in_room and room_position == 0 and locations[f"{amphipod_type}1"] != "":
#       #print(f"Blocked in")
#       return []
    
#     # We are in the room,  but we can move out into the corridor
#     # C0....C10   We cannot stop on 2,4,6,8
#     enter_at = room_entries[room_type]

#     possible_moves = []

#     #Cost to exit the room
#     cost = 0 if room_position == 1 else 1

#     # Moving left
#     i = enter_at
#     while i >= 0 and locations[f"C{i}"] == "":
#       cost+=1
#       if i not in (2,4,6,8):
#         possible_moves.append((f"C{i}", cost))
#       i -= 1

#     # Moving right
#     cost = 0 if room_position == 1 else 1
#     i = enter_at
#     while i <= 10 and locations[f"C{i}"] == "":
#       cost+=1
#       if i not in (2,4,6,8):
#         possible_moves.append((f"C{i}", cost))
#       i += 1
#     return possible_moves
  
#   else:
#     # We are in a corridor.  We can only enter our own rooms if none else
#     # is in it.
#     can_enter_room = (locations[f"{amphipod_type}0"] == "" or locations[f"{amphipod_type}0"][0] == amphipod_type) and \
#                      (locations[f"{amphipod_type}1"] == "")
#     if can_enter_room:
#       # And there is a path from here?
#       current_position = int(amphipod_location[1:])
#       enter_at = room_entries[amphipod_type]
#       cost = 0
#       blocked = False
#       if current_position < enter_at:
#         # Move right
#         i = current_position + 1
#         cost += 1
#         while i < enter_at and not blocked:
#           if locations[f"C{i}"] != "":
#             blocked=True
#           i += 1
#           cost += 1
#       else:
#         # Move left
#         i = current_position - 1
#         cost += 1
#         while i > enter_at and not blocked:
#           if locations[f"C{i}"] != "":
#             blocked=True
#           i -= 1
#           cost += 1

#       if not blocked:
#         if locations[f"{amphipod_type}0"] == "":
#           cost += 2
#           return [(f"{amphipod_type}0", cost)]
#         else:
#           cost += 1
#           return [(f"{amphipod_type}1", cost)]          
      
#   return []

# def game_is_won(amphipod_locations) -> bool:
#   for i in range(len(amphipod_locations)):
#     location = amphipod_locations[i]
#     if location[0] != amphipod_types[i]:
#       return False
#   return True

# def play(locations, amphipod_locations):
#   if game_is_won(amphipod_locations):
#     # No more moves are required.
#     return 0

#   best_cost = 999999
#   for amphipod_number in range(len(amphipod_locations)):
#     possible_moves = get_valid_moves(locations, amphipod_locations, amphipod_number)
#     for possible_move in possible_moves:

#       # make the move
#       current_location = amphipod_locations[amphipod_number]
#       locations[current_location] = ""
#       locations[possible_move[0]] = amphipod_names[amphipod_number]
#       amphipod_locations[amphipod_number] = possible_move[0]

#       cost = (possible_move[1] * costs[amphipod_number]) + play(locations, amphipod_locations)

#       # undo the move
#       locations[current_location] = amphipod_names[amphipod_number]
#       locations[possible_move[0]] = ""
#       amphipod_locations[amphipod_number] = current_location

#       best_cost = min(cost, best_cost)
#   return best_cost

# print(play(locations, amphipod_locations))


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

    if amphipod_type == room_type and room_position == 1 \
       and current_state[pair_number] == f"{amphipod_type}0":
      #print(f"Both home")
      return []
    
    if in_room and room_position == 0 and locations[f"{amphipod_type}1"] != "":
      #print(f"Blocked in")
      return []

    # We are in the room,  but we can move out into the corridor
    # C0....C10   We cannot stop on 2,4,6,8
    enter_at = room_entries[room_type]

    #Cost to exit the room
    cost = 1 if room_position == 1 else 2

    # Moving left
    i = enter_at
    while i >= 0 and locations[f"P{i}"] == "":
      if i not in (2,4,6,8):
        temp = copy.deepcopy(current_state)
        temp[amphipod_number] = f"P{i}"
        possible_moves.append((temp, amphipod_cost*cost))
      cost+=1
      i -= 1

    # Moving right
    cost = 1 if room_position == 1 else 2
    i = enter_at
    while i <= 10 and locations[f"P{i}"] == "":
      if i not in (2,4,6,8):
        temp = copy.deepcopy(current_state)
        temp[amphipod_number] = f"P{i}"        
        possible_moves.append((temp, amphipod_cost*cost))
      cost+=1
      i += 1

  if in_room:
    current_position = enter_at  # Where do we enter the corridor
    basecost = 1 if room_position == 1 else 2 # Cost of leaving the room
  else:
    current_position = int(current_location[1:])
    basecost = 0

  # We are in a corridor.  We can only enter our own rooms if none else
  # is in it.
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
      while i < enter_at and not blocked:
        if locations[f"P{i}"] != "":
          blocked=True
        i += 1
        cost += 1
    else:
      # Move left
      i = current_position - 1
      cost += 1
      while i > enter_at and not blocked:
        if locations[f"P{i}"] != "":
          blocked=True
        i -= 1
        cost += 1

    if not blocked:
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



G = nx.Graph()

starting_position = ["A0","D0", "A1", "C1", "B1", "C0", "B0", "D1"]
starting_position = ["B1","C0", "C1", "D0", "A1", "B0", "A0", "D1"]
# starting_position = ["A0","B1", "B0", "A1", "C", "C", "D", "D"]
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
      # print(f"{next_position}=>{following_state}")
      G.add_edge(next_position, following_state, weight = possible_move[1])
      if not following_state in processed:
        todo.append(following_state)

print(G)
total, route = (nx.single_source_dijkstra(G,
          source="-".join(starting_position),
          target="-".join(target_position),
          weight='weight'))

print(total)  #15360 to high


