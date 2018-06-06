import json
import copy
import re


with open('gunfire.json') as f:
    data = json.load(f)

dataxs = data[1:4]

for item in dataxs:
    for key in item:
        if 'participant' in key:
            value = item.get(key)
            if value == None:
                continue
            newvalue = value.split("||")
            splitted = {}
            for e in newvalue:
                newlist = e.split("::")
                if len(newlist) == 1:
                    continue
                splitted[newlist[0]] = newlist[1]
            item[key] = splitted
        if 'characteristics' in key:
            value = item.get(key)
            if value == None:
                continue
            newvalue = value.split("||")
            item[key] = newvalue
print(dataxs)