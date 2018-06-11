import json

with open('gunfire.json') as f:
    data = json.load(f)

genderdict = {}

for incident in data:
    for entry in incident:
        genders = incident["participant_gender"]
        if genders == None:
            continue
        for key in genders:
            if key == None:
                continue
            value = genders.get(key)
            if value == None:
                continue
            if value not in genderdict:
                genderdict[value] = 1
            else:
                genderdict[value] += 1

victimgender = {}

for incident in data:
    genders = incident["participant_gender"]
    victims = incident["participant_type"]
    if genders == None:
        continue
    for key in genders:
        if key == None:
            continue
        gender = genders.get(key)
        thetype = victims.get(key)
        if gender == None or thetype == None:
            continue
        value = (gender, thetype)
        if value not in victimgender:
            victimgender[value] = 1
        else:
            victimgender[value] += 1

print(victimgender)

