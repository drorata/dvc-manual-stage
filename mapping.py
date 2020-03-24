import json

with open("mapping.json", "r") as f:
    mapping = json.load(f)

with open("raw_data.txt", "r") as f:
    raw_line = f.readline()

mapped_line_list = [mapping[word.strip()] for word in raw_line.split(" ")]

new_line = " ".join(mapped_line_list)
print(new_line)

with open("mapped_line.txt", "w") as f:
    f.write(new_line)
