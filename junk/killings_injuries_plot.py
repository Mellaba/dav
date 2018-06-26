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

    p = figure(x_range=years, plot_height=350, title="Verdeling van victims ofzo",
           toolbar_location=None, tools="")


    renderers = p.vbar_stack(types, x='years', width=0.9, color=colors, source=source,
                         legend=[value(x) for x in types], name=types)
    for r in renderers:
        typen = r.name
        hover = HoverTool(tooltips=[
            ("%s total" % typen, "@%s" % typen)], renderers=[r])
        p.add_tools(hover)

    p.y_range.start = 0
    p.x_range.range_padding = 0.1
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



def main():
    with open('gunfire.json') as f:
        data = json.load(f)

    injuries_kill_year(data)
    victim_status(data)
    return None

main()






