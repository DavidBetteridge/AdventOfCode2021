import dataclasses
import functools
import math
import numba
import numpy as np
from functools import lru_cache
from typing import List, Optional, Tuple

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

@numba.jit
def get_state(state: np.array, op) -> int:
  if op == "w": return state[0]
  if op == "x": return state[1]
  if op == "y": return state[2]
  return state[3]

@numba.jit
def set_state(state: np.array, op, val) -> np.array:
  if op == "w": state[0] = val
  if op == "x": state[1] = val
  if op == "y": state[2] = val
  if op == "z": state[3] = val
  return state

# @numba.jit
def execute_instruction(operation: str, operand1, operand2, state: np.array, w: int) -> np.array:
  op1 = None if operand1 is None else get_state(state, operand1) if not operand1.isdigit() else int(operand1)
  op2 = None if operand2 is None else get_state(state, operand2) if not operand2.isdigit() else int(operand2)

  if operation == "inp":
    return set_state(state, operand1, w)
  elif operation == "add":
    result = op1 + op2
    return set_state(state, operand1, result)
  elif operation == "mul":
    result = op1 * op2
    return set_state(state, operand1, result)
  elif operation == "div":
    result = math.floor(op1 / op2)
    return set_state(state, operand1, result)
  elif operation == "mod":
    result = op1 % op2
    return set_state(state, operand1, result)
  elif operation == "eql":
    if op1 == op2:
      return set_state(state, operand1, 1)
    else:
      return set_state(state, operand1, 0)
  else:
    print(f"Not supported {operation}")


def split_instructions_into_stages(source: List[Instruction]) -> List[List[Instruction]]:
  results = []
  current = []
  index = 0
  while index < len(source):
    if source[index].operation == "inp":
      if len(current) > 0: results.append(current)
      current = []
    current.append(source[index])
    index += 1
  results.append(current)
  return results


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
      #print(f"{n}: {i} {comment}")
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
      #print(f"{n}: {i} {comment}")
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
      #print(f"{n}: {i} {comment}")
      return state    

    state = state.setValue(instruction.operand1, expr, list(possible))
    comment = f"; {instruction.operand1} = {expr}"
  else:
    # Too many values
    state = state.setValue(instruction.operand1, expr, [])
    comment = f"; {instruction.operand1} = {expr}"    

  #print(f"{n}: {i} {comment}")
  return state

def parse_instruction(n: int, instruction: Instruction, state: ParseState) -> ParseState:
  second = "" if instruction.operand2 is None else instruction.operand2
  i = f"{instruction.operation} {instruction.operand1} {second}"
  comment = ""
  op1 = state.getValue(instruction.operand1)
  op2 = state.getValue(instruction.operand2)  

  if instruction.operation == "inp":
    comment = "; Skipped"
    # state = state.setValue(instruction.operand1, f"INPUT{state.inputNumber}", list(range(1,10)))
    # comment = f"; {instruction.operand1} = INPUT{state.inputNumber}"
    # state = state.nextInput()

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

  #print(f"{n}: {i} {comment}")
  return state



# def brute_force_stage(stage: List[Instruction], target: List[int]) -> List[Tuple[int,int,int]]:
#   results = []
#   for w in range (1, 10):
#     for z in range (0,10000):
#       # w,x,y,z
#       state = np.empty([0,0,0,z], np.longlong)
#       for instruction in stage:
#         state = execute_instruction(instruction.operation, instruction.operand1, instruction.operand2, state, w)
#       if state[3] in target:
#         results.append((z, w, state.z))
#   return results        

@lru_cache(maxsize=None)
def ev(w,z,i) -> int:
  return eval(i)

# import os
# os.system("cls")
# instructions = parse_file("day24/data.txt")
# stages = split_instructions_into_stages(instructions)


# zs = [0]
# for n, stage in enumerate(stages[::-1]):
#   r = brute_force_stage(stage, zs)
#   zs = set([z for z,w,t in r])
#   print(r)


# instru=[]
# instru.append(lambda w,z: (((z/ 1)*((25*(1 if (1 if ((z % 26)+11)==w else 0)==0 else 0))+1))+((((((25*(1 if (1 if ((z % 26)+11)==w else 0)==0 else 0))+1)*0)+w)+14)*(1 if (1 if ((z % 26)+11)==w else 0)==0 else 0))))
# instru.append(lambda w,z: (((z/ 1)*((25*(1 if (1 if ((z % 26)+13)==w else 0)==0 else 0))+1))+((((((25*(1 if (1 if ((z % 26)+13)==w else 0)==0 else 0))+1)*0)+w)+8)*(1 if (1 if ((z % 26)+13)==w else 0)==0 else 0))))
# instru.append(lambda w,z: (((z/ 1)*((25*(1 if (1 if ((z % 26)+11)==w else 0)==0 else 0))+1))+((((((25*(1 if (1 if ((z % 26)+11)==w else 0)==0 else 0))+1)*0)+w)+4)*(1 if (1 if ((z % 26)+11)==w else 0)==0 else 0))))
# instru.append(lambda w,z: (((z/ 1)*((25*(1 if (1 if ((z % 26)+10)==w else 0)==0 else 0))+1))+((((((25*(1 if (1 if ((z % 26)+10)==w else 0)==0 else 0))+1)*0)+w)+10)*(1 if (1 if ((z % 26)+10)==w else 0)==0 else 0))))
# instru.append(lambda w,z: (((z/26)*((25*(1 if (1 if ((z % 26)+-3)==w else 0)==0 else 0))+1))+((((((25*(1 if (1 if ((z % 26)+-3)==w else 0)==0 else 0))+1)*0)+w)+14)*(1 if (1 if ((z % 26)+-3)==w else 0)==0 else 0))))
# instru.append(lambda w,z: (((z/26)*((25*(1 if (1 if ((z % 26)+-4)==w else 0)==0 else 0))+1))+((((((25*(1 if (1 if ((z % 26)+-4)==w else 0)==0 else 0))+1)*0)+w)+10)*(1 if (1 if ((z % 26)+-4)==w else 0)==0 else 0))))
# instru.append(lambda w,z: (((z/ 1)*((25*(1 if (1 if ((z % 26)+12)==w else 0)==0 else 0))+1))+((((((25*(1 if (1 if ((z % 26)+12)==w else 0)==0 else 0))+1)*0)+w)+4)*(1 if (1 if ((z % 26)+12)==w else 0)==0 else 0))))
# instru.append(lambda w,z: (((z/26)*((25*(1 if (1 if ((z % 26)+-8)==w else 0)==0 else 0))+1))+((((((25*(1 if (1 if ((z % 26)+-8)==w else 0)==0 else 0))+1)*0)+w)+14)*(1 if (1 if ((z % 26)+-8)==w else 0)==0 else 0))))
# instru.append(lambda w,z: (((z/26)*((25*(1 if (1 if ((z % 26)+-3)==w else 0)==0 else 0))+1))+((((((25*(1 if (1 if ((z % 26)+-3)==w else 0)==0 else 0))+1)*0)+w)+1)*(1 if (1 if ((z % 26)+-3)==w else 0)==0 else 0))))
# instru.append(lambda w,z: (((z/26)*((25*(1 if (1 if ((z % 26)+-12)==w else 0)==0 else 0))+1))+((((((25*(1 if (1 if ((z % 26)+-12)==w else 0)==0 else 0))+1)*0)+w)+6)*(1 if (1 if ((z % 26)+-12)==w else 0)==0 else 0))))
# instru.append(lambda w,z: (((z/ 1)*((25*(1 if (1 if ((z % 26)+14)==w else 0)==0 else 0))+1))+((((((25*(1 if (1 if ((z % 26)+14)==w else 0)==0 else 0))+1)*0)+w)+0)*(1 if (1 if ((z % 26)+14)==w else 0)==0 else 0))))
# instru.append(lambda w,z: (((z/26)*((25*(1 if (1 if ((z % 26)+-6)==w else 0)==0 else 0))+1))+((((((25*(1 if (1 if ((z % 26)+-6)==w else 0)==0 else 0))+1)*0)+w)+9)*(1 if (1 if ((z % 26)+-6)==w else 0)==0 else 0))))
# instru.append(lambda w,z: (((z/ 1)*((25*(1 if (1 if ((z % 26)+11)==w else 0)==0 else 0))+1))+((((((25*(1 if (1 if ((z % 26)+11)==w else 0)==0 else 0))+1)*0)+w)+13)*(1 if (1 if ((z % 26)+11)==w else 0)==0 else 0))))
# instru.append(lambda w,z: (((z/26)*((25*(1 if (1 if ((z % 26)+-12)==w else 0)==0 else 0))+1))+((((((25*(1 if (1 if ((z % 26)+-12)==w else 0)==0 else 0))+1)*0)+w)+12)*(1 if (1 if ((z % 26)+-12)==w else 0)==0 else 0))))


# zs=set([0])
# for i, stage in enumerate(stages):
#   new_zs = set()
#   for w in range(1,10):
#     for z in zs:
#       e = instru[i](w,z)
#       new_zs.add(e)
#   zs = new_zs
#   print(len(zs))


  # ps = ParseState()
  # ps = ps.setValue("w", f"w", list(range(1,10)))
  # ps = ps.setValue("x", f"x", [0])
  # ps = ps.setValue("y", f"y", [0])
  # ps = ps.setValue("z", f"z", zs)
  # for n, instruction in enumerate(stage):
  #   ps = parse_instruction(n+1, instruction, ps)
  # final = ps.z
  # print(f"instru.append(lambda w,z: {final})")

  #     # state = np.array([0,0,0,z], np.longlong)
  #     # for instruction in stage:
  #     #   execute_instruction(instruction.operation, instruction.operand1, instruction.operand2, state, w)

  #     e = ev(w,z,final)      
  #     # f = state[3]
  #     # assert e==f

@numba.jit
def solve():
  instru=[
      (1,11,14),
      (1,13,8),
      ( 1, 11,4),
      ( 1, 10,10),
      (26, -3,14),
      (26, -4,10),
      ( 1, 12,4),
      (26, -8,14),
      (26, -3,1),
      (26,-12,+6),
      ( 1, 14,0),
      (26, -6,9),
      ( 1, 11,13),
      (26,-12,+12)    
  ]

  # instru.append(lambda w,z: (((z/ a)*((25*(1 if (1 if ((z % 26)+ b)==w else 0)==0 else 0))+1))+((((((25*(1 if (1 if ((z % 26)+b)==w else 0)==0 else 0))+1)*0)+w)+c)*(1 if (1 if ((z % 26)+b)==w else 0)==0 else 0))))
  # instru.append(lambda w,z: (((z/ a)*((25*(1 if (1 if ((z % 26)+ b)==w else 0)==0 else 0))+1))+((((((25*(1 if (1 if ((z % 26)+b)==w else 0)==0 else 0))+1)*0)+w)+c)*(1 if (1 if ((z % 26)+b)==w else 0)==0 else 0))))
 

  zs=set([0])
  stage=0
  while stage<14:
    new_zs = set()
    for w in range(1,10):
      for z in zs:
        a,b,c = instru[stage]
        e=(((z/ a)*((25*(1 if (1 if ((z % 26)+ b)==w else 0)==0 else 0))+1))+((((((25*(1 if (1 if ((z % 26)+b)==w else 0)==0 else 0))+1)*0)+w)+c)*(1 if (1 if ((z % 26)+b)==w else 0)==0 else 0)))
        new_zs.add(e)
    stage +=1
    zs = new_zs
    print(len(zs))

  return 0

solve()