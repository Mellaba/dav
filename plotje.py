from bokeh.core.properties import value
from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.transform import dodge
import json

with open('gunfire.json') as f:
    data = json.load(f)

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

print(gender_type_months['Male suspect'][0])

output_file("bar_dodged.html")

fruits = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
years = ['Male Victim', 'Male Suspect', 'Female Victim', 'Female Suspect']
colorsmen = ["#c9d9d3", "#718dbf"]
colorswomen = ["#718dbf", "#e84d60"]

data = {'fruits' : fruits,
        'Male Victim'   : [gender_type_months['Male victim'][0], gender_type_months['Male victim'][1], gender_type_months['Male victim'][2], gender_type_months['Male victim'][3], gender_type_months['Male victim'][4], gender_type_months['Male victim'][5], gender_type_months['Male victim'][6], gender_type_months['Male victim'][7], gender_type_months['Male victim'][8], gender_type_months['Male victim'][9], gender_type_months['Male victim'][10], gender_type_months['Male victim'][11]],
        'Male Suspect'   : [gender_type_months['Male suspect'][0], gender_type_months['Male suspect'][1], gender_type_months['Male suspect'][2], gender_type_months['Male suspect'][3], gender_type_months['Male suspect'][4], gender_type_months['Male suspect'][5], gender_type_months['Male suspect'][6], gender_type_months['Male suspect'][7], gender_type_months['Male suspect'][8], gender_type_months['Male suspect'][9], gender_type_months['Male suspect'][10], gender_type_months['Male suspect'][11]],
        'Female Victim' : [gender_type_months['Female victim'][0],gender_type_months['Female victim'][1], gender_type_months['Female victim'][2], gender_type_months['Female victim'][3], gender_type_months['Female victim'][4], gender_type_months['Female victim'][5], gender_type_months['Female victim'][6], gender_type_months['Female victim'][7], gender_type_months['Female victim'][8], gender_type_months['Female victim'][9], gender_type_months['Female victim'][10], gender_type_months['Female victim'][11]],
        'Female Suspect' : [gender_type_months['Female suspect'][0], gender_type_months['Female suspect'][1], gender_type_months['Female suspect'][2], gender_type_months['Female suspect'][3], gender_type_months['Female suspect'][4], gender_type_months['Female suspect'][5], gender_type_months['Female suspect'][6], gender_type_months['Female suspect'][7],gender_type_months['Female suspect'][8], gender_type_months['Female suspect'][9], gender_type_months['Female suspect'][10], gender_type_months['Female suspect'][11]]}


source = ColumnDataSource(data=data)

p = figure(x_range=fruits, y_range=(0, 20000), plot_height=350, title="Types per gender per month",
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

# output_file("bar_stacked.html")

# fruits = ['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries']
# years = ["2015", "2016", "2017"]
# colors = ["#c9d9d3", "#718dbf", "#e84d60"]

# data = {'fruits' : fruits,
#         '2015'   : [2, 1, 4, 3, 2, 4],
#         '2016'   : [5, 3, 4, 2, 4, 6],
#         '2017'   : [3, 2, 4, 4, 5, 3]}

# source = ColumnDataSource(data=data)

# p = figure(x_range=fruits, plot_height=350, title="Fruit Counts by Year",
#            toolbar_location=None, tools="")

# renderersfem = p.vbar_stack(years, x='fruits', width=0.9, color=colors, source=source,
#                          legend=[value(x) for x in years], name=years)
# renderersmale = p.vbar_stack(years, x='fruits', width=0.9, color=colors, source=source,
#                          legend=[value(x) for x in years], name=years)

# p.y_range.start = 0
# p.x_range.range_padding = 0.1
# p.xgrid.grid_line_color = None
# p.axis.minor_tick_line_color = None
# p.outline_line_color = None
# p.legend.location = "top_left"
# p.legend.orientation = "horizontal"

# show(p)