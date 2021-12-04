
from typing import List, Tuple

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

def read_file() -> Tuple[List[int], List]:
  with open("Day04/data.txt") as f:
    lines = f.readlines()
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
  return calls, boards


def play(calls, boards, number_of_renaming_boards_needed):
  remainining_boards = set([b for b in range(len(boards))])
  for call in calls:
    for board_number, board in enumerate(boards):
      if board_number in remainining_boards:
        for row in board:
          for i in range(len(row)):
            if row[i] == call:
              row[i] = ""
              if is_winning_board(board):
                remainining_boards.remove(board_number)
                if len(remainining_boards) == number_of_renaming_boards_needed:
                  print(score_board(board) * call) 
                  return

calls, boards = read_file()
play(calls, boards, number_of_renaming_boards_needed = len(boards) - 1)  #6592
play(calls, boards, number_of_renaming_boards_needed = 0)    #31755