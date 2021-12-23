
# """

# #############
# #ABCDEFGHIJK#
# ###L#N#P#R###
#   #M#O#Q#S#
#   #########

# """

# from typing import List


# sample_cells = {
#   "A" : "",
#   "B" : "",
#   "C" : "",
#   "D" : "",
#   "E" : "",
#   "F" : "",
#   "G" : "",
#   "H" : "",
#   "I" : "",
#   "J" : "",
#   "K" : "",
#   "L" : "B",
#   "M" : "A",
#   "N" : "C",
#   "O" : "D",
#   "P" : "B",
#   "Q" : "C",
#   "R" : "D",
#   "S" : "A",
# }

# scores = {
#   "A" : 1,
#   "B" : 10,
#   "C" : 100,
#   "D" : 1000,
# }

# rooms = {
#   "A" : ["L", "M"],
#   "B" : ["N", "O"],
#   "C" : ["P", "Q"],
#   "D" : ["R", "S"],
# }

# valid_moves = {
#   "A" : ["B"],
#   "B" : ["A", "C"],
#   "C" : ["B", "D", "L"],
#   "D" : ["C", "E"],
#   "E" : ["D", "F", "N"],
#   "F" : ["E", "G"],
#   "G" : ["F", "H", "P"],
#   "H" : ["G", "I"],
#   "I" : ["H", "J", "R"],
#   "J" : ["I", "K"],
#   "K" : ["J"],
#   "L" : ["C", "M"],
#   "M" : ["L"],
#   "N" : ["E", "O"],
#   "O" : ["N"],
#   "P" : ["G", "Q"],
#   "Q" : ["P"],
#   "R" : ["I", "S"],
#   "S" : ["R"],
# }

# def can_stop(cell: str) -> bool:
#   return cell not in ["C","E","G","I"]

# def can_enter_room(cells: dict, amphipod: str, cell: str) -> bool:
#   room = rooms[amphipod]
#   if cell not in room: return False  # Not our room
#   if cells[room[0]] not in ("", amphipod): return False #Someone in our room
#   if cells[room[1]] not in ("", amphipod): return False #Someone in our room
#   return True

# def is_win(cells: dict) -> bool:
#   return cells["L"] == "A" and cells["M"] == "A" and \
#          cells["N"] == "B" and cells["O"] == "B" and \
#          cells["P"] == "C" and cells["Q"] == "C" and \
#          cells["L"] == "R" and cells["S"] == "D"


# def find_valid_moves(cells: dict, index: str) -> List[str]:
#   amphipod = cells[index]
#   if amphipod == "": return []  #Cell is empty
#   room = rooms[amphipod]
#   if index == room[1]: return [] #At end of room
#   if index == room[0] and room[1] == amphipod: return [] #Room is full of the correct types.

#   possible_moves = []
#   for move in valid_moves[index]:
#     if cells[move] == "":   #We can only move into empty squares
#       pass


# #ABCDEFGHIJK


# cells = sample_cells

from numba import jit
from typing import List


corridor = [""] * 11
roomA = ["B", "A"]
roomB = ["C", "D"]
roomC = ["B", "C"]
roomD = ["D", "A"]

#   Label corridor  C0....C10
#   Label rooms RA0, RA1 .... RD0, RD1

sample_amphipods = {
    "A0": {
        "Type": "A",
        "Location": "RA0"
    },
    "A1": {
        "Type": "A",
        "Location": "RD0"
    },
    "B0": {
        "Type": "B",
        "Location": "RA1"
    },
    "B1": {
        "Type": "B",
        "Location": "RC1"
    },
    "C0": {
        "Type": "C",
        "Location": "RB1"
    },
    "C1": {
        "Type": "C",
        "Location": "RC0"
    },
    "D0": {
        "Type": "D",
        "Location": "RB0"
    },
    "D1": {
        "Type": "D",
        "Location": "RD1"
    }
}

real_amphipods = {
    "A0": {
        "Type": "A",
        "Location": "RB1"
    },
    "A1": {
        "Type": "A",
        "Location": "RC0"
    },
    "B0": {
        "Type": "B",
        "Location": "RC1"
    },
    "B1": {
        "Type": "B",
        "Location": "RD0"
    },
    "C0": {
        "Type": "C",
        "Location": "RA1"
    },
    "C1": {
        "Type": "C",
        "Location": "RB0"
    },
    "D0": {
        "Type": "D",
        "Location": "RA0"
    },
    "D1": {
        "Type": "D",
        "Location": "RD1"
    }
}

amphipods = real_amphipods

# amphipods = {
#     "A0": {
#         "Type": "A",
#         "Location": "RA0"
#     },
#     "A1": {
#         "Type": "A",
#         "Location": "RB1"
#     },
#     "B0": {
#         "Type": "B",
#         "Location": "RB0"
#     },
#     "B1": {
#         "Type": "B",
#         "Location": "RA1"
#     },
#     "C0": {
#         "Type": "C",
#         "Location": "RC0"
#     },
#     "C1": {
#         "Type": "C",
#         "Location": "RC1"
#     },
#     "D0": {
#         "Type": "D",
#         "Location": "RD0"
#     },
#     "D1": {
#         "Type": "D",
#         "Location": "RD1"
#     }
# }


locations_lookup = [
  ["C0"],
  ["C1"],
  ["C2"],
  ["C3"],
  ["C4"],
  ["C5"],
  ["C6"],
  ["C7"],
  ["C8"],
  ["C9"],
  ["C10"],
  ["RA0"],
  ["RA1"],
  ["RB0"],
  ["RB1"],
  ["RC0"],
  ["RC1"],
  ["RD0"],
  ["RD1"]
]

locations = {
  "C0" : "",
  "C1" : "",
  "C2" : "",
  "C3" : "",
  "C4" : "",
  "C5" : "",
  "C6" : "",
  "C7" : "",
  "C8" : "",
  "C9" : "",
  "C10" : "",
  "RA0" : "",
  "RA1" : "",
  "RB0" : "",
  "RB1" : "",
  "RC0" : "",
  "RC1" : "",
  "RD0" : "",
  "RD1" : "",
}

room_entries = {
  "A" : 2,
  "B" : 4,
  "C" : 6,
  "D" : 8,
}

costs = [1,1,10,10,100,100,1000,1000]

amphipod_locations = []
amphipod_types = []
amphipod_names = []

for amphipod_name, amphipod in amphipods.items():
  amphipod_location = amphipod["Location"]
  locations[amphipod_location] = amphipod_name
  amphipod_locations.append(amphipod_location)
  amphipod_types.append(amphipod["Type"])
  amphipod_names.append(amphipod_name)

import functools

# @functools.lru_cache(maxsize=None)
def get_valid_moves(locations, amphipod_locations, amphipod_number) -> List[str]:
  amphipod_type = amphipod_types[amphipod_number]
  amphipod_location = amphipod_locations[amphipod_number]
  in_room = amphipod_location.startswith("R")
  if in_room:
    room_type = amphipod_location[1]
    room_position = int(amphipod_location[2])
    if amphipod_type == room_type and room_position == 0:
      #print(f"Home")
      return []

    if amphipod_type == room_type and room_position == 1 and locations[f"R{amphipod_type}0"].startswith(amphipod_type):
      #print(f"Both home")
      return []
    
    if in_room and room_position == 0 and locations[f"R{amphipod_type}1"] != "":
      #print(f"Blocked in")
      return []
    
    # We are in the room,  but we can move out into the corridor
    # C0....C10   We cannot stop on 2,4,6,8
    enter_at = room_entries[room_type]

    possible_moves = []

    #Cost to exit the room
    cost = 0 if room_position == 1 else 1

    # Moving left
    i = enter_at
    while i >= 0 and locations[f"C{i}"] == "":
      cost+=1
      if i not in (2,4,6,8):
        possible_moves.append((f"C{i}", cost))
      i -= 1

    # Moving right
    cost = 0 if room_position == 1 else 1
    i = enter_at
    while i <= 10 and locations[f"C{i}"] == "":
      cost+=1
      if i not in (2,4,6,8):
        possible_moves.append((f"C{i}", cost))
      i += 1
    return possible_moves
  
  else:
    # We are in a corridor.  We can only enter our own rooms if none else
    # is in it.
    can_enter_room = (locations[f"R{amphipod_type}0"] == "" or locations[f"R{amphipod_type}0"][0] == amphipod_type) and \
                     (locations[f"R{amphipod_type}1"] == "" or locations[f"R{amphipod_type}1"][0] == amphipod_type)
    if can_enter_room:
      # And there is a path from here?
      current_position = int(amphipod_location[1:])
      enter_at = room_entries[amphipod_type]
      cost = 0
      blocked = False
      if current_position < enter_at:
        # Move right
        i = current_position + 1
        cost += 1
        while i < enter_at and not blocked:
          if locations[f"C{i}"] != "":
            blocked=True
          i += 1
          cost += 1
      else:
        # Move left
        i = current_position - 1
        cost += 1
        while i > enter_at and not blocked:
          if locations[f"C{i}"] != "":
            blocked=True
          i -= 1
          cost += 1

      if not blocked:
        if locations[f"R{amphipod_type}0"] == "":
          cost += 2
          return [(f"R{amphipod_type}0", cost)]
        else:
          cost += 1
          return [(f"R{amphipod_type}1", cost)]          
      
  return []

def game_is_won(amphipod_locations) -> bool:
  for i in range(len(amphipod_locations)):
    location = amphipod_locations[i]
    if location[0] != "R" or location[1] != amphipod_types[i]:
      return False
  return True

def play(locations, amphipod_locations):
  if game_is_won(amphipod_locations):
    # No more moves are required.
    return 0

  best_cost = 999999
  for amphipod_number in range(len(amphipod_locations)):
    possible_moves = get_valid_moves(locations, amphipod_locations, amphipod_number)
    for possible_move in possible_moves:

      # make the move
      current_location = amphipod_locations[amphipod_number]
      locations[current_location] = ""
      locations[possible_move[0]] = amphipod_names[amphipod_number]
      amphipod_locations[amphipod_number] = possible_move[0]

      cost = (possible_move[1] * costs[amphipod_number]) + play(locations, amphipod_locations)

      # undo the move
      locations[current_location] = amphipod_names[amphipod_number]
      locations[possible_move[0]] = ""
      amphipod_locations[amphipod_number] = current_location

      best_cost = min(cost, best_cost)
  return best_cost

print(play(locations, amphipod_locations))
