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
    val = int(input("Input value: "))
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



@dataclasses.dataclass(frozen=True)
class ParseState:
  w: str = dataclasses.field(default="0")
  x: str = dataclasses.field(default="0")
  y: str = dataclasses.field(default="0")
  z: str = dataclasses.field(default="0")
  inputNumber: int = dataclasses.field(default=1)

  def getValue(self, variableNameOrValue: str) -> str:
    if variableNameOrValue in ["w","x", "y", "z"]:
      return variableNameOrValue
    else:
      return variableNameOrValue

  def nextInput(self) -> "ParseState":
    return ParseState(self.w, self.x, self.y, self.z, self.inputNumber+1)

  def setValue(self, variableName: str,  newValue: int) -> "ParseState":
    if variableName == "w":
      return ParseState(newValue, self.x, self.y, self.z, self.inputNumber)
    elif variableName == "x":
      return ParseState(self.w, newValue, self.y, self.z, self.inputNumber)
    elif variableName == "y":
      return ParseState(self.w, self.x, newValue, self.z, self.inputNumber)
    elif variableName == "z":
      return ParseState(self.w, self.x, self.y, newValue, self.inputNumber)

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


def parse_instruction(instruction: Instruction, state: ParseState) -> ParseState:
  second = "" if instruction.operand2 is None else instruction.operand2
  i = f"{instruction.operation} {instruction.operand1} {second}"
  comment = ""

  if instruction.operation == "inp":
    state = state.setValue(instruction.operand1, f"INPUT{state.inputNumber}")
    comment = f"; {instruction.operand1} = INPUT{state.inputNumber}"
    state = state.nextInput()

  elif instruction.operation == "add":
    op1 = state.getValue(instruction.operand1)
    op2 = state.getValue(instruction.operand2)
    if op1.isdigit() and op2.isdigit():
      val = int(op1) + int(op2)
      state = state.setValue(instruction.operand1, str(val))
      comment = f"; {instruction.operand1} = {val}"
    elif op1 in ["0", 0]:
      state = state.setValue(instruction.operand1, op2)
      comment = f"; {instruction.operand1} = {op2}"      
    elif op1 == "(INPUT1+14)" and op2 == "13":      
      state = state.setValue(instruction.operand1, f"(INPUT1+27)")
      comment = f"; {instruction.operand1} = (INPUT1+27)"      
    else:      
      state = state.setValue(instruction.operand1, f"({op1}+{op2})")
      comment = f"; {instruction.operand1} = {op1}+{op2}"

  elif instruction.operation == "mul":
    op1 = state.getValue(instruction.operand1)
    op2 = state.getValue(instruction.operand2)
    if op1 in ["0", 0] or op2 in ["0", 0]:
      state = state.setValue(instruction.operand1, "0")
      comment = f"; {instruction.operand1} = 0"
    elif op2 in ["1", 1]:
      state = state.setValue(instruction.operand1, op1)
      comment = f"; {instruction.operand1} = {op1}"      
    else:
      state = state.setValue(instruction.operand1, f"({op1} * {op2})")
      comment = f"; {instruction.operand1} = {op1} * {op2}"

  elif instruction.operation == "div":
    op1 = state.getValue(instruction.operand1)
    op2 = state.getValue(instruction.operand2)
    if op2 in ["1", 1]:
      state = state.setValue(instruction.operand1, op1)
      comment = f"; {instruction.operand1} = {op1}"    
    else:      
      state = state.setValue(instruction.operand1, f"({op1} / {op2})")
      comment = f"; {instruction.operand1} = {op1} / {op2}" 

  elif instruction.operation == "mod":
    op1 = state.getValue(instruction.operand1)
    op2 = state.getValue(instruction.operand2)
    if op1 in ["0", 0]:
      state = state.setValue(instruction.operand1, "0")
      comment = f"; {instruction.operand1} = 0"
    elif op1 == "(INPUT1+14)" and op2 == "26":
      # Input1 can never be more than 9,  and 9+14 < 26
      state = state.setValue(instruction.operand1, op1)
      comment = f"; {instruction.operand1} = {op1}"
    else:      
      state = state.setValue(instruction.operand1, f"({op1} mod {op2})")
      comment = f"; {instruction.operand1} = {op1} mod {op2}"    

  elif instruction.operation == "eql":
    op1 = state.getValue(instruction.operand1)
    op2 = state.getValue(instruction.operand2)

    if op2.startswith("INPUT") and op1.isdigit() and (int(op1) > 10 or int(op1) < 1):
      state = state.setValue(instruction.operand1, "0")
      comment = f"; {instruction.operand1} = 0"
    elif op1 == "(INPUT1+27)" and op2=="INPUT2":
      #INPUT2 can not be more than 9
      state = state.setValue(instruction.operand1, "0")
      comment = f"; {instruction.operand1} = 0"      
    elif op1 == op2:
      state = state.setValue(instruction.operand1, "1")
      comment = f"; {instruction.operand1} = 1"      
    else:
      state = state.setValue(instruction.operand1, f"(1 if {op1}=={op2} else 0)")
      comment = f"; {instruction.operand1} = (1 if {op1}=={op2} else 0)"  

  else:
    print(f"Not supported {instruction.operation}")

  print(f"{i} {comment}")
  return state

import os
os.system("cls")
instructions = parse_file("day24/data.txt")
state = ParseState()
for instruction in instructions:
  state = parse_instruction(instruction, state)


# Input 1,    w=input1   x=1,  y=input1+14   z=input1+14


