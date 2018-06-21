from bokeh.core.properties import value
from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.transform import dodge
import json

with open('gunfire.json') as f:
    data = json.load(f)

states = {}

for incident in data:
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

# print(statelist, countlist)
print(statelist)

for iets in statelist:
    indexnum = int(statelist.index(iets))
    for key in states[iets]:
        howmany = int(states[iets].get(key))
        standardized = howmany/int(countlist[indexnum])*100000
        print(standardized)

output_file("bar_dodged.html")

fruits = [key for key in states]
years = ['Male Victim', 'Male Suspect', 'Female Victim', 'Female Suspect']
colorsmen = ["#c9d9d3", "#718dbf"]
colorswomen = ["#718dbf", "#e84d60"]


data = {'fruits' : fruits,
        'Male Victim'   : [states[key]['Male victim'] for key in states],
        'Male Suspect'   : [states[key]['Male suspect'] for key in states],
        'Female Victim' : [states[key]['Female victim'] for key in states],
        'Female Suspect' : [states[key]['Female suspect'] for key in states]}

# print([states[key]['Male victim'] for key in states])

source = ColumnDataSource(data=data)

p = figure(x_range=fruits, y_range=(0, 2000), plot_height=350, plot_width=2000, title="Types per gender per month",
           toolbar_location=None, tools="")

p.vbar(x=dodge('fruits', -0.25, range=p.x_range), top='Male Victim', width=0.2, source=source,
       color="#aeaeb8", legend=value("Male Victim"))

p.vbar(x=dodge('fruits',  0.0,  range=p.x_range), top='Male Suspect', width=0.2, source=source,
       color="#0d3362", legend=value("Male Suspect"))

p.vbar(x=dodge('fruits',  0.25,  range=p.x_range), top='Female Victim', width=0.2, source=source,
       color="#e69584", legend=value("Female Victim"))

p.vbar(x=dodge('fruits',  0.5,  range=p.x_range), top='Female Suspect', width=0.2, source=source,
       color="#c64737", legend=value("Female Suspect"))



p.x_range.range_padding = 0.1
p.xgrid.grid_line_color = None
p.legend.location = "top_left"
p.legend.orientation = "horizontal"

show(p)