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

# print(victimgender)

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

# print(gendermonths)

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

# print(gender_type_months)


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

# print(gender_type_years)
print(genderdict, victimgender)

from bokeh.core.properties import value
from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import figure

output_file("bar_stacked.html")

genders = ['Male', 'Female']
types = ["Victim", "Suspect"]
colors = ["#c9d9d3", "#718dbf"]

data = {'genders' : genders,
        'Victim'   : [136394, 30630],
        'Suspect'   : [167708, 11746]}

source = ColumnDataSource(data=data)

p = figure(x_range=genders, plot_height=350, title="Gender in gunviolence by type",
           toolbar_location=None, tools="")

renderers = p.vbar_stack(types, x='genders', width=0.9, color=colors, source=source,
                         legend=[value(x) for x in types], name=types)

p.y_range.start = 0
p.x_range.range_padding = 0.1
p.xgrid.grid_line_color = None
p.axis.minor_tick_line_color = None
p.outline_line_color = None
p.legend.location = "top_left"
p.legend.orientation = "horizontal"

show(p)

