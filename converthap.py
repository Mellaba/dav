import json

with open('gunfire.json') as f:
    data = json.load(f)

# new_string = json.dumps(data, indent=2)
# print(new_string)

with open('gunfire_indent.json', 'w') as f:
    json.dump(data, f, indent=2)