
from typing import List

def is_winning_board(board):
  for row in board:
    if all([c == "" for c in row]):
      return True

  for c in range(5):
    column = [board[r][c] for r in range(5)]
    if all([r == "" for r in column]):
      return True

  return False

def score_board(board):
  return sum([column 
              for row in board
              for column in row
              if column != ""])

def read_file() -> List[str]:
  with open("Day04/data.txt") as f:
    return f.readlines()

lines = read_file()
calls = list(map(int, lines[0].split(",")))

line_number = 2
boards = []

while line_number < len(lines):
  current_board = []
  for _ in range(5):
    row = [
      int(lines[line_number][:2]),
      int(lines[line_number][2:5]),
      int(lines[line_number][5:8]),
      int(lines[line_number][8:11]),
      int(lines[line_number][11:14]),
    ]
    current_board.append(row)
    line_number +=1
  boards.append(current_board)

  line_number += 1


for call in calls:
  for board in boards:
    for row in board:
      for i in range(len(row)):
        if row[i] == call:
          row[i] = ""
          if is_winning_board(board):
            print(board)
            print(score_board(board) * call)  #11312
            print(score_board(board))
