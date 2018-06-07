import numpy as np
import json
from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource
import bokeh.palettes
from bokeh.plotting import figure


def incident_per_state():
    states = {}
    with open('gunfire_small.json') as f:
     data = json.load(f)
    for entry in data:
        if entry['state'] not in states:
            states[entry['state']] = 1
        else:
            states[entry['state']] += 1
    
    return states

d = incident_per_state()

states = list(d.keys())
# state_abb = [state[:2] for state in states]
incidents = list(d.values())

source = ColumnDataSource(data=dict(states=states, incidents=incidents))

output_file("bars.html")

p = figure(x_range=states, plot_height=250, title="Incidents per state",
           toolbar_location=None, tools="")

p.vbar(x='states', top='incidents', width=0.9, source=source)

p.xgrid.grid_line_color = None
p.y_range.start = 0

show(p)
