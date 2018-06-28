import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json

# killer - victim
# how many victims
# does killer kill more
# gang/or fmiliy or something else??
# unique values per column
# child involved incidents

# slachtoffers per incident + std
# gimmiddeld aantal slachtoffer + std 

# in hoeveel gevallen raakt de suspect zelf gewond/dood

# 21x ofc of security als name, 


'''
with open('gunfire.json') as f:
	data = json.load(f)

print(data[0]['n_injured'])


injured = 0
killed = 0
accidental = 0
for incident in data:
	if incident['incident_characteristics'] is not None:
		if "Child Involved Incident" in incident['incident_characteristics']:
			accidental += 1
	injured += incident['n_injured']
	killed += incident['n_killed']

print(injured, killed, accidental)


#5000 accidental injuries
#8000 total accidental shootings (killings&injuries)


#injuries, killings, accidental shootings 
#118402 60468 8075

# 2100 keer Child Involved Incident


adults = 0
teens = 0
childs = 0
for incident in data:
	if incident['participant_age_group'] is not None:
		#for key, value in dict if value is "Child" child += 1 etcetc
		if "Child Involved Incident" in incident['participant_age_group']:
			accidental += 1
	injured += incident['n_injured']
	killed += incident['n_killed']

print(injured, killed, accidental)
'''

'''
from bokeh.core.properties import value
from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import figure

output_file("bar_stacked.html")

fruits = ['2013', '2014', '2015', '2016', '2017']
years = ["injuries", "killings"]
colors = ["#c9d9d3", "#718dbf"]

data = {'fruits' : fruits,
        'injuries'   : [2, 1, 4, 3, 2],
        'killings'   : [5, 3, 4, 2, 4]}

source = ColumnDataSource(data=data)

p = figure(x_range=fruits, plot_height=350, title="Injuries and Killings by Year",
           toolbar_location=None, tools="")

renderers = p.vbar_stack(years, x='fruits', width=0.9, color=colors, source=source,
                         legend=[value(x) for x in years], name=years)

for r in renderers:
    year = r.name
    hover = HoverTool(tooltips=[
        ("%s total" % year, "@%s" % year),
        ("index", "$index")
    ], renderers=[r])
    p.add_tools(hover)

p.y_range.start = 0
p.x_range.range_padding = 0.1
p.xgrid.grid_line_color = None
p.axis.minor_tick_line_color = None
p.outline_line_color = None
p.legend.location = "top_left"
p.legend.orientation = "horizontal"

show(p)
'''


'''
with open('gunfire.json') as f:
	data = json.load(f)

injuries = {}
killings = {}


years = [str(x) for x in range(2013,2019)]	
for year in years:
	injuries.setdefault(year, 0)
	killings.setdefault(year, 0)

for incident in data:
	year = incident['date'][0]
	print(year, injuries[year])
	dead = incident['n_killed'] 
	injured = incident['n_injured']
	injuries[year] += injured
	killings[year] += dead
	#print(year, injuries[year], killings[year], injured, dead)

print(injuries)
print(killings)
'''

with open('gunfire.json') as f:
	data = json.load(f)


'''
look at unique values 
values = set()
for item in data:
	if item['participant_type'] is not None:
		for person in item['participant_type']:
			values.add(item['participant_type'][person])

print(values)
'''

s_v = {}
v = {}
s = {}

for incident in data:
	suspects = 0
	victims = 0
	if incident['participant_type'] is not None:
		for participant in incident['participant_type']:
			if incident['participant_type'][participant] == "Subject-Suspect":
				suspects += 1
			if incident['participant_type'][participant] == "Victim":
				victims += 1
		if (suspects, victims) in s_v:
			s_v[(suspects, victims)] += 1
		else:
			s_v[(suspects, victims)] = 1
		if suspects in s:
			s[suspects] += 1
		else:
			s[suspects] = 1
		if victims in v:
			v[victims] +=1
		else: 
			v[victims] = 1


print(v)
print("\n")
print(s)


'''
print(list(s_v.keys()))
print(sorted(list(s_v.keys()), key=lambda x: x[1]))
'''

'''
for incident in data:
	if incident['incident_id'] == "577157":
		print(incident)
	if incident['incident_id'] == 577157:
		print(incident)
'''




hist = []
edges = []
'''
for victims in v:
	hist.append(v[victims])
	edges.append(victims)
'''
for suspects in s:
	hist.append(s[suspects])
	edges.append(suspects)



tupls =list(zip(hist,edges))
print(hist)
tups = sorted(tupls, key=lambda x: x[1])


print("\n")
for tup in tups:
	print(tup[0],"\t", tup[1])


hist = []
edges = []
for tupl in tups:
	hist.append(tupl[0])
	edges.append(tupl[1])

edges.append(max(edges) + 1)

print(hist)
print(edges)

print(len(hist), len(edges))


'''
plot histogram killer/victim numbers
import numpy as np
import scipy.special

from bokeh.layouts import gridplot
from bokeh.plotting import figure, show, output_file


p3 = figure(title="Victims by occurence", tools="save",
            background_fill_color="#E8DDCB")

p3.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
        fill_color="#036564", line_color="#033649")


p3.legend.location = "center_right"
p3.legend.background_fill_color = "darkgrey"
p3.xaxis.axis_label = '#victims'
p3.yaxis.axis_label = '#occurence`'


p4 = figure(title="Victims by occurence", tools="save",
            background_fill_color="#E8DDCB")

hist2 = hist[20:]
edges2 = edges[20:]


p4.quad(top=hist2, bottom=0, left=edges2[:-1], right=edges2[1:],
        fill_color="#036564", line_color="#033649")


p4.legend.location = "center_right"
p4.legend.background_fill_color = "darkgrey"
p4.xaxis.axis_label = 'x'
p4.yaxis.axis_label = 'Pr(x)'



p2 = figure(title="Victims by occurence", tools="save",
            background_fill_color="#E8DDCB")

hist1 = hist[:20]
edges1 = edges[:21]


p2.quad(top=hist1, bottom=0, left=edges1[:-1], right=edges1[1:],
        fill_color="#036564", line_color="#033649")


p2.legend.location = "center_right"
p2.legend.background_fill_color = "darkgrey"
p2.xaxis.axis_label = 'x'
p2.yaxis.axis_label = 'Pr(x)'




output_file('histogram.html', title="histogram.py example")

show(gridplot(p2, p3, p4, ncols=2, plot_width=400, plot_height=400, toolbar_location=None))
'''


'''


import numpy as np
import scipy.special

from bokeh.layouts import gridplot
from bokeh.plotting import figure, show, output_file

p3 = figure(title="Gamma Distribution (k=1, θ=2)", tools="save",
            background_fill_color="#E8DDCB")

k, theta = 1.0, 2.0

measured = np.random.gamma(k, theta, 1000)
hist, edges = np.histogram(measured, density=True, bins=50)
print(len(hist), len(edges))

p3.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
        fill_color="#036564", line_color="#033649")


p3.legend.location = "center_right"
p3.legend.background_fill_color = "darkgrey"
p3.xaxis.axis_label = 'x'
p3.yaxis.axis_label = 'Pr(x)'



output_file('histogram.html', title="histogram.py example")

show(gridplot(p3, ncols=2, plot_width=400, plot_height=400, toolbar_location=None))

''' 


