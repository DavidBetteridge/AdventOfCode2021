
from typing import List, Optional

input = "[[[[[9,8],1],2],3],4]"

def tokenise(input: str) -> List:
  tokens = []
  ind = 0
  while ind < len(input):
    if input[ind] == "[":
      tokens.append("OPEN")
      ind += 1
    elif input[ind] == "]":
      tokens.append("CLOSE")
      ind += 1
    elif input[ind] == ",":
      tokens.append("COMMA")
      ind += 1
    else:
      value = ""  
      while ind < len(input) and input[ind].isdigit():
        value += input[ind]
        ind+=1
      tokens.append(value)
  return tokens


def tokens_to_string(tokens: List) -> str:
  result = ""
  for token in tokens:
    if token == "OPEN":
      result += "["
    elif token == "CLOSE":
      result += "]"      
    elif token == "COMMA":
      result += ","
    else:
      result += token
  return result


def find_previous_token_of_type(tokens: List[str], token_type, start_from):
  ind = start_from
  while ind >= 0:
    if tokens[ind] == token_type or (token_type == "NUMBER" and tokens[ind].isdigit()):
      return ind
    else:
      ind -= 1
  return None

def find_next_token_of_type(tokens: List[str], token_type, start_from):
  ind = start_from
  while ind < len(tokens):
    if tokens[ind] == token_type or (token_type == "NUMBER" and tokens[ind].isdigit()):
      return ind
    else:
      ind += 1
  return None

def find_pair_to_explode(tokens: List) -> Optional[int]:
  # Returns the index of the opening bracket
  ind = 0
  depth = 0
  while ind < len(tokens):
    if tokens[ind] == "OPEN":
      depth+=1
      
      if depth >= 4:
        # We are too deep so we need to explode the first left most pair.
        # However,  we can only explode a pair if it contains two regular numbers.
        # So  [1,2] is ok,  but [1, [2,3]] is not.
        # ie is there a [ before our closing ]
        next_open = find_next_token_of_type(tokens, "OPEN", ind+1)
        next_close = find_next_token_of_type(tokens, "CLOSE", ind+1)
        if next_open is None or next_close < next_open:
          return ind

      ind+=1
    elif tokens[ind] == "CLOSE":
      depth-=1
      ind+=1
    else:
      ind+=1
  return None


def explode_pair(tokens : List, ind_of_start_of_pair: int) -> List:
  # We ..... number_to_left ..... ind_of_start_of_pair:[ lhs comma rhs ] ... number_to_right ....
  lhs = int(tokens[ind_of_start_of_pair + 1])
  rhs = int(tokens[ind_of_start_of_pair + 3])
  index_of_number_to_left = find_previous_token_of_type(tokens, "NUMBER", ind_of_start_of_pair - 1)
  if index_of_number_to_left is not None:
    tokens[index_of_number_to_left] = str(int(tokens[index_of_number_to_left]) + lhs)

  index_of_number_to_right = find_next_token_of_type(tokens, "NUMBER", ind_of_start_of_pair + 4)
  if index_of_number_to_right is not None:
    tokens[index_of_number_to_right] = str(int(tokens[index_of_number_to_right]) + rhs)

  # Now we have to replace this pair with a 0
  tokens = tokens[:ind_of_start_of_pair] + ["0"] + tokens[ind_of_start_of_pair+5:]

  return tokens


input = tokenise("[[[[[9,8],1],2],3],4]")
explode = explode_pair(input, find_pair_to_explode(input))
assert tokens_to_string(explode) == "[[[[0,9],2],3],4]"

input = tokenise("[7,[6,[5,[4,[3,2]]]]]")
explode = explode_pair(input, find_pair_to_explode(input))
assert tokens_to_string(explode) == "[7,[6,[5,[7,0]]]]"

input = tokenise("[[6,[5,[4,[3,2]]]],1]")
explode = explode_pair(input, find_pair_to_explode(input))
assert tokens_to_string(explode) == "[[6,[5,[7,0]]],3]"

input = tokenise("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]")
explode = explode_pair(input, find_pair_to_explode(input))
assert tokens_to_string(explode) == "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]"

input = tokenise("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]")
explode = explode_pair(input, find_pair_to_explode(input))
assert tokens_to_string(explode) == "[[3,[2,[8,0]]],[9,[5,[7,0]]]]"