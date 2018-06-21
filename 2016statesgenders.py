from bokeh.core.properties import value
from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.transform import dodge
from bokeh.layouts import gridplot
from bokeh.layouts import column
import json
import math

with open('gunfire.json') as f:
    data = json.load(f)

states2 = {}
for incident in data:
    year = incident["date"][0]
    if year == '2016':
        genders = incident["participant_gender"]
        victims = incident["participant_type"]
        state = incident["state"]
        if genders == None or victims == None or state == None:
            continue
        if state not in states2:
            states2[state] = {'Male suspect': 0, 'Female suspect': 0, 'Male victim':0, 'Female victim':0}
        for key in genders:
            gender = genders.get(key)
            thetype = victims.get(key)
            if gender == 'Male' and thetype == 'Subject-Suspect':
                states2[state]['Male suspect'] += 1
            elif gender == 'Female' and thetype == 'Subject-Suspect':
                states2[state]['Female suspect'] += 1
            elif gender == 'Male' and thetype == 'Victim':
                states2[state]['Male victim'] += 1
            elif gender == 'Female' and thetype == 'Victim':
                states2[state]['Female victim'] += 1

statelist = []
countlist = []
with open('populationstate2017.txt') as s:
    temp = s.read().splitlines()
    for elem in temp:
        state, amount = elem.split(',')
        statelist.append(state)
        countlist.append(amount)

for iets in statelist:
    indexnum = int(statelist.index(iets))
    for key in states2[iets]:
        howmany = int(states2[iets].get(key))
        standardized = howmany/int(countlist[indexnum])*100000
        states2[iets][key] = standardized
        print(states2[iets][key])

output_file("bar_dodged2016.html")

sort = sorted(states2)

fruits2 = [key for key in sort]
years = ['Male Victim', 'Male Suspect', 'Female Victim', 'Female Suspect']
colorsmen = ["#c9d9d3", "#718dbf"]
colorswomen = ["#718dbf", "#e84d60"]

data = {'fruits2' : fruits2,
        'Male Victim'   : [states2[key]['Male victim'] for key in sort],
        'Male Suspect'   : [states2[key]['Male suspect'] for key in sort],
        'Female Victim' : [states2[key]['Female victim'] for key in sort],
        'Female Suspect' : [states2[key]['Female suspect'] for key in sort]}

source = ColumnDataSource(data=data)

p2 = figure(x_range=fruits2, y_range=(0, 50), plot_height=350, plot_width=2000, title="Types per gender per state 2016",
           toolbar_location=None, tools="")

p2.vbar(x=dodge('fruits2', -0.25, range=p2.x_range), top='Male Victim', width=0.2, source=source,
       color="#aeaeb8", legend=value("Male Victim"))

p2.vbar(x=dodge('fruits2',  0.0,  range=p2.x_range), top='Male Suspect', width=0.2, source=source,
       color="#0d3362", legend=value("Male Suspect"))

p2.vbar(x=dodge('fruits2',  0.25,  range=p2.x_range), top='Female Victim', width=0.2, source=source,
       color="#e69584", legend=value("Female Victim"))

p2.vbar(x=dodge('fruits2',  0.5,  range=p2.x_range), top='Female Suspect', width=0.2, source=source,
       color="#c64737", legend=value("Female Suspect"))

p2.xaxis.major_label_orientation = math.pi/2
p2.x_range.range_padding = 0.1
p2.xgrid.grid_line_color = None
p2.legend.location = "top_left"
p2.legend.orientation = "horizontal"

show(p2)