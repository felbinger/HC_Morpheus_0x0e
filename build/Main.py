from PIL import Image
import textwrap

with open("input_binary_or_not.txt", "r") as f:
    string = f.read()

converted = []

for row in textwrap.wrap(string, 530)[0::10]:
    converted.append(row.replace("0", " ")[0::10])
    print(row.replace("0", " ")[0::10])

img = Image.new('RGB', (len(converted[0]), len(converted)), "white")
pixels = img.load()

for y in range(img.size[0]):
    for x in range(img.size[1]):
        if converted[x][y] == "1":
            pixels[y, x] = (0, 0, 0)

img.save("output_qr.png")
