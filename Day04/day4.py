import pandas as pd
import numpy as np
from typing import List, Tuple

def is_winning_board(board: pd.DataFrame):
  # Completed Row
  if 0 in board.sum(axis=1).values:
    return True

  # Completed Column
  if 0 in board.sum(axis=0).values:
    return True

  return False

def score_board(board):
  return board.sum(numeric_only=True).sum()

def read_file() -> Tuple[List[int], List[pd.DataFrame]]:
  with open("Day04/data.txt") as f:
    lines = f.readlines()
    calls = list(map(int, lines[0].split(",")))

    line_number = 2
    boards = []

    while line_number < len(lines):
      current_board = pd.DataFrame(columns =['0', '1', '2', '3', '4'])
      for _ in range(5):
        row = [int(lines[line_number][i:i+2]) for i in range(0, len(lines[line_number]), 3)]
        current_board.loc[len(current_board)] = row
        line_number +=1
      boards.append(current_board)

      line_number += 1
  return calls, boards


def play(calls, boards, number_of_remaining_boards_needed):
  remaining_boards = set([b for b in range(len(boards))])
  dictionary = {c : c for c in calls }

  for call in calls:
    for board_number, board in enumerate(boards):
      if board_number in remaining_boards:
        dictionary[call] = np.nan
        board = board.applymap(dictionary.get) 
        if is_winning_board(board):
          remaining_boards.remove(board_number)
          if len(remaining_boards) == number_of_remaining_boards_needed:
            print(score_board(board) * call) 
            return

calls, boards = read_file()
play(calls, boards, number_of_remaining_boards_needed = len(boards) - 1)  #6592
play(calls, boards, number_of_remaining_boards_needed = 0)    #31755