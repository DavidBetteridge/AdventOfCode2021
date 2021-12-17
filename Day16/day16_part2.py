import math

def read_file(filename: str) -> str:
  with open(filename) as f:
    return f.readline().strip()



def package_length(binary, start_from=0) -> int:
  a=start_from
  if binary[start_from:].replace("0", "") == "":
    return None, len(binary) 

  # Decode packet
  version = int(binary[start_from:start_from+3],2)
  start_from+=3
  print(f"version={version}")

  packet_type = int(binary[start_from:start_from+3],2)
  start_from+=3
  is_literal = packet_type == 4
  print(f"packet_type={packet_type}")

  if is_literal:
    done = False
    literal_value = ""
    while not done:
      group = binary[start_from:start_from+5]
      done = binary[start_from] == "0"
      start_from += 5
      literal_value += group[1:]
    print("literal_value", int(literal_value,2))
    return int(literal_value,2), start_from
  else:
    # Operator
    length_type = int(binary[start_from],2)
    start_from+=1
    subpacket_values = []
    if length_type == 0:
      packet_length = int(binary[start_from:start_from+15],2)
      start_from+=15
      print("packet_length="+str(packet_length))
      while start_from < len(binary):
        subpackage_value, start_from = package_length(binary, start_from)   
        if subpackage_value is not None:
          subpacket_values.append(subpackage_value)
    else:
      number_of_subpackets = int(binary[start_from:start_from+11],2)
      start_from+=11
      print("number_of_subpackets="+str(number_of_subpackets))

      for sp in range(number_of_subpackets):
        subpackage_value, start_from = package_length(binary, start_from)   
        if subpackage_value is not None:
          subpacket_values.append(subpackage_value)
    
    if packet_type == 0:
      result = sum(subpacket_values)

    if packet_type == 1:
      result = math.prod(subpacket_values)

    if packet_type == 2:
      result = min(subpacket_values)

    if packet_type == 3:
      result = max(subpacket_values)

    if packet_type == 5:
      result = 1 if subpacket_values[0] > subpacket_values[1] else 0

    if packet_type == 6:
      result = 1 if subpacket_values[0] < subpacket_values[1] else 0

    if packet_type == 7:
      result = 1 if subpacket_values[0] == subpacket_values[1] else 0

    return result, start_from


hex = read_file("Day16/data.txt")
binary = "".join( [bin(int(h, 16))[2:].zfill(4) for h in hex] )
print(hex)
print(binary)
print(package_length(binary))  #893

  
