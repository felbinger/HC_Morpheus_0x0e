from PIL import Image

img = Image.open("raw_qr_input.jpg")
pixels = img.load()

string = ""

for y in range(img.size[0]):
    for x in range(img.size[1]):
        string += str(pixels[y, x])

with open("input_binary_or_not.txt", "w") as f:
    f.write(string)
