import json
from bokeh.plotting import *
from numpy import pi

with open('gunfire.json') as f:
    data = json.load(f)


# # define starts/ends for wedges from percentages of a circle
# percents = [0, 0.3, 0.4, 0.6, 0.9, 1]
# starts = [p*2*pi for p in percents[:-1]]
# ends = [p*2*pi for p in percents[1:]]

# # a color for each pie piece
# colors = ["red", "green", "blue", "orange", "yellow"]

# p = figure(x_range=(-1,1), y_range=(-1,1))

# p.wedge(x=0, y=0, radius=1, start_angle=starts, end_angle=ends, color=colors)

# # display/save everythin  
# output_file("pie.html")
# show(p)

from bokeh.io import curdoc
from bokeh.layouts import layout
from bokeh.models import (HoverTool, ColumnDataSource, Legend, LegendItem)
from bokeh.plotting import figure, show
from bokeh.palettes import brewer
from numpy import pi

starts = [0.0, 0.27429672626751683, 0.8713156234544629, 5.1821330567582686, 6.245873609350836]

ends = [0.27429672626751683, 0.8713156234544629, 5.1821330567582686, 6.245873609350836, 6.2831853071795862]

labels = ['Male Victim', 'Male Suspect', 'Female Victim', 'Female Suspect', 'e']

colors = ['#2b83ba', '#abdda4', '#ffffbf', '#fdae61', '#d7191c']

amounts = ['1,521,377', '3,311,344', '23,909,795', '5,899,999', '206,948']



source=ColumnDataSource(dict(starts=starts, ends=ends, labels=labels, colors=colors, amounts=amounts))



plot =  figure()



hover = HoverTool(

        tooltips=[

          ('type', '@labels'),

          ('quantity','@amounts')

        ]

    )

plot.add_tools(hover)
portions = []

for i in range(len(starts)):
    portions.append(plot.wedge(x=0, y=0, radius=1, start_angle='starts', end_angle='ends', color='colors', source=source))



legend_items = []

for idx, portion in enumerate(portions):
    legend_items.append(LegendItem(label=labels[idx], renderers=[portion]))
legend = Legend(items=legend_items, location=(40, 0))
plot.add_layout(legend, 'right')
layout = layout([[plot],])
show(plot)