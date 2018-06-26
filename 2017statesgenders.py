from bokeh.core.properties import value
from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.transform import dodge
from bokeh.layouts import gridplot
from bokeh.layouts import column
import json
import math
from bokeh.layouts import widgetbox
from bokeh.models.widgets import CheckboxGroup
from bokeh.layouts import row
from bokeh.io import output_file, show
from bokeh.layouts import widgetbox
from bokeh.models.widgets import CheckboxGroup

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

allmalesus = 0
allfemsus  = 0
allmalevic = 0
allfemvic = 0


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
        if key == 'Male suspect':
            allmalesus += states[iets]['Male suspect']
        elif key == 'Female suspect':
            allfemsus += states[iets]['Female suspect']
        elif key == 'Male victim':
            allmalevic += states[iets]['Male victim']
        elif key == 'Female victim':
            allfemvic += states[iets]['Female victim']
        # print(states[iets][key])

print(allmalesus, allfemsus, allmalevic, allfemvic)

output_file("bar_dodged2017.html")

sort = sorted(states)


# carrier_selection = CheckboxGroup(labels=[key for key in sort], 
#                                   active = [0, 1])
# [carrier_selection.labels[i] for i in carrier_selection.active]

# def update(attr, old, new):
#     # Get the list of carriers for the graph
#     carriers_to_plot = [carrier_selection.labels[i] for i in 
#                         carrier_selection.active]
#     # Make a new dataset based on the selected carriers and the 
#     # make_dataset function defined earlier
#     new_src = make_dataset(carriers_to_plot,
#                            range_start = -60,
#                            range_end = 120,
#                            bin_width = 5)
#     # Update the source used in the quad glpyhs
#     src.data.update(new_src.data)

# carrier_selection.on_change('active', update)


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


# output_file("checkbox_group.html")


p1.xaxis.major_label_orientation = math.pi/2
p1.x_range.range_padding = 0.1
p1.xgrid.grid_line_color = None
p1.legend.location = "top_left"
p1.legend.orientation = "horizontal"


show(p1)
#show(p2)

''' Present an interactive function explorer with slider widgets.
Scrub the sliders to change the properties of the ``sin`` curve, or
type into the title text box to update the title of the plot.
Use the ``bokeh serve`` command to run the example by executing:
    bokeh serve sliders.py
at your command prompt. Then navigate to the URL
    http://localhost:5006/sliders
in your browser.
'''
