import math

class BinaryPipe:

  __lookup = {
    "0" : "0000",
    "1" : "0001",
    "2" : "0010",
    "3" : "0011",
    "4" : "0100",
    "5" : "0101",
    "6" : "0110",
    "7" : "0111",
    "8" : "1000",
    "9" : "1001",
    "A" : "1010",
    "B" : "1011",
    "C" : "1100",
    "D" : "1101",
    "E" : "1110",
    "F" : "1111",
  }

  def __init__(self, hex_string: str):
    self.__binary = "".join( [self.__lookup[h] for h in hex_string] )
    self.__offset = 0

  def read(self, number_of_bits: int) -> int:
    value = self.__binary[self.__offset:self.__offset+number_of_bits]
    self.__offset += number_of_bits
    return int(value,2)
  
  def current_offset(self) -> int:
    return self.__offset


def read_file(filename: str) -> str:
  with open(filename) as f:
    return f.readline().strip()


def package_length(binary : BinaryPipe, part1: bool) -> int:
  version = binary.read(3)
  packet_type = binary.read(3)
  if packet_type == 4:
    # Literal packet
    done = False
    literal_value = 0
    while not done:
      done = binary.read(1) == 0
      group = binary.read(4)
      literal_value = (literal_value << 4) + group
    if part1:
      return version
    else:
      return literal_value
  else:
    # Operator Packet
    length_type = binary.read(1)
    subpacket_values = []
    if length_type == 0:
      packet_length = binary.read(15)
      end_of_subpackets = binary.current_offset() + packet_length
      while binary.current_offset() < end_of_subpackets:
        subpacket_values.append(package_length(binary, part1))
    else:
      number_of_subpackets = binary.read(11)
      for _ in range(number_of_subpackets):
        subpacket_values.append(package_length(binary, part1))
    
    if part1:
      return version + sum(subpacket_values)

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

    return result


hex = read_file("Day16/data.txt")

pipe = BinaryPipe(hex)
part1 = package_length(pipe, True)
print(part1)
assert part1 == 893

pipe = BinaryPipe(hex)
part2 = package_length(pipe, False)
print(part2)
assert part2 == 4358595186090
