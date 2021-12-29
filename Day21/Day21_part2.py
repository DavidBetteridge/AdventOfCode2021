from typing import Tuple
from numba import jit
import numpy as np

player1 = 6
player2 = 9

cache = np.empty((524287,2), np.double)

@jit
def play(player_position: int,
         other_player_position: int,
         player_score: int,
         other_player_score: int,
         cache: np.array) -> Tuple[int, int]:

  key = (player_position << 15) + (player_score << 10) + (other_player_position << 6) + other_player_score
  if cache[key][0] != 0 or cache[key][1] != 0:
    return cache[key][0], cache[key][1]

  wins_for_player = 0
  wins_for_other_player = 0

  for turn in [3,4,5,4,5,6,5,6,7,4,5,6,5,6,7,6,7,8,5,6,7,6,7,8,7,8,9]:
    new_position = (((player_position + turn) -1) % 10) + 1
    new_score = new_position + player_score
    if new_score >= 21: 
      wins_for_player+=1
    else:
      p1, p2 = play(other_player_position, new_position, other_player_score, new_score, cache)
      wins_for_player+=p2
      wins_for_other_player+=p1

  cache[key][0] = wins_for_player
  cache[key][1] = wins_for_other_player

  return wins_for_player, wins_for_other_player

print(play(player1, player2, 0, 0, cache))
