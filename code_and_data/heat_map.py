''' Creates a map plot of the number of incidents per state per 10,000 residents over 2017.
'''

import pandas as pd
import json

from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource
from bokeh.models import HoverTool
from bokeh.sampledata.us_states import data as states

def violence_rate(data):
    ''' Calculates incident rate using a text file with population per state.
    '''
    state_incidents = {}
    for incident in data:
        state = incident["state"]
        if int(incident['date'][0]) == 2017:
            if state in state_incidents:
                state_incidents[state] += 1
            else:
                state_incidents[state] = 1

    df = pd.read_csv('populationstate2017.txt', header=None)
    for index, row in df.iterrows():
        if index != 50:
            state = row[0].title()
        else:
            state = row[0]
        state_incidents[state] = state_incidents[state]/row[1] * 10000

    return state_incidents

def heat_plot(state_incidents, states):
    ''' Plots the map fills the states with right colors.
    '''
    EX = ["Hawaii", "Alaska"]

    del states["HI"]
    del states["AK"] 
    state_xs = [(states[code]["lons"],states[code]['name']) for code in states]
    state_ys = [(states[code]["lats"],states[code]['name']) for code in states]
    
    names = [state for state in state_incidents.keys() if state not in EX]
    rates = [state_incidents[state] for state in state_incidents.keys() if state not in EX]

    state_lons = []
    state_lats = []
    for name in names:
        index = [y[1] for y in state_xs].index(name)
        state_lons.append(state_xs[index][0])
        state_lats.append(state_ys[index][0])

    colors = ["#F1EEF6", "#D4B9DA", "#C994C7", "#DF65B0", "#DD1C77", "#980043"]
    state_colors = [colors[int(rate%6)] for rate in rates]
    data=ColumnDataSource(dict(
        x=state_lons,
        y=state_lats,
        state=names,
        rate=rates,
        color=state_colors
    ))

    TOOLS = "pan,wheel_zoom,reset,hover,save"

    p = figure(
    x_axis_location=None, y_axis_location=None, plot_width=850, plot_height=550, tools=TOOLS)
    p.grid.grid_line_color = None
    p.patches('x', 'y', source=data, fill_color='color', fill_alpha=0.7,
          line_color="#884444", line_width=2, line_alpha=0.3)

    hover = p.select_one(HoverTool)
    hover.point_policy = "follow_mouse"
    hover.tooltips = [
    ("Name", "@state"),
    ("Unemployment rate)", "@rate"),
    ("(Long, Lat)", "($x, $y)"),
    ]

    output_file("states_heat_map.html", title="Number of incidents per 10,000 habitants in 2017")
    show(p)

def main():

    with open('gunfire.json') as f:
        d = json.load(f)
    state_incidents = violence_rate(d)
    heat_plot(state_incidents, states)

if __name__ == "__main__":
    main()
