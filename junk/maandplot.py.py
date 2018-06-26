from collections import OrderedDict
from math import log, sqrt

import json
import re
import numpy as np
import pandas as pd

import numpy as np
import scipy.special

from bokeh.layouts import gridplot
from bokeh.plotting import figure, show, output_file
from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource, FactorRange
from bokeh.transform import factor_cmap

def incidents_per_season():
    with open('gunfire.json') as f:
	    data = json.load(f)

    columns = ['2014', '2015', '2016', '2017', '2018']
    months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    df = pd.DataFrame(index=months, columns=columns)

    incidents = 0
    for year in df:        
        for month in months:
            for entry in data:
                if entry['date'][0] == year and entry['date'][1] == month:
                    incidents += 1
            df.ix[month, year] = incidents
            incidents = 0

    return df, columns, months    

data, years, months = incidents_per_season()

#for month in months:
 #   print(np.mean(data.loc[month]))

output_file("bar_nested_colormapped.html")

palette = ["#c9d9d3", "#718dbf", "#e84d60", "#b821a7"]

# this creates [ ("Apples", "2015"), ("Apples", "2016"), ("Apples", "2017"), ("Pears", "2015), ... ]
x = [ (month, year) for month in months for year in years ]
counts = sum(zip(data['2014'], data['2015'], data['2016'], data['2017'], data['2018']), ()) # like an hstack

source = ColumnDataSource(data=dict(x=x, counts=counts))

p = figure(x_range=FactorRange(*x), plot_height=450, title="Aantal incidenten per maand per jaar",
           toolbar_location=None, tools="")

p.vbar(x='x', top='counts', width=1, source=source, line_color="white",
       fill_color=factor_cmap('x', palette=palette, factors=years, start=1, end=3))

y_line = []
for month in months:
    if data.loc[month]["2018"] == 0:
        y_line.append(sum(data.loc[month])/4)
        continue
    y_line.append(np.mean(data.loc[month]))

x_line = [month for month in months]
p.line(x_line, y_line, line_color="#D95B43", line_width=8, alpha=0.7, legend="Gemiddelde")

p.y_range.start = 0
p.x_range.range_padding = 0.05
p.xaxis.major_label_orientation = 1
p.xgrid.grid_line_color = None

show(p)


