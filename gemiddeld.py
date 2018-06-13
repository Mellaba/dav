import json

with open('gunfire.json') as f:
    data = json.load(f)

# deze code kijkt naar hoeveel mensen er per schietpartij gewond if gedood zijn en telt ook de daders hierbij
n_woundedorkilled = 0

for incident in data:
    injured = int(incident["n_injured"])
    killed = int(incident["n_killed"])
    n_woundedorkilled += killed 
    n_woundedorkilled += injured
print(n_woundedorkilled)

count = len(data)
gemiddeld = n_woundedorkilled / count
print(gemiddeld)

# plotje met wanneer er niemand gewond raakt en wanneer injured en wanneer gewond

# Deze code kijkt naar hoeveel mensen er per schietpatij gewond of gedood zijn zonder de dader hierbij te betrekken

# Hoe vaak raakt de dader zelf ook gewond of dood?

howmanytimes = {}

for incident in data:
    victimsandsuspects = incident["participant_type"]
    if victimsandsuspects == None:
        continue
    killedorinjured = incident["participant_status"]
    if killedorinjured == None:
        continue
    for key in victimsandsuspects:
        if key == None:
            continue
        thetype = victimsandsuspects.get(key)
        if thetype == 'Subject-Suspect':
            whathappened = killedorinjured.get(key)
            if whathappened == None:
                continue
            if whathappened not in howmanytimes:
                howmanytimes[whathappened] = 1
            else:
                howmanytimes[whathappened] += 1


