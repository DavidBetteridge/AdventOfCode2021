import dataclasses
import math
from typing import List, Optional

@dataclasses.dataclass(frozen=True)
class Instruction:
  operation: str
  operand1: str
  operand2: Optional[str]

@dataclasses.dataclass(frozen=True)
class State:
  w: int = dataclasses.field(default=0)
  x: int = dataclasses.field(default=0)
  y: int = dataclasses.field(default=0)
  z: int = dataclasses.field(default=0)

  def setValue(self, variableName: str,  newValue: int) -> "State":
    if variableName == "w":
      return State(newValue, self.x, self.y, self.z)
    elif variableName == "x":
      return State(self.w, newValue, self.y, self.z)
    elif variableName == "y":
      return State(self.w, self.x, newValue, self.z)
    elif variableName == "z":
      return State(self.w, self.x, self.y, newValue)

  def getValue(self, variableNameOrValue: str) -> int:
    if variableNameOrValue == "w":
      return self.w
    elif variableNameOrValue == "x":
      return self.x
    elif variableNameOrValue == "y":
      return self.y
    elif variableNameOrValue == "z":
      return self.z
    else:
      return int(variableNameOrValue)

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


def execute_instruction(instruction: Instruction, state: State) -> State:
  if instruction.operation == "inp":
    val = int(input(f"Input value {instruction.operand1}: "))
    return state.setValue(instruction.operand1, val)
  elif instruction.operation == "add":
    result = state.getValue(instruction.operand1) + state.getValue(instruction.operand2)
    return state.setValue(instruction.operand1, result)    
  elif instruction.operation == "mul":
    result = state.getValue(instruction.operand1) * state.getValue(instruction.operand2)
    return state.setValue(instruction.operand1, result)
  elif instruction.operation == "div":
    result = math.floor(state.getValue(instruction.operand1) / state.getValue(instruction.operand2))
    return state.setValue(instruction.operand1, result)
  elif instruction.operation == "mod":
    result = state.getValue(instruction.operand1) % state.getValue(instruction.operand2)
    return state.setValue(instruction.operand1, result)    
  elif instruction.operation == "eql":
    if state.getValue(instruction.operand1) == state.getValue(instruction.operand2):
      return state.setValue(instruction.operand1, 1)
    else:
      return state.setValue(instruction.operand1, 0)
  else:
    print(f"Not supported {instruction.operation}")



import os
os.system("cls")
instructions = parse_file("day24/data2.txt")

state = State()
for n, instruction in enumerate(instructions):
  state = execute_instruction(instruction, state)
print(state)    



