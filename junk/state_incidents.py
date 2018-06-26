import pandas as pd
import numpy as np
import math
import json

from bokeh.core.properties import value
from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure

def all_states(data):
    states = []
    for incident in data:
        if incident['state'] not in states:
            states.append(incident['state'])
    return states

def state_incidents(states, data):
    d = {'states' : states,
         '2013' : [0]*len(states),
         '2014' : [0]*len(states),
         '2015' : [0]*len(states),
         '2016' : [0]*len(states),
         '2017' : [0]*len(states),
         '2018' : [0]*len(states),
         }

    for incident in data:
        state = d['states'].index(incident['state'])
        d[incident['date'][0]][state] += 1
    return d

def plot(incidents):
    years = list(incidents.keys())[1:]
    states = incidents['states']
    colors = ["#c9d9d3", "#718dbf", "#e84d60","#696969", "#FF8C00",  "#FF1493"]
    source = ColumnDataSource(data=incidents)

    p = figure(x_range=states, plot_height=250, title="Incidents per state per year",
           toolbar_location=None, tools="")

    p.vbar_stack(years, x='states', width=0.9, color=colors, source=source,
             legend=[value(x) for x in years])

    p.y_range.start = 0
    p.x_range.range_padding = 0
    p.xgrid.grid_line_color = None
    p.axis.minor_tick_line_color = None
    p.xaxis.major_label_orientation = math.pi/3
    p.outline_line_color = None
    p.legend.location = "top_right"
    p.legend.orientation = "horizontal"
    show(p)

def main():

    with open('gunfire.json') as f:
	    data = json.load(f)
    states = all_states(data)
    incidents = state_incidents(states, data)
    plot(incidents)


if __name__ == "__main__":
    main()
