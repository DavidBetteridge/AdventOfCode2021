
import math
from typing import List, Optional

class TokenType:
  OPEN = "OPEN"
  CLOSE = "CLOSE"
  COMMA = "COMMA"

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

      # We only increase the depth if we contain exactly two children
      # ie.  [1,2] or [1,[1,2]] etc is fine
      # but [[1,2]] isn't as [1,2] is only child
      

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


def find_pair_to_split(tokens: List) -> Optional[int]:
  # Returns the index of the number
  ind = 0
  while ind < len(tokens):
    if tokens[ind].isdigit() and int(tokens[ind]) > 9:
      return ind
    else:
      ind += 1
  return None

def split_pair(tokens : List, ind_of_pair: int) -> List:
  number = int(tokens[ind_of_pair])
  lhs = math.floor(number / 2.0)
  rhs = math.ceil(number / 2.0)
  new_tokens = [ TokenType.OPEN, str(lhs), TokenType.COMMA, str(rhs), TokenType.CLOSE] 
  return tokens[:ind_of_pair] + new_tokens + tokens[ind_of_pair+1:]


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
  return tokens[:ind_of_start_of_pair] + ["0"] + tokens[ind_of_start_of_pair+5:]

  
def add_tokens(lhs_tokens: List[str], rhs_tokens: List[str]) -> List[str]:
  return [ TokenType.OPEN ] + lhs_tokens + [TokenType.COMMA] + rhs_tokens + [ TokenType.CLOSE ]




lhs = tokenise("[1,2]")
rhs = tokenise("[[3,4],5]")
added = add_tokens(lhs, rhs)
assert tokens_to_string(added) == "[[1,2],[[3,4],5]]"


input = tokenise("[[[[0,7],4],[15,[0,13]]],[1,1]]")
split = split_pair(input, find_pair_to_split(input))
assert tokens_to_string(split) == "[[[[0,7],4],[[7,8],[0,13]]],[1,1]]"

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
print(tokens_to_string(explode))
assert tokens_to_string(explode) == "[[3,[2,[8,0]]],[9,[5,[7,0]]]]"