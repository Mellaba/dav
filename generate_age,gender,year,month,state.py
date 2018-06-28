from bokeh.core.properties import value
from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, FactorRange
from bokeh.plotting import figure
from bokeh.transform import factor_cmap
from bokeh.palettes import Spectral5
from bokeh import plotting

from numpy import pi
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import math
import re
import itertools


def dict_categories():
    '''create formatted selection of categories from external file 
        { main_cat : [main_cat, sub_cat1, sub_cat2...] }'''
    categories = {}
    dont_add = ['Raids', 'Gun at school', 'Mass Problem']
    with open('list_categories.txt', 'r+') as f:
        lines = f.readlines()
        for i in range(0, len(lines)):
            if "\t" in lines[i]:
                continue
            line = lines[i].rstrip()
            if line in dont_add:
                categories[line] = []
            else: categories[line] = [line]
            if i+1 < len(lines):
                while "\t" in lines[i+1]:            
                    i += 1
                    categories[line].append(re.split("\t", lines[i])[1].rstrip())
    return categories

def map_to_cat(categories):
    ''' map subcategories back to their main category'''
    map_to_cat = {}
    for main_cat in categories:
        for sub_cat in categories[main_cat]:
            map_to_cat[sub_cat] = main_cat
    return map_to_cat

def add_to_dict(cat_data, vals, susp_vic, main_cat):
    ''' add +1 count for variables in dictionary 
        vb. for cat='Domestic violence' var='age' val='21' +1  '''
    var = ['gender', 'age', 'state', 'year', 'month']
    i = 0
    for val in vals:
        if val in cat_data[main_cat][susp_vic][var[i]]:
            cat_data[main_cat][susp_vic][var[i]][val] += 1
        else:
            cat_data[main_cat][susp_vic][var[i]][val] = 1
        i += 1
    return cat_data

def get_values(incident, columns, typ):
    ''' return list of found types per variables
        # gender, age, state, date, month
        e.g. ['Male', '21', 'Ohio', '2014', '02']'''
    var = []   
    if incident['participant_gender']:
        var.append(incident['participant_gender'].get(typ))
    if not incident['participant_gender']:
        var.append("None")
    if incident['participant_age']:
        var.append(incident['participant_age'].get(typ))
    if not incident['participant_age']:
        var.append("None")
    if incident['state']:
        var.append(incident['state'])
    if not incident['state']:
        var.append("None")
    if incident['date']:
        var.append(incident['date'][0])
        var.append(incident['date'][1])
    if not incident['date']:
        var.append("None")
        var.append("None")
    return var[0], var[1], var[2], var[3], var[4]



def count_categories(states, ofile):
    '''From gunfire.json, collect counts of category occurence and store in dict'''

    with open(ofile) as f:
        data = json.load(f)

    categories = dict_categories()
    map_to_c = map_to_cat(categories)

    cat_data = {}

    main_cats = list(categories.keys())

    for cat in main_cats:
        cat_data[cat] = {}

    # initialize dict structure and keys
    for cat in cat_data:
        cat_data[cat] = {
                                "suspect" : {"gender" : {"Male" : 0, "Female" : 0, "None": 0} , 
                                            "age" : {"None" : 0}, 
                                            "year" : {"2013": 0, "2014" : 0, "2015" : 0, "2016" : 0, "2017" : 0, "2018" : 0, "None":0}, 
                                            "state" : {"None" : 0} ,
                                            "month" : {"None" : 0} }, 
                                "victim" : {"gender" : {"Male" : 0, "Female" : 0, "None" : 0} , 
                                            "age" : {"None" : 0}, 
                                            "year" : {"2013": 0, "2014" : 0, "2015" : 0, "2016" : 0, "2017" : 0, "2018" : 0, "None":0}, 
                                            "state" : {"None" : 0} ,
                                            "month" : {"None" : 0} }
                            }
    
    # add age keys 
    for age in range(120):
        for cat_key in cat_data:
            cat_data[cat_key]["suspect"]["age"][str(age)] = 0
            cat_data[cat_key]["victim"]["age"][str(age)] = 0

    # add state keys
    for state in states:
        for cat_key in cat_data:
            cat_data[cat_key]["suspect"]["state"][str(state)] = 0
            cat_data[cat_key]["victim"]["state"][str(state)] = 0 

    # add month keys
    months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
    for month in months:
        for cat_key in cat_data:
            cat_data[cat_key]["suspect"]["month"][month] = 0
            cat_data[cat_key]["victim"]["month"][month] = 0 

    # main loop
    # for all incidents, count types of all variables per category
    for incident in data:
        if incident['incident_characteristics'] and incident['date']:
            if int(incident['date'][0]) > 2013:
                main_cats_used = []
                for char in incident['incident_characteristics']:
                    if char in map_to_c:
                        main_cat = map_to_c[char]
                        if main_cat not in main_cats_used:
                            main_cats_used.append(main_cat)
                            type_keys = []
                            if incident['participant_type']:
                                type_keys = list(incident['participant_type'].keys())
                            if type_keys:
                                for typ in type_keys:
                                    participant_type = incident['participant_type'][typ]
                                    if participant_type == "Subject-Suspect":
                                        gender, age, state, year, month = get_values(incident, ['participant_gender', 'participant_age'], typ)
                                        cat_data = add_to_dict(cat_data, [gender, age, state, year, month], 'suspect', main_cat)
                                    if participant_type == "Victim":
                                        gender, age, state, year, month = get_values(incident, ['participant_gender', 'participant_age'], typ)
                                        cat_data = add_to_dict(cat_data, [gender, age, state, year, month], 'victim', main_cat)
    return cat_data, main_cats, categories



def plot_per_cat(cat_data, main_cats, categories, variables, name, sus_vic):
    ''' for suspects/victims per category per age/gender/year/month/state 
        output barplot '''
    from bokeh.io import show, output_file

    out_f = "per_catergory_per_ %s,%ss,absolute.html"%(name, sus_vic)
    output_file(out_f)

    categories = [cat for cat in main_cats]

    data = {'categories' : categories }

    for var in variables:
        data[var] = [cat_data[cat][sus_vic][name][str(var)] for cat in main_cats]
    #palette = Spectral5
    palette = ["#c9d9d3" for x in range(len(main_cats) * len(variables))]
    x = [(cat, var) for cat in categories for var in variables ]
    counts = []
    for cat in categories:
        for var in variables:
            counts.append(cat_data[cat][sus_vic][name][var])

    title = "%s of %s by Category" %(sus_vic, name)
    source = ColumnDataSource(data=dict(x=x, counts=counts))
    p = figure(x_range=FactorRange(*x), plot_height=500, plot_width = 3000, title="title",
               toolbar_location=None, tools="")

    p.vbar(x='x', top='counts', width=0.9, source=source, line_color="white", fill_alpha=0.9,
           fill_color=factor_cmap('x', palette=palette, factors=variables, start=1, end=2))

    p.y_range.start = 0
    p.y_range.end = 0.5
    p.x_range.range_padding = 0.05
    p.legend.orientation = "vertical"
    p.xaxis.major_label_orientation = math.pi/2

    p.xgrid.grid_line_color = None
    show(p)

def divide_states_population():
    ''' return dict of {States : state_population} and list of State names'''
    with open('populationstate2017.txt', 'r+') as f:
        lines = f.readlines()
    state_population = {}
    states = []
    for i in range(0, len(lines)):
        l = lines[i].split(",")
        if l[0].title() != "District Of Columbia":
            state_population[l[0].title()] = l[1].rstrip()
            states.append(l[0].title())
        if  l[0].title() == "District Of Columbia":
            state_population["District of Columbia"] = l[1]
            states.append("District of Columbia")
    return state_population, states

def states_to_population(cat_data, main_cats):
    ''' devide total occurences of incidents per state by state population * 1000 '''
    state_population, _ = divide_states_population()
    for cat in main_cats:
        types = ['suspect', 'victim']
        for typ in types:
            for state in cat_data[cat][typ]['state']:
                if cat_data[cat][typ]['state'][state]:
                    cat_data[cat][typ]['state'][state] = ( cat_data[cat][typ]['state'][state]/float(state_population[state]) ) * 1000
    return cat_data


def normalize_plots(cat_data, states, main_cats, categories, all_variables, all_names):
    ''' per category, make proportions of each type instead of absolute counts 
        return dict with proportional values, and show plots'''
    normalize_cat = cat_data
    for variables, name in zip(all_variables, all_names):
        max_val = 0
        for cat in cat_data:
            values_s = []
            values_v = []
            for var in variables:
                values_s.append(cat_data[cat]['suspect'][name][var])
                values_v.append(cat_data[cat]['victim'][name][var])
            percentages_s = []
            percentages_v = []
            if sum(values_s) == 0:
                percentages_s = [x for x in values_s]
            if sum(values_v) == 0:
                percentages_v = [x for x in values_v]
            if sum(values_s) != 0:
                percentages_s = [x/float(sum(values_s)) for x in values_s]
            if sum(values_v) != 0:
                percentages_v = [x/float(sum(values_v)) for x in values_v]
            
            for i, var in enumerate(variables):
                normalize_cat[cat]['suspect'][name][var] = percentages_s[i]
                normalize_cat[cat]['victim'][name][var] = percentages_v[i]

  #  for variables, name in zip(all_variables, all_names):
 #       plot_per_cat(normalize_cat, main_cats, categories, variables, name, 'suspect')
#        plot_per_cat(normalize_cat, main_cats, categories, variables, name, 'victim')
    months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "None"]
    plot_per_cat(normalize_cat, main_cats, categories, months, 'month', 'suspect')
    plot_per_cat(normalize_cat, main_cats, categories, months, 'month', 'victim')

    return normalize_cat




def main():
    _, states = divide_states_population()
    cat_data, main_cats, categories = count_categories(states, 'gunfire.json')
    cat_data = states_to_population(cat_data, main_cats)

    np.save('my_file.npy', cat_data) 

    months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "None"]
    ages =  [str(x) for x in range(0,100)]
    ages.append("None")
    states.append("None")
    all_variables = [['2014', '2015', '2016', '2017', "None"], ['Male', 'Female', "None"], ages, states, months]
    all_names = ['year','gender','age','state', 'month']

    normal_cat_data = normalize_plots(cat_data, states, main_cats, categories, all_variables, all_names)

    # absolute counts plots

    #plot_per_cat(cat_data, main_cats, categories, states, 'state', 'suspect')
    #plot_per_cat(cat_data, main_cats, categories, states, 'state', 'victim')


    #for variables, name in zip(all_variables, all_names):
     #    plot_per_cat(cat_data, main_cats, categories, variables, name, 'suspect')
      #   plot_per_cat(cat_data, main_cats, categories, variables, name, 'victim')


main()