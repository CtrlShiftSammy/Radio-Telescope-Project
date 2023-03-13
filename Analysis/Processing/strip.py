with open("Readings/ORT/sun_slw26novS1_clean.txt", "r") as file:
    lines = file.readlines()

lines = [line.strip() for line in lines]

with open("Readings/ORT/sun_slw26novS1_clean.txt", "w") as file:
    file.write("\n".join(lines))
