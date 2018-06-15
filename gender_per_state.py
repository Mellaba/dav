import json

with open('gunfire.json') as f:
    data = json.load(f)

genderstatedict = {}

for incident in data:
    genders = incident["participant_gender"]
    state = incident["state"]
    victims = incident["participant_type"]
    if state == None or genders == None or victims == None:
        continue
    if state not in genderstatedict:
        genderstatedict[state] = {'Male suspect':0, 'Female suspect': 0, 'Male victim': 0, 'Female victim':0}
    for key in genders:
        if key == None:
            continue
        gender = genders.get(key)
        thetype = victims.get(key)
        if gender == None or thetype == None:
            continue
        if gender == 'Male' and thetype == 'Subject-Suspect':
            genderstatedict[state]['Male suspect'] += 1
        elif gender == 'Female' and thetype == 'Subject-Suspect':
            genderstatedict[state]['Female suspect'] += 1
        elif gender == 'Male' and thetype == 'Victim':
            genderstatedict[state]['Male victim'] += 1
        elif gender == 'Female' and thetype == 'Victim':
            genderstatedict[state]['Female victim'] += 1

from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure

print(genderstatedict)

colormen = ['#084594', '#2171b5']
colorwomen =  ['#4292c6', '#6baed6']
malesuspectlist = []
femalesuspectlist = []
malevictimlist = []
femalevictimlist = []


statelist = []
for key in genderstatedict:
    statelist.append(key)
    for i in genderstatedict[key]:
        if i == 'Male suspect':
            value = genderstatedict[key].get(i)
            malesuspectlist.append(value)
        if i == 'Female suspect':
            value = - int(genderstatedict[key].get(i))
            femalesuspectlist.append(value)
        if i == 'Male victim':
            value = genderstatedict[key].get(i)
            malevictimlist.append(value)
        if i == 'Female victim':
            value = - int(genderstatedict[key].get(i))
            femalevictimlist.append(value)

print(malesuspectlist)
print(femalesuspectlist)
output_file("bar_stacked_split.html")

fruits = statelist
years = ["Suspect", "Victim"]

exports = {'fruits' : fruits,
           'Suspect'   : malesuspectlist,
           'Victim'   : malevictimlist}
imports = {'fruits' : fruits,
           'Suspect'   : femalesuspectlist,
           'Victim'   : femalevictimlist}

p = figure(y_range=fruits, plot_height=700, x_range=(-4000, 15000), title="Fruit import/export, by year",
           toolbar_location=None)

p.hbar_stack(years, y='fruits', height=0.9, color=colormen, source=ColumnDataSource(exports),
             legend=["Male %s" % x for x in years])

p.hbar_stack(years, y='fruits', height=0.9, color=colorwomen, source=ColumnDataSource(imports),
             legend=["Female %s" % x for x in years])

p.y_range.range_padding = 0.1
p.ygrid.grid_line_color = None
p.legend.location = "top_left"
p.axis.minor_tick_line_color = None
p.outline_line_color = None

show(p)