Stage 0
  Takes only W as input
  Result: Z is W + 14  (ie.  15 to 23)


Stage 1
  Takes W and Z as input
  Z is between 15 and 23
  Result: ((INPUT_Z*26)+(INPUT_W+8))
  This is 9 * 9 = 81 possible values


Stage 2
  Takes W and Z as input
  Z is one of 81 values
  Result: ((INPUT_Z*26)+(INPUT_W+4))
  This is 81 * 9 = 729 possible values


Stage 3
  Takes W and Z as input
  Z is one of 729 values
  Result: ((INPUT_Z*26)+(INPUT_W+10))
  This is 729 * 9 = 6561 possible values


Stage 4
  Takes W and Z as input
  Z is one of 6561 values
  Result: 
          let c = (1 if (1 if ((INPUT_Z % 26)+-3)==INPUT_W else 0)==0 else 0)
          (
            ((INPUT_Z/26) * ((25*c)+1))
 
            +

            ((INPUT_W+14) * c)
          )




General 1-3:
  Z = (INPUT_Z*a)+(INPUT_W+b)

  for z in range(15,24):
    for w in range(8,25):
      print (z*26)+(w+8)


Stage14
[(-21, 9), (-20, 8), (-19, 7), (-18, 6), (-17, 5), (-16, 4), (-14, 2)]      