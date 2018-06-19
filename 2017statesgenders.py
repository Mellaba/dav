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

states = {}

for incident in data:
    year = incident["date"][0]
    if year == '2017':
        genders = incident["participant_gender"]
        victims = incident["participant_type"]
        state = incident["state"]
        if genders == None or victims == None or state == None:
            continue
        if state not in states:
            states[state] = {'Male suspect': 0, 'Female suspect': 0, 'Male victim':0, 'Female victim':0}
        for key in genders:
            gender = genders.get(key)
            thetype = victims.get(key)
            if gender == 'Male' and thetype == 'Subject-Suspect':
                states[state]['Male suspect'] += 1
            elif gender == 'Female' and thetype == 'Subject-Suspect':
                states[state]['Female suspect'] += 1
            elif gender == 'Male' and thetype == 'Victim':
                states[state]['Male victim'] += 1
            elif gender == 'Female' and thetype == 'Victim':
                states[state]['Female victim'] += 1

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
    for key in states[iets]:
        howmany = int(states[iets].get(key))
        standardized = howmany/int(countlist[indexnum])*100000
        states[iets][key] = standardized
        print(states[iets][key])

output_file("bar_dodged2017.html")

sort = sorted(states)

fruits1 = [key for key in sorted(states)]
years = ['Male Victim', 'Male Suspect', 'Female Victim', 'Female Suspect']
colorsmen = ["#c9d9d3", "#718dbf"]
colorswomen = ["#718dbf", "#e84d60"]


data = {'fruits1' : fruits1,
        'Male Victim'   : [states[key]['Male victim'] for key in sort],
        'Male Suspect'   : [states[key]['Male suspect'] for key in sort],
        'Female Victim' : [states[key]['Female victim'] for key in sort],
        'Female Suspect' : [states[key]['Female suspect'] for key in sort]}


# print([states[key]['Male victim'] for key in states])

source = ColumnDataSource(data=data)

p1 = figure(x_range=fruits1, y_range=(0, 50), plot_height=350, plot_width=2000, title="Types per gender per state 2017",
           toolbar_location=None, tools="")

p1.vbar(x=dodge('fruits1', -0.25, range=p1.x_range), top='Male Victim', width=0.2, source=source,
       color="#aeaeb8", legend=value("Male Victim"))

p1.vbar(x=dodge('fruits1',  0.0,  range=p1.x_range), top='Male Suspect', width=0.2, source=source,
       color="#0d3362", legend=value("Male Suspect"))

p1.vbar(x=dodge('fruits1',  0.25,  range=p1.x_range), top='Female Victim', width=0.2, source=source,
       color="#e69584", legend=value("Female Victim"))

p1.vbar(x=dodge('fruits1',  0.5,  range=p1.x_range), top='Female Suspect', width=0.2, source=source,
       color="#c64737", legend=value("Female Suspect"))


p1.xaxis.major_label_orientation = math.pi/2
p1.x_range.range_padding = 0.1
p1.xgrid.grid_line_color = None
p1.legend.location = "top_left"
p1.legend.orientation = "horizontal"

# show(gridplot(p1,p2, nrows=2, plot_width=2000, plot_height=350, toolbar_location=None))
show(p1)
#show(p2)