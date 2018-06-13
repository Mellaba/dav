import json

with open('gunfire.json') as f:
    data = json.load(f)


# GENDER VERDELING IN ALLE DATA

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

# GENDER VERDELING IN ALLE DATA PER TYPE

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

# GENDER PER MAAND

months = {}
gendermonths = {'Male':[0,0,0,0,0,0,0,0,0,0,0,0], 'Female':[0,0,0,0,0,0,0,0,0,0,0,0]}

for incident in data:
    datelist = incident["date"]
    month = int(datelist[1])-1
    genders = incident["participant_gender"]
    if genders == None:
        continue
    for key in genders:
        gender = genders.get(key)
        if gender == 'Male':
            gendermonths['Male'][month] += 1
        elif gender == 'Female':
            gendermonths['Female'][month] += 1

print(gendermonths)

# GENDER TYPE PER MAAND

gender_type_months = {'Male suspect':[0,0,0,0,0,0,0,0,0,0,0,0], 'Female suspect':[0,0,0,0,0,0,0,0,0,0,0,0], 'Male victim':[0,0,0,0,0,0,0,0,0,0,0,0], 'Female victim':[0,0,0,0,0,0,0,0,0,0,0,0]}

for incident in data:
    datelist = incident["date"]
    month = int(datelist[1])-1
    genders = incident["participant_gender"]
    victims = incident["participant_type"]
    if genders == None:
        continue
    for key in genders:
        gender = genders.get(key)
        thetype = victims.get(key)
        if gender == 'Male' and thetype == 'Subject-Suspect':
            gender_type_months['Male suspect'][month] += 1
        elif gender == 'Female' and thetype == 'Subject-Suspect':
            gender_type_months['Female suspect'][month] += 1
        elif gender == 'Male' and thetype == 'Victim':
            gender_type_months['Male victim'][month] += 1
        elif gender == 'Female' and thetype == 'Victim':
            gender_type_months['Female victim'][month] += 1

print(gender_type_months)


# GENDER TYPE PER JAAR

gender_type_years = {'Male suspect':[0,0,0,0], 'Female suspect':[0,0,0,0], 'Male victim':[0,0,0,0], 'Female victim':[0,0,0,0]}
            
for incident in data:
    datelist = incident["date"]
    year = int(datelist[0])-2014
    if year == -1 or year == 4:
        continue
    genders = incident["participant_gender"]
    victims = incident["participant_type"]
    if genders == None:
        continue
    for key in genders:
        gender = genders.get(key)
        thetype = victims.get(key)
        if gender == 'Male' and thetype == 'Subject-Suspect':
            gender_type_years['Male suspect'][year] += 1
        elif gender == 'Female' and thetype == 'Subject-Suspect':
            gender_type_years['Female suspect'][year] += 1
        elif gender == 'Male' and thetype == 'Victim':
            gender_type_years['Male victim'][year] += 1
        elif gender == 'Female' and thetype == 'Victim':
            gender_type_years['Female victim'][year] += 1

print(gender_type_years)
