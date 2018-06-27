from bokeh.core.properties import value
from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import figure

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import math

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

def plot_injuries_kill_year(data, years):
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




def count_stuff(data):
    ''' count   #victims, #suspects
                #injured #killed (2 columns)
                #incidents total '''
    
    nones_val = [0,0]   #participant status, #p type
    victims = 0
    suspects = 0
    incidents = 0
    incidents_with_injury = 0
    incidents_with_kill = 0
    incidents_with_victim = 0
    incidents_with_no_victim = 0
    incidents_with_kill_and_injury = 0
    injured_status = 0
    killed_status = 0
    injured_n = 0
    killed_n = 0
    for incident in data:
        incidents += 1
        injured_n += incident['n_injured']
        killed_n += incident['n_killed']

        if incident['participant_type'] is not None:
            for participant in incident['participant_type']:
                if incident['participant_type'][participant] == "Subject-Suspect":
                    suspects += 1
                if incident['participant_type'][participant] == "Victim":
                    victims += 1

        if incident['participant_status'] is not None:
            for participant in incident['participant_status']:
                if incident['participant_status'][participant] == "Injured":
                    injured_status += 1
                if incident['participant_status'][participant] == "Killed":
                    killed_status += 1

        if incident['participant_status'] is None:
            nones_val[0] += 1
            if incident['n_injured'] > 0 or incident['n_killed']:
                bad_nones_val[0] += 1

        if incident['participant_type'] is None:
            nones_val[1] += 1
            if incident['n_injured'] > 0 or incident['n_killed']:
                bad_nones_val[1] += 1

        if incident['n_injured'] == 0 and incident['n_killed'] == 0:
            incidents_with_no_victim += 1
    
        if incident['n_injured'] > 0 or incident['n_killed'] > 0:
            incidents_with_victim += 1
            if incident['n_injured'] > 0 and incident['n_killed'] == 0:
                incidents_with_injury += 1
            if incident['n_killed'] > 0 and incident['n_injured'] == 0:
                incidents_with_kill += 1
            if incident['n_injured'] > 0 and incident['n_killed'] > 0:
                incidents_with_kill_and_injury += 1
    
    varias = [incidents, incidents_with_no_victim, incidents_with_kill, incidents_with_injury, incidents_with_kill_and_injury, incidents_with_victim, victims, suspects, injured_status, killed_status, injured_n, killed_n, nones_val]
    varss = ["incidents", "incidents_with_no_victim", "incidents_with_kill", "incidents_with_injury", "incidents_with_kill_and_injury", "incidents_with_victim", "victims", "suspects", "injured_status", "killed_status", "injured_n", "killed_n", "nones_val"]
    i = 0
    # for var in varias:
    #     print(varss[i], "\t \t", var)
    #     i +=1
    return incidents_with_no_victim, incidents_with_kill, incidents_with_injury, incidents_with_kill_and_injury

def plot_victims_status(incidents_with_no_victim, incidents_with_kill, incidents_with_injury, incidents_with_kill_and_injury):
    from bokeh.io import output_file
    output_file("victim_status.html")
    years = ["all"]
    types = ['no one hurt', 'injured victim(s)', 'killed victim(s)', 'victim(s) killed and injured']
    colors = ["#c9d9d3", "#718dbf", "#e84d60", "#624F6D"]

    data = {'years': years,
            'no one hurt' : [incidents_with_no_victim],
            'injured victim(s)' : [incidents_with_injury],
            'killed victim(s)' : [incidents_with_kill],
            'victim(s) killed and injured' : [incidents_with_kill_and_injury] 
            }

    source = ColumnDataSource(data=data)

    p = figure(x_range=years, plot_height=650, plot_width=400, title="Verdeling van victims ofzo",
           toolbar_location=None, tools="")


    renderers = p.vbar_stack(types, x='years', width=0.9, color=colors, source=source,
                         legend=[value(x) for x in types], name=types)
    for r in renderers:
        typen = r.name
        hover = HoverTool(tooltips=[
            ("%s total" % typen, "@%s" % typen)], renderers=[r])
        p.add_tools(hover)

    p.y_range.start = 0
    p.x_range.range_padding = 0.3
    p.xgrid.grid_line_color = None
    p.axis.minor_tick_line_color = None
    p.outline_line_color = None
    p.legend.location = "top_left"
    p.legend.orientation = "horizontal"

    show(p)
    return None



def injuries_kill_year(data):
    years = [str(x) for x in range(2013,2019)]
    injuries, killings = injured_killed(years, data)
    data = dicts_format(injuries, killings, years)
    plot_injuries_kill_year(data, years)

def victim_status(data):
    incidents_with_no_victim, incidents_with_kill, incidents_with_injury, incidents_with_kill_and_injury = count_stuff(data)
    plot_victims_status(incidents_with_no_victim, incidents_with_kill, incidents_with_injury, incidents_with_kill_and_injury)

def childs_incidents(data):
    childs_incidents = ["Child Involved Incident", "Child injured (not child shooter)", 
                    "Child injured by child", "Child injured self", "Child killed (not child shooter)",
                    "Child killed by child", "Child killed self", "Child picked up & fired gun", "Child with gun - no shots fired"]

    dicciedict = {}

    for child_inc in childs_incidents:
        dicciedict[child_inc] = 0

    child_involved_incident = 0
    all_child_inc = 0
    for incident in data:
        if incident['incident_characteristics']:
            if [child_inc for child_inc in incident['incident_characteristics'] if child_inc in childs_incidents]:
                #print(incident['incident_characteristics'])
                all_child_inc += 1
                if 'Child Involved Incident' in incident['incident_characteristics']:
                    child_involved_incident += 1

    #print(all_child_inc, child_involved_incident)


    for incident in data:
        if incident['incident_characteristics']:
            if "Child Involved Incident" in incident['incident_characteristics']:
                l = [child_inc for child_inc in incident['incident_characteristics'] if child_inc in childs_incidents]
                for child_inc in l:
                    dicciedict[child_inc] += 1
                #print(incident['incident_characteristics'], incident['participant_age'])

    #print(dicciedict)


    from bokeh.io import show, output_file
    output_file("bar_colors.html")

    counts = []
    for child_inc in childs_incidents:
        counts.append(dicciedict[child_inc])

    fruits = childs_incidents
    print(childs_incidents)

    colors = ["#c9d9d3", "#718dbf", "#e84d60", "#624F6D","#c9d9d3", "#718dbf", "#e84d60", "#624F6D", "#c9d9d3"]

    source = ColumnDataSource(data=dict(fruits=fruits, counts=counts, color=colors))

    p = figure(x_range=fruits, y_range=(0,max(counts)+400), plot_height=800, plot_width=1600, title="Fruit Counts",
               toolbar_location=None, tools="")

    p.vbar(x='fruits', top='counts', width=0.9, color='color', legend="fruits", source=source)

    p.xgrid.grid_line_color = None
    p.legend.orientation = "horizontal"
    p.legend.location = "top_center"

    show(p)

def categories_occurence(data): 
    categories = []
    with open('list_categories.txt') as f:
        for line in f:
            categories.append(line.rstrip())


    dicciedict = {}

    for cat in categories:
        dicciedict[cat] = 0

    #if [child_inc for child_inc in characteristics if child_inc in childs_incidents]

    for incident in data:
        if incident['incident_characteristics']:
            for inc in incident['incident_characteristics']:
                dicciedict[inc] += 1

    from bokeh.io import output_file
    output_file("categories_occurence.html")

    counts = []
    for cat in categories:
        counts.append(dicciedict[cat])



    c = "#c9d9d3"
    colors = []
    for x in range(len(categories)):
        colors.append(c)

    #colors = ["#c9d9d3", "#718dbf", "#e84d60", "#624F6D","#c9d9d3", "#718dbf", "#e84d60", "#624F6D", "#c9d9d3"]

    source = ColumnDataSource(data=dict(categories=categories, counts=counts, color=colors))

    p = figure(x_range=categories, y_range=(0,max(counts)+400), plot_height=800, plot_width=1600, title="Fruit Counts",
               toolbar_location=None, tools="")

    p.vbar(x='categories', top='counts', width=0.9, color='color', legend="categories", source=source)

    p.xgrid.grid_line_color = None
    p.xaxis.major_label_orientation = math.pi/2
    p.legend.orientation = "horizontal"
    p.legend.location = "top_center"

    show(p)



def main():
    with open('gunfire.json') as f:
        data = json.load(f)

    #injuries_kill_year(data)
    #victim_status(data)
    #childs_incidents(data)
    categories_occurence(data)
    return None

main()






