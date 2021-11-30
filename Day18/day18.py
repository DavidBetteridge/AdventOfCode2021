
import math
from typing import List, Optional

class TokenType:
  OPEN = "OPEN"
  CLOSE = "CLOSE"
  COMMA = "COMMA"

def read_file(filename: str) -> List[str]:
  with open(filename) as f:
    lines = f.readlines()
    return [line.strip() for line in lines]

def tokenise(input: str) -> List:
  tokens = []
  ind = 0
  while ind < len(input):
    if input[ind] == "[":
      tokens.append(TokenType.OPEN)
      ind += 1
    elif input[ind] == "]":
      tokens.append(TokenType.CLOSE)
      ind += 1
    elif input[ind] == ",":
      tokens.append(TokenType.COMMA)
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
    if token == TokenType.OPEN:
      result += "["
    elif token == TokenType.CLOSE:
      result += "]"      
    elif token == TokenType.COMMA:
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

def find_pair_to_explode(tokens: List[str]) -> Optional[int]:
  # Returns the index of the opening bracket
  ind = 0
  depth = 0
  while ind < len(tokens):
    if tokens[ind] == TokenType.OPEN:
      depth+=1
      if depth > 4:
        # We are too deep so we need to explode the first left most pair.
        # However,  we can only explode a pair if it contains two regular numbers.
        # So  [1,2] is ok,  but [1, [2,3]] is not.
        if tokens[ind+1].isdigit() and tokens[ind+3].isdigit():
          return ind

      ind+=1
    elif tokens[ind] == TokenType.CLOSE:
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
  # ..... number_to_left ..... ind_of_start_of_pair:[ lhsTokenType.commarhs ] ... number_to_right ....
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


def reduce(tokens : List[str]) -> List[str]:
  while True:
    if (pair_to_explode := find_pair_to_explode(tokens)) is not None:
      tokens = explode_pair(tokens, pair_to_explode)

    elif (pair_to_split := find_pair_to_split(tokens)) is not None:
      tokens = split_pair(tokens, pair_to_split)

    else:
      return tokens


def calculate_magnitude(tokens : List[str]) -> int:
  # Keep replacing any [ x, y ] with a number
  ind = 0
  while len(tokens) > 1:
    if tokens[ind] == TokenType.OPEN and \
       tokens[ind+1].isdigit() and \
       tokens[ind+2] == TokenType.COMMA and \
       tokens[ind+3].isdigit() and \
       tokens[ind+4] == TokenType.CLOSE:
       magnitude = (3 * int(tokens[ind+1])) + (2 * int(tokens[ind+3])) 
       tokens = tokens[:ind] + [str(magnitude)] + tokens[ind+5:]
       ind = 0
    else:
      ind += 1
  return int(tokens[0])

assert calculate_magnitude(tokenise("[9,1]")) == 29
assert calculate_magnitude(tokenise("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]")) == 3488

lhs = tokenise("[[[[4,3],4],4],[7,[[8,4],9]]]")
rhs = tokenise("[1,1]")
added = add_tokens(lhs, rhs)
output = reduce(added)
assert tokens_to_string(output) == "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"

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

numbers = read_file("Day18/data.txt")
tokenised = [tokenise(number) for number in numbers]

total = tokenised[0]
for i in range(1, len(numbers)):
  rhs = tokenised[i]
  total = add_tokens(total, rhs)
  total = reduce(total)
print(tokens_to_string(total))
print(calculate_magnitude(total))   #4140   3675


# Part 2
best = 0
for lhs in tokenised:
  for rhs in tokenised:
    total = calculate_magnitude(reduce(add_tokens(lhs, rhs)))
    best = max(best, total)
print(best)    # 3993 4650