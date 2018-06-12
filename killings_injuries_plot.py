from bokeh.core.properties import value
from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import figure

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json


def injured_killed(years, data):
	injuries = {}
	killings = {}	
	for year in years:
		injuries.setdefault(year, 0)
		killings.setdefault(year, 0)

	for incident in data:
		year = incident['date'][0]
		#print(year, injuries[year])
		dead = incident['n_killed'] 
		injured = incident['n_injured']
		injuries[year] += injured
		killings[year] += dead
		#print(year, injuries[year], killings[year], injured, dead)
	#print(injuries)
	#print(killings)
	return injuries, killings

def dicts_format(injuries, killings, years):
	data = {}
	data['years'] = years
	data.setdefault('injuries', [])
	data.setdefault('killings', [])
	for year in years:
		data['injuries'].append(injuries[year])
		data['killings'].append(killings[year])
	return data


def plot(data, years):
	from bokeh.io import output_file
	output_file("output_file.html")
	
	types = ["injuries", "killings"]
	colors = ["#c9d9d3", "#718dbf"]

	source = ColumnDataSource(data=data)

	p = figure(x_range=years, plot_height=350, title="Injuries and Killings by Year",
	           toolbar_location=None, tools="")

	renderers = p.vbar_stack(types, x='years', width=0.9, color=colors, source=source,
	                         legend=[value(x) for x in types], name=types)
	for r in renderers:
	    types = r.name
	    hover = HoverTool(tooltips=[
	        ("%s total" % types, "@%s" % types)], renderers=[r])
	    p.add_tools(hover)

	p.y_range.start = 0
	p.x_range.range_padding = 0.1
	p.xgrid.grid_line_color = None
	p.axis.minor_tick_line_color = None
	p.outline_line_color = None
	p.legend.location = "top_left"
	p.legend.orientation = "horizontal"
	show(p)


def main():
	with open('gunfire.json') as f:
		data = json.load(f)

	years = [str(x) for x in range(2013,2019)]
	injuries, killings = injured_killed(years, data)
	data = dicts_format(injuries, killings, years)
	plot(data, years)
	return None

main()