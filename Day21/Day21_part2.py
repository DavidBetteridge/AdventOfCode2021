from typing import Tuple
from numba import jit
import numpy as np

player1 = 4#6
player2 = 8#9

cache = np.empty((524287,2), int)

@jit
def mod_add(current, add, mod):
  return (((current + add) -1) % mod) + 1

@jit
def f(player1_position: int, player2_position: int, player1_score: int, player2_score: int, player1_to_play: bool, cache: np.array) -> Tuple[int, int]:
  wins_for_player1 = 0
  wins_for_player2 = 0

  key = (player1_position << 15) + (player1_score << 10) + (player2_position << 6) + (player2_score << 1) + (1 if player1_to_play else 0)
  if cache[key][0] != 0 or cache[key][1] != 0:
    return cache[key][0], cache[key][1]

  if player1_to_play:
    for turn in [3,4,5,4,5,6,5,6,7,4,5,6,5,6,7,6,7,8,5,6,7,6,7,8,7,8,9]:
      new_position = mod_add(player1_position, turn, 10)
      new_score = new_position + player1_score
      if new_score >= 21: 
        wins_for_player1+=1
      else:
        p1, p2 = f(new_position, player2_position, new_score, player2_score, False, cache)
        wins_for_player1+=p1
        wins_for_player2+=p2
  else:
    for turn in [3,4,5,4,5,6,5,6,7,4,5,6,5,6,7,6,7,8,5,6,7,6,7,8,7,8,9]:
      new_position = mod_add(player2_position, turn, 10)
      new_score = new_position + player2_score
      if new_score >= 21: 
        wins_for_player2+=1
      else:
        p1, p2 = f(player1_position, new_position, player1_score, new_score, True, cache)            
        wins_for_player1+=p1
        wins_for_player2+=p2
            
  cache[key][0] = wins_for_player1
  cache[key][1] = wins_for_player2
  return wins_for_player1, wins_for_player2


#print(f(1, 1, 16, 20, True, cache))
print(f(player1, player2, 0, 0, True, cache))

# 444356092776315
# 211721548553058
# 5448578290973
# 46039336396241697