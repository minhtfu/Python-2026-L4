color_list = ["red", "blue", "green"]
color_pick = input("What is your favourite color? ")

index = -1
for i, color in enumerate(color_list):
    if color_pick.lower() == color:
        index = i
        break

if index >= 0:
    print(f"Your colod is at index {index} in my list")
else:
    print("Sorry, I could not find your color")
