import json
import copy
import re

with open('gunfire.json') as f:
    data = json.load(f)

# new_string = json.dumps(data, indent=2)
# print(new_string)



# for key in data:
#     if 'participant' in key:
#         for i in key:
#             if int(i):
#                 key[i]
#             elif i == ':' and i-1 == ':':
#                 data.key.[(i-2)] = i 
#                 i = ''
#                 i-1 = ''
#             elif i == ':':
#                 continue
#             elif i == '|' and i-1 == '|':
#                 i-1 = ''
#                 i = ','
#             elif i == '|':
#                 continue

# Convert | to , add 1 to value.replace for only first occurrence
copydata = copy.deepcopy(data)

for entry in copydata:
    for key in entry:
        if 'participant' in key:
            # re.match(pattern, string, flags=0)
            key = key

for entry in copydata:
    for key in entry:
        if 'participant' in key:
            value = entry.get(key)
            if value == None:
                continue
            value = value.replace('|', ',')
            entry[key] = value
            # if value == None:
            #     continue
            # for i in value:
            #     if i == '|':
            #         # print("HOI")
            #         i = ',' 
                
        # if 'participant' in key:
        #     for i in data.get(key):
        #         if i == '|':
        #             i = ','
        #         else:
        #             continue

for i in range(len(copydata)):
    if i < 4:
        print(copydata[i])
# # with open('gunfire_indent.json', 'w') as f:
#     json.dump(data, f, indent=2)

