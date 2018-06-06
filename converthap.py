import json
import copy
import re


with open('gunfire.json') as f:
     data = json.load(f)

new_string = json.dumps(data, indent=2)
print(new_string)


i = 0
for key in data:
    i+=1
    print(key)
    if i == 5:
        break


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
# #                 continue

# # Convert | to , add 1 to value.replace for only first occurrence
# copydata = copy.deepcopy(data)

# for entry in copydata:
#     for key in entry:
#         if 'participant' in key:

#             re.match(pattern, string, flags=0)

for entry in copydata:
    for key in entry:
        if 'participant' in key:
            value = entry.get(key)
            if value == None:
                continue
            newvalue = value.split("||")
            splitted = {}
            for e in newvalue:
                newlist = e.split("::")
                if len(newlist) == 1:
                    continue
                splitted[newlist[0]] = newlist[1]
            entry[key] = splitted
        if 'characteristics' in key:
            value = entry.get(key)
            if value == None:
                continue
            newvalue = value.split("||")
            entry[key] = newvalue #HIER STAAT NU EEN LIJST IN MOET GEFIXT WORDEN

        # if 'participant' in key:
        #     value = entry.get(key)
        #     if value == None:
        #         continue
        #     value = value.replace('|', ',')
        #     entry[key] = value


# for entry in copydata:
#     for key in entry:
#         if 'participant' in key:
#             value = str(entry.get(key))
#             newvalue = value.split("||")
#             entry[key] = newvalue

# x = "0::Arrested||1::Injured||2::Injured||3::Injured||4::Injured"

# y = x.split("||")

# splitted_dict = {}
# for e in y:
#     index, status = e.split("::")
#     splitted_dict[index] = status
    

# print(splitted_dict)
# blabla[participant_status] = splitted_dict

#             # if value == None:
#             #     continue
#             # for i in value:
#             #     if i == '|':
#             #         # print("HOI")
#             #         i = ',' 
                
#         # if 'participant' in key:
#         #     for i in data.get(key):
#         #         if i == '|':
#         #             i = ','
#         #         else:
#         #             continue

# for i in range(len(copydata)):
#     if i < 4:
#         print(copydata[i])

with open('gunfire_indent.json', 'w') as f:
    json.dump(copydata, f, indent=2)


