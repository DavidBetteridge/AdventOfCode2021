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
  w: str = dataclasses.field(default=0)
  x: str = dataclasses.field(default=0)
  y: str = dataclasses.field(default=0)
  z: str = dataclasses.field(default=0)
  possible_w: List[int] = dataclasses.field(default_factory= lambda : [0] )
  possible_x: List[int] = dataclasses.field(default_factory= lambda : [0] )
  possible_y: List[int] = dataclasses.field(default_factory= lambda : [0] )
  possible_z: List[int] = dataclasses.field(default_factory= lambda : [0] )


  def setValue(self, variableName: str,
               newValue: str,
               possible_values: List[int]) -> "ParseState":
    if variableName == "w":
      return ParseState(newValue, self.x, self.y, self.z, possible_values, self.possible_x, self.possible_y, self.possible_z)
    elif variableName == "x":
      return ParseState(self.w, newValue, self.y, self.z, self.possible_w, possible_values, self.possible_y, self.possible_z)
    elif variableName == "y":
      return ParseState(self.w, self.x, newValue, self.z, self.possible_w, self.possible_x, possible_values, self.possible_z)
    elif variableName == "z":
      return ParseState(self.w, self.x, self.y, newValue, self.possible_w, self.possible_x, self.possible_y, possible_values)

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



def do_binary_operation(instruction: Instruction, state: ParseState, fn, expr: str) -> ParseState:
  second = "" if instruction.operand2 is None else instruction.operand2
  i = f"{instruction.operation} {instruction.operand1} {second}"
  
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
      return state

    # Is the result always the first argument?
    always_first = True
    for a in op1v:
      for b in op2v:
        if fn(a, b) != a:
          always_first = False
    if always_first:          
      state = state.setValue(instruction.operand1, op1, list(possible))
      return state

    # Is the result always the second argument?
    always_second = True
    for a in op1v:
      for b in op2v:
        if fn(a, b) != b:
          always_second = False
    if always_second:          
      state = state.setValue(instruction.operand1, op2, list(possible))
      return state    

    state = state.setValue(instruction.operand1, expr, list(possible))
  else:
    # Too many values
    state = state.setValue(instruction.operand1, expr, [])

  return state

def parse_instruction(instruction: Instruction, state: ParseState) -> ParseState:
  second = "" if instruction.operand2 is None else instruction.operand2
  i = f"{instruction.operation} {instruction.operand1} {second}"
  op1 = state.getValue(instruction.operand1)
  op2 = state.getValue(instruction.operand2)  

  if instruction.operation == "inp":
    state = state.setValue(instruction.operand1, f"INPUT_{instruction.operand1.upper()}", list(range(1,10)))

  elif instruction.operation == "add":
    return do_binary_operation(instruction, state, lambda a,b: a+b, f"({op1}+{op2})") 

  elif instruction.operation == "mul":
    return do_binary_operation(instruction, state, lambda a,b: a*b, f"({op1}*{op2})") 

  elif instruction.operation == "div":
    return do_binary_operation(instruction, state, lambda a,b: math.floor(a/b), f"math.floor({op1}/{op2})") 

  elif instruction.operation == "mod":
    return do_binary_operation(instruction, state, lambda a,b: a%b, f"({op1} % {op2})") 

  elif instruction.operation == "eql":
    return do_binary_operation(instruction, state, lambda a,b: 1 if {a}=={b} else 0, f"(1 if {op1}=={op2} else 0)") 

  else:
    print(f"Not supported {instruction.operation}")

  return state



instructions = parse_file("C:\Personal\AdventOfCode2021\day24/data.txt")
stages = split_instructions_into_stages(instructions)
lambdas = {}


for stage_number in range(len(stages)):
  state = ParseState()
  state = state.setValue("z", f"INPUT_Z", [])
  for i in stages[stage_number]:
    state = parse_instruction(i,state)
  fn = state.z
  exec("lambdas[stage_number+1] = lambda INPUT_W,INPUT_Z : " + fn)

def solve_stage(target: List[int], stage_fn):
  return ([
    (z,w,t) 
    for z in range(0, 1000000)
    for w in range(1, 10)
    if (t:=stage_fn(w,z)) in (target)
  ])

solutions = {}

zs = [0]
for stage_number in range(len(stages),0,-1):
  sol = solve_stage(zs, lambdas[stage_number])
  zs = set([z for z,_,_ in sol])
  solutions[stage_number]=sol


answer=""
sol = solutions[1]
best_w = max(w for _,w,t in sol)
next_z = [t for _,w,t in sol if w==best_w][0]
answer+=str(best_w)

for s in range(2,15):
  sol = solutions[s]
  best_w = max(w for z,w,t in sol if z==next_z)
  next_z = [t for z,w,t in sol if w==best_w and z==next_z][0]
  answer+=str(best_w)
print(answer)     #74929995999389


answer=""
sol = solutions[1]
best_w = min(w for _,w,t in sol)
next_z = [t for _,w,t in sol if w==best_w][0]
answer+=str(best_w)   

for s in range(2,15):
  sol = solutions[s]
  best_w = min(w for z,w,t in sol if z==next_z)
  next_z = [t for z,w,t in sol if w==best_w and z==next_z][0]
  answer+=str(best_w)
print(answer)         #11118151637112