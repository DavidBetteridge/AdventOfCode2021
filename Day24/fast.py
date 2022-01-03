from typing import List
import numba

@numba.jit(nopython=True)
def solve():
  instru_a: List[int]=[
       1,
       1,
       1,
       1,
      26,
      26,
       1,
      26,
      26,
      26,
       1,
      26,
       1,
      26,
  ]

  instru_b: List[int]=[
      11,
      13,
      11,
      10,
      -3,
      -4,
      12,
      -8,
      -3,
      -12,
      14,
      -6,
      11,
      12
  ]

  instru_c: List[int]=[
      14,
      8,
      4,
      10,
      14,
      10,
      4,
      14,
      1,
      6,
      0,
      9,
      13,
      12    
  ]  


  zs: List[int] = [0]
  stage=0
  while stage<14:
    new_zs: List[int] = [i for i in range(0)]
    a = instru_a[stage]
    b = instru_b[stage]
    c = instru_c[stage]
    for z in zs:
       d=((z % 26)+ b)
       for w in range(1,10):
         m=1 if d!=w else 0
         e=int(((z/ a)*((25*m)+1))+((w+c)*m))
         new_zs.append(e)
    stage +=1
    zs = new_zs
    print(len(zs))

  return 0

solve()