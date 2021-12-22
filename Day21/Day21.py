player1 = 6
player2 = 9
player1_score = 0
player2_score = 0
next_dice = 1
rolls = 0

def mod_add(current, add, mod):
  return (((current + add) -1) % mod) + 1

while player1_score < 1000 and player2_score < 1000:

  turn = 0
  for _ in range(3):
    turn += next_dice
    next_dice = mod_add(next_dice, 1, 100)
    rolls += 1
  player1 = mod_add(player1, turn, 10)
  player1_score += player1

  if player1_score < 1000:
    turn = 0
    for _ in range(3):
      turn += next_dice
      next_dice = mod_add(next_dice, 1, 100)
      rolls += 1
    player2 = mod_add(player2, turn, 10)
    player2_score += player2

loser = player2_score if player2_score < player1_score else player1_score
print(loser * rolls)