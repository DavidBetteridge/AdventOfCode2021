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
    state = state.setValue(instruction.operand1, f"INPUT_{instruction.operand1.upper()}", list(range(1,10)))
    comment = f"; {instruction.operand1} = INPUT_{instruction.operand1.upper()}"
    print(f"{n}: {i} {comment}")

  elif instruction.operation == "add":
    return do_binary_operation(n, instruction, state, lambda a,b: a+b, f"({op1}+{op2})") 

  elif instruction.operation == "mul":
    return do_binary_operation(n, instruction, state, lambda a,b: a*b, f"({op1}*{op2})") 

  elif instruction.operation == "div":
    return do_binary_operation(n, instruction, state, lambda a,b: math.floor(a/b), f"math.floor({op1}/{op2})") 

  elif instruction.operation == "mod":
    return do_binary_operation(n, instruction, state, lambda a,b: a%b, f"({op1} % {op2})") 

  elif instruction.operation == "eql":
    return do_binary_operation(n, instruction, state, lambda a,b: 1 if {a}=={b} else 0, f"(1 if {op1}=={op2} else 0)") 

  else:
    print(f"Not supported {instruction.operation}")

  return state



instructions = parse_file("C:\Personal\AdventOfCode2021\day24/data.txt")
stages = split_instructions_into_stages(instructions)

# zs2=[]
# for z in range(15,24):
#   for w in range(1, 10):
#     zs2.append((z*26)+(w+8)  )

# zs3=[]
# for z in zs2:
#   for w in range(1, 10):
#     zs3.append((z*26)+(w+4)  )
# print(len(zs3))


# zs4=[]
# for z in zs3:
#   for w in range(1, 10):
#     zs4.append((z*26)+(w+10)  )
# print(len(zs4))

# state = ParseState()
# state = state.setValue("z", f"INPUT_Z", [])
# for n, i in enumerate(stages[-14]):
#   state = parse_instruction(n,i,state)


def stage14(INPUT_W,INPUT_Z):
  return ((math.floor(INPUT_Z/26)*((25*(1 if (1 if (((0+INPUT_Z) % 26)-12)==INPUT_W else 0)==0 else 0))+1))+((((((25*(1 if (1 if (((0+INPUT_Z) % 26)-12)==INPUT_W else 0)==0 else 0))+1)*0)+INPUT_W)+12)*(1 if (1 if (((0+INPUT_Z) % 26)-12)==INPUT_W else 0)==0 else 0)))

def stage13(INPUT_W,INPUT_Z):
  return ((math.floor(INPUT_Z/1)*((25*(1 if (1 if (((0+INPUT_Z) % 26)+11)==INPUT_W else 0)==0 else 0))+1))+((((((25*(1 if (1 if (((0+INPUT_Z) % 26)+11)==INPUT_W else 0)==0 else 0))+1)*0)+INPUT_W)+13)*(1 if (1 if (((0+INPUT_Z) % 26)+11)==INPUT_W else 0)==0 else 0)))

def stage12(INPUT_W,INPUT_Z):
  return ((math.floor(INPUT_Z/26)*((25*(1 if (1 if (((0+INPUT_Z) % 26)+-6)==INPUT_W else 0)==0 else 0))+1))+((((((25*(1 if (1 if (((0+INPUT_Z) % 26)+-6)==INPUT_W else 0)==0 else 0))+1)*0)+INPUT_W)+9)*(1 if (1 if (((0+INPUT_Z) % 26)+-6)==INPUT_W else 0)==0 else 0)))

def stage11(INPUT_W,INPUT_Z):
  return ((math.floor(INPUT_Z/1)*((25*(1 if (1 if (((0+INPUT_Z) % 26)+14)==INPUT_W else 0)==0 else 0))+1))+((((((25*(1 if (1 if (((0+INPUT_Z) % 26)+14)==INPUT_W else 0)==0 else 0))+1)*0)+INPUT_W)+0)*(1 if (1 if (((0+INPUT_Z) % 26)+14)==INPUT_W else 0)==0 else 0)))

def stage10(INPUT_W,INPUT_Z):
  return ((math.floor(INPUT_Z/26)*((25*(1 if (1 if (((0+INPUT_Z) % 26)+-12)==INPUT_W else 0)==0 else 0))+1))+((((((25*(1 if (1 if (((0+INPUT_Z) % 26)+-12)==INPUT_W else 0)==0 else 0))+1)*0)+INPUT_W)+6)*(1 if (1 if (((0+INPUT_Z) % 26)+-12)==INPUT_W else 0)==0 else 0)))

def stage9(INPUT_W,INPUT_Z):
  return ((math.floor(INPUT_Z/26)*((25*(1 if (1 if (((0+INPUT_Z) % 26)+-3)==INPUT_W else 0)==0 else 0))+1))+((((((25*(1 if (1 if (((0+INPUT_Z) % 26)+-3)==INPUT_W else 0)==0 else 0))+1)*0)+INPUT_W)+1)*(1 if (1 if (((0+INPUT_Z) % 26)+-3)==INPUT_W else 0)==0 else 0)))

def stage8(INPUT_W,INPUT_Z):
  return ((math.floor(INPUT_Z/26)*((25*(1 if (1 if (((0+INPUT_Z) % 26)+-8)==INPUT_W else 0)==0 else 0))+1))+((((((25*(1 if (1 if (((0+INPUT_Z) % 26)+-8)==INPUT_W else 0)==0 else 0))+1)*0)+INPUT_W)+14)*(1 if (1 if (((0+INPUT_Z) % 26)+-8)==INPUT_W else 0)==0 else 0)))

def stage7(INPUT_W,INPUT_Z):
  return  ((math.floor(INPUT_Z/1)*((25*(1 if (1 if (((0+INPUT_Z) % 26)+12)==INPUT_W else 0)==0 else 0))+1))+((((((25*(1 if (1 if (((0+INPUT_Z) % 26)+12)==INPUT_W else 0)==0 else 0))+1)*0)+INPUT_W)+4)*(1 if (1 if (((0+INPUT_Z) % 26)+12)==INPUT_W else 0)==0 else 0)))

def stage6(INPUT_W,INPUT_Z):
  return ((math.floor(INPUT_Z/26)*((25*(1 if (1 if (((0+INPUT_Z) % 26)+-4)==INPUT_W else 0)==0 else 0))+1))+((((((25*(1 if (1 if (((0+INPUT_Z) % 26)+-4)==INPUT_W else 0)==0 else 0))+1)*0)+INPUT_W)+10)*(1 if (1 if (((0+INPUT_Z) % 26)+-4)==INPUT_W else 0)==0 else 0)))

def stage5(INPUT_W,INPUT_Z):
  return ((math.floor(INPUT_Z/26)*((25*(1 if (1 if (((0+INPUT_Z) % 26)+-3)==INPUT_W else 0)==0 else 0))+1))+((((((25*(1 if (1 if (((0+INPUT_Z) % 26)+-3)==INPUT_W else 0)==0 else 0))+1)*0)+INPUT_W)+14)*(1 if (1 if (((0+INPUT_Z) % 26)+-3)==INPUT_W else 0)==0 else 0)))

def stage4(INPUT_W,INPUT_Z):
  return ((math.floor(INPUT_Z/1)*((25*(1 if (1 if (((0+INPUT_Z) % 26)+10)==INPUT_W else 0)==0 else 0))+1))+((((((25*(1 if (1 if (((0+INPUT_Z) % 26)+10)==INPUT_W else 0)==0 else 0))+1)*0)+INPUT_W)+10)*(1 if (1 if (((0+INPUT_Z) % 26)+10)==INPUT_W else 0)==0 else 0)))

def stage3(INPUT_W,INPUT_Z):
  return ((math.floor(INPUT_Z/1)*((25*(1 if (1 if (((0+INPUT_Z) % 26)+11)==INPUT_W else 0)==0 else 0))+1))+((((((25*(1 if (1 if (((0+INPUT_Z) % 26)+11)==INPUT_W else 0)==0 else 0))+1)*0)+INPUT_W)+4)*(1 if (1 if (((0+INPUT_Z) % 26)+11)==INPUT_W else 0)==0 else 0)))

def stage2(INPUT_W,INPUT_Z):
  return ((math.floor(INPUT_Z/1)*((25*(1 if (1 if (((0+INPUT_Z) % 26)+13)==INPUT_W else 0)==0 else 0))+1))+((((((25*(1 if (1 if (((0+INPUT_Z) % 26)+13)==INPUT_W else 0)==0 else 0))+1)*0)+INPUT_W)+8)*(1 if (1 if (((0+INPUT_Z) % 26)+13)==INPUT_W else 0)==0 else 0)))

def stage1(INPUT_W,INPUT_Z):
  return ((math.floor(INPUT_Z/1)*((25*(1 if (1 if (((0+INPUT_Z) % 26)+11)==INPUT_W else 0)==0 else 0))+1))+((((((25*(1 if (1 if (((0+INPUT_Z) % 26)+11)==INPUT_W else 0)==0 else 0))+1)*0)+INPUT_W)+14)*(1 if (1 if (((0+INPUT_Z) % 26)+11)==INPUT_W else 0)==0 else 0)))

def solve_stage(target: List[int], stage_fn):
  return ([
    (z,w,t) 
    for z in range(0, 1000000)
    for w in range(1, 10)
    if (t:=stage_fn(w,z)) in (target)
  ])


sol = solve_stage([0], stage14)
zs = set([z for z,_,_ in sol])
print(zs)

sol = solve_stage(zs, stage13)
zs = set([z for z,_,_ in sol])
print(zs)

sol = solve_stage(zs, stage12)
zs = set([z for z,_,_ in sol])
print(zs)

sol = solve_stage(zs, stage11)
zs = set([z for z,_,_ in sol])
print(zs)

sol = solve_stage(zs, stage10)
zs = set([z for z,_,_ in sol])
print(zs)

sol = solve_stage(zs, stage9)
zs = set([z for z,_,_ in sol])
print(zs)

sol = solve_stage(zs, stage8)
zs = set([z for z,_,_ in sol])
print(zs)

sol = solve_stage(zs, stage7)
zs = set([z for z,_,_ in sol])
print(zs)

sol = solve_stage(zs, stage6)
zs = set([z for z,_,_ in sol])
print(zs)

sol = solve_stage(zs, stage5)
zs = set([z for z,_,_ in sol])
print(zs)

sol = solve_stage(zs, stage4)
zs = set([z for z,_,_ in sol])
print(zs)

sol = solve_stage(zs, stage3)
zs = set([z for z,_,_ in sol])
print(sol)

sol = solve_stage(zs, stage2)
zs = set([z for z,_,_ in sol])
print(sol)

sol = solve_stage(zs, stage1)
zs = set([z for z,_,_ in sol])
print(sol)
