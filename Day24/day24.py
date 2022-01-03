import dataclasses
import math
from typing import List, Optional

@dataclasses.dataclass(frozen=True)
class Instruction:
  operation: str
  operand1: str
  operand2: Optional[str]

def parse_line(line: str) -> Instruction:
  parts = line.split(" ")
  if len(parts) == 2:
    return Instruction(parts[0], parts[1], None)
  else:
    return Instruction(parts[0], parts[1], parts[2])


def parse_file(filename: str) -> List[Instruction]:
  with open(filename) as f:
    lines = f.readlines()
    return [parse_line(l.strip()) for l in lines]


@dataclasses.dataclass(frozen=True)
class ParseState:
  w: str = dataclasses.field(default="0")
  x: str = dataclasses.field(default="0")
  y: str = dataclasses.field(default="0")
  z: str = dataclasses.field(default="0")
  inputNumber: int = dataclasses.field(default=1)
  possible_w: List[int] = dataclasses.field(default_factory= lambda : [0] )
  possible_x: List[int] = dataclasses.field(default_factory= lambda : [0] )
  possible_y: List[int] = dataclasses.field(default_factory= lambda : [0] )
  possible_z: List[int] = dataclasses.field(default_factory= lambda : [0] )

  def getValue(self, variableNameOrValue: str) -> str:
    if variableNameOrValue in ["w","x", "y", "z"]:
      return variableNameOrValue
    else:
      return variableNameOrValue

  def nextInput(self) -> "ParseState":
    return ParseState(self.w, self.x, self.y, self.z, self.inputNumber+1, self.possible_w, self.possible_x, self.possible_y, self.possible_z)

  def setValue(self, variableName: str,
               newValue: str,
               possible_values: List[int]) -> "ParseState":
    if variableName == "w":
      return ParseState(newValue, self.x, self.y, self.z, self.inputNumber, possible_values, self.possible_x, self.possible_y, self.possible_z)
    elif variableName == "x":
      return ParseState(self.w, newValue, self.y, self.z, self.inputNumber, self.possible_w, possible_values, self.possible_y, self.possible_z)
    elif variableName == "y":
      return ParseState(self.w, self.x, newValue, self.z, self.inputNumber, self.possible_w, self.possible_x, possible_values, self.possible_z)
    elif variableName == "z":
      return ParseState(self.w, self.x, self.y, newValue, self.inputNumber, self.possible_w, self.possible_x, self.possible_y, possible_values)

  def getValue(self, variableNameOrValue: str) -> str:
    if variableNameOrValue == "w":
      return self.w
    elif variableNameOrValue == "x":
      return self.x
    elif variableNameOrValue == "y":
      return self.y
    elif variableNameOrValue == "z":
      return self.z
    else:
      return variableNameOrValue


  def getPossibleValues(self, variableNameOrValue: str) -> List[int]:
    if variableNameOrValue == "w":
      return self.possible_w
    elif variableNameOrValue == "x":
      return self.possible_x
    elif variableNameOrValue == "y":
      return self.possible_y
    elif variableNameOrValue == "z":
      return self.possible_z
    else:
      return [int(variableNameOrValue)]


def do_binary_operation(n: int, instruction: Instruction, state: ParseState, fn, expr: str) -> ParseState:
  second = "" if instruction.operand2 is None else instruction.operand2
  i = f"{instruction.operation} {instruction.operand1} {second}"
  comment = ""  
  
  op1v = state.getPossibleValues(instruction.operand1)
  op2v = state.getPossibleValues(instruction.operand2)
  op1 = state.getValue(instruction.operand1)  
  op2 = state.getValue(instruction.operand2)  

  # Is there only one possible value?
  if len(op1v) > 0 and len(op2v) > 0:
    possible = set()
    for a in op1v:
      for b in op2v:
        possible.add(fn(a, b))

    if len(possible) == 1:
      only_value = next(iter(possible))
      state = state.setValue(instruction.operand1, only_value, [only_value])
      comment = f"; {instruction.operand1} = {only_value}"
      print(f"{n}: {i} {comment}")
      return state

    # Is the result always the first argument?
    always_first = True
    for a in op1v:
      for b in op2v:
        if fn(a, b) != a:
          always_first = False
    if always_first:          
      state = state.setValue(instruction.operand1, op1, list(possible))
      comment = f"; {instruction.operand1} = {op1}" 
      print(f"{n}: {i} {comment}")
      return state

    # Is the result always the second argument?
    always_second = True
    for a in op1v:
      for b in op2v:
        if fn(a, b) != b:
          always_second = False
    if always_second:          
      state = state.setValue(instruction.operand1, op2, list(possible))
      comment = f"; {instruction.operand1} = {op2}" 
      print(f"{n}: {i} {comment}")
      return state    

    state = state.setValue(instruction.operand1, expr, list(possible))
    comment = f"; {instruction.operand1} = {expr}"
  else:
    # Too many values
    state = state.setValue(instruction.operand1, expr, [])
    comment = f"; {instruction.operand1} = {expr}"    

  print(f"{n}: {i} {comment}")
  return state

def parse_instruction(n: int, instruction: Instruction, state: ParseState) -> ParseState:
  second = "" if instruction.operand2 is None else instruction.operand2
  i = f"{instruction.operation} {instruction.operand1} {second}"
  comment = ""
  op1 = state.getValue(instruction.operand1)
  op2 = state.getValue(instruction.operand2)  

  if instruction.operation == "inp":
    state = state.setValue(instruction.operand1, f"INPUT{state.inputNumber}", list(range(1,10)))
    comment = f"; {instruction.operand1} = INPUT{state.inputNumber}"
    state = state.nextInput()

  elif instruction.operation == "add":
    return do_binary_operation(n, instruction, state, lambda a,b: a+b, f"({op1}+{op2})") 

  elif instruction.operation == "mul":
    return do_binary_operation(n, instruction, state, lambda a,b: a*b, f"({op1}*{op2})") 

  elif instruction.operation == "div":
    return do_binary_operation(n, instruction, state, lambda a,b: math.floor(a/b), f"({op1}/{op2})") 

  elif instruction.operation == "mod":
    return do_binary_operation(n, instruction, state, lambda a,b: a%b, f"({op1} % {op2})") 

  elif instruction.operation == "eql":
    return do_binary_operation(n, instruction, state, lambda a,b: 1 if {a}=={b} else 0, f"(1 if {op1}=={op2} else 0)") 

  else:
    print(f"Not supported {instruction.operation}")

  print(f"{n}: {i} {comment}")
  return state

import os
os.system("cls")
instructions = parse_file("day24/data2.txt")
state = ParseState()

# state = state.setValue("w", f"INPUT1", list(range(1,10)))
# state = state.setValue("x", f"INPUT2", [])
# state = state.setValue("y", f"INPUT3", [])
# state = state.setValue("z", f"INPUT4", [])

for n, instruction in enumerate(instructions):
  state = parse_instruction(n+1, instruction, state)

print("")
print("")
print(state.z)

# Input 1,    w=input1   x=1,  y=input1+14   z=input1+14

# # w 1..9
# # x 0..1
# # y 0 and 13..21
# # z lots 14390875

# # -12

# (Z % 26) - 12 == W

# Z % 26 = 12

# Z = (n 26) + 12


# INPUT2=12
# INPUT3=12
# for INPUT1 in range (-1000,1000):
#   for INPUT4 in range (1, 10):
#     # a = (((INPUT4/26)*((25*(1 if (1 if ((INPUT4 % 26)+-12)==INPUT1 else 0)==0 else 0))+1))+\
#     #   ((INPUT1+12)*(1 if (1 if ((INPUT4 % 26)+-12)==INPUT1 else 0)==0 else 0)))
#     a = (((INPUT4/26)*((((INPUT3*0)+25)*(1 if (1 if (((INPUT2*0)+INPUT4)+-12)==INPUT1 else 0)==0 else 0))+1))+((((((((INPUT3*0)+25)*(1 if (1 if (((INPUT2*0)+INPUT4)+-12)==INPUT1 else 0)==0 else 0))+1)*0)+INPUT1)+12)*(1 if (1 if (((INPUT2*0)+INPUT4)+-12)==INPUT1 else 0)==0 else 0)))
#     if a == 0:
#       print(INPUT1, INPUT4)

