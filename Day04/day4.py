
from typing import List, Tuple

def is_winning_board(board):
  # Completed Row
  if any(sum(row) == 0 for row in board):
    return True

  # Completed Column
  if any(sum([board[r][c] for r in range(5)]) == 0 for c in range(5)):
    return True

  return False

def score_board(board):
  return sum([column 
              for row in board
              for column in row])

def read_file() -> Tuple[List[int], List]:
  with open("Day04/data.txt") as f:
    lines = f.readlines()
    calls = list(map(int, lines[0].split(",")))

    line_number = 2
    boards = []

    while line_number < len(lines):
      current_board = []
      for _ in range(5):
        row = [int(lines[line_number][i:i+2]) for i in range(0, len(lines[line_number]), 3)]
        current_board.append(row)
        line_number +=1
      boards.append(current_board)

      line_number += 1
  return calls, boards


def play(calls, boards, number_of_remaining_boards_needed):
  remaining_boards = set([b for b in range(len(boards))])
  for call in calls:
    for board_number, board in enumerate(boards):
      if board_number in remaining_boards:

        updated_board = [[cell if cell != call else 0 for cell in row]
                          for row in board]
        boards[board_number] = updated_board

        if is_winning_board(updated_board):
          remaining_boards.remove(board_number)
          if len(remaining_boards) == number_of_remaining_boards_needed:
            print(score_board(board) * call) 
            return

calls, boards = read_file()
play(calls, boards, number_of_remaining_boards_needed = len(boards) - 1)  #6592
play(calls, boards, number_of_remaining_boards_needed = 0)    #31755