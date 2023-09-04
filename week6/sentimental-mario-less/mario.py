from cs50 import get_int

# Get height from user
while True:
    height = get_int("Height: ")
    if height > 0 and height < 9:
        break

# Print pyramid
for row in range(1, height + 1):
    print(" " * (height - row) + "#" * row)