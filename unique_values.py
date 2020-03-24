import json

with open("raw_data.txt", "r") as f:
    line = f.readline()

res = {word.strip(): "XXX" for word in line.split(" ")}

with open("unique_values.json", "w") as f:
    json.dump(res, f)
