from typing import Counter


def parse_file():
  with open("data.txt") as f:
    lines = f.readlines()
    image_enhancement_algorithm = lines[0].strip()
    image = ['......'+l.strip()+'......' for l in lines[2:]]
    top_and_bottom = "." * len(image[0])
    return image_enhancement_algorithm, ([top_and_bottom]*6) + image + ([top_and_bottom]*6)

image_enhancement_algorithm, image = parse_file()

for _ in range(2):
  new_image = []
  for row in range(1, len(image) - 2):
    new_row = ""
    for column in range(1, len(image[0]) - 2):
      input = image[row-1][column-1] + image[row-1][column] + image[row-1][column+1] +  \
              image[row][column-1] + image[row][column] + image[row][column+1] + \
              image[row+1][column-1] + image[row+1][column] + image[row+1][column+1]
      input = input.replace(".", "0").replace("#", "1")
      key = int(input, 2)
      output = image_enhancement_algorithm[key]
      new_row += output
    new_image.append(new_row)
  image = new_image

for i in image:
  print(i)


c = Counter("".join([i for i in image]))
print(c["#"])
