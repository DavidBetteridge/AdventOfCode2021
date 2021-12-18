
def add_to_right_most_number(current_string: str, value_to_add: int) -> str:
  ind = len(current_string) - 1
  while ind >= 0:
    if current_string[ind].isdigit():
      end_of_number = ind
      left_value = ""
      while ind>=0 and current_string[ind].isdigit():
        left_value = current_string[ind] + left_value
        ind -= 1
      value = str(int(left_value) + value_to_add)
      return current_string[:ind+1] + value + current_string[end_of_number+1:]
    ind -= 1
  return current_string      

input = "[[[[[9,8],1],2],3],4]"

ind = 0
depth = 0
output = ""
while ind < len(input):
  if input[ind] == "[":
    depth += 1
    ind += 1
    if depth >= 4:
      # We are too deep so we need to explode the first left most pair.
      # However,  we can only explode a pair if it contains two regular numbers.
      # So  [1,2] is ok,  but [1, [2,3]] is not.
      # ie is there a [ before our closing ]
      next_open = input.find("[", ind)
      next_close = input.index("]", ind)
      if next_close < next_open or next_open == -1:
        # We are good to go.
        lhs = input[ind:input.index(",", ind)]
        rhs = input[input.index(",", ind)+1:input.index("]", ind)]
        print(lhs)
        print(rhs)
        output = add_to_right_most_number(output, int(lhs))
        output += "0"
        depth -= 1
        ind = input.index("]", ind) + 1
      else:
        # This isn't a regular pair
        output += "["  
    else:
      output += "["

  elif input[ind] == "]":
    depth -= 1    
    ind += 1
    output += "]"
  else:
    output += input[ind]
    ind += 1


print(output)