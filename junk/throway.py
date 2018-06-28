# a copy of lisatryouts3 that works to the point of plotting all categories at once


from bokeh.core.properties import value
from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, FactorRange
from bokeh.plotting import figure
from bokeh.transform import factor_cmap
from bokeh.palettes import Spectral5
from bokeh import plotting
from bokeh.palettes import Spectral5
from bokeh.models.widgets import CheckboxGroup


from numpy import pi
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import math
import re
import itertools


# # Load
# generate and save data from generate file. Save it with logical filename
cat_data = np.load('my_file.npy').item()
categories = list(cat_data.keys())

category_selection = CheckboxGroup(labels=categories, 
                              active = [0, 1])

# Select the airlines names from the selection values
[category_selection.labels[i] for i in category_selection.active]
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

def style(p):
        # Title 
        p.title.align = 'center'
        p.title.text_font_size = '20pt'
        p.title.text_font = 'serif'

        # Axis titles
        p.xaxis.axis_label_text_font_size = '14pt'
        p.xaxis.axis_label_text_font_style = 'bold'
        p.yaxis.axis_label_text_font_size = '14pt'
        p.yaxis.axis_label_text_font_style = 'bold'

        # Tick labels
        p.xaxis.major_label_text_font_size = '12pt'
        p.yaxis.major_label_text_font_size = '12pt'

        #other
        p.plot_width = 950
        p.plot_height = 450
        return p


def get_percentages(cat):
    _, states = divide_states_population()
    variables =  [str(x) for x in range(0,100)] # ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "None"] #states
    name = 'age'
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
    return percentages_v

def make_dataset(categories, range_start = 0, range_end = 100, bin_width = 1):

    # Check to make sure the start is less than the end!
    assert range_start < range_end, "Start must be less than end!"
    
    for_category = pd.DataFrame(columns=['proportion', 'left', 'right', 
                                       'f_proportion', 'f_interval',
                                       'name', 'color'])
    range_extent = range_end - range_start
    
    # Iterate through all the carriers
    i = 0
    for category in categories:
        #GET THESE PERCENTAGES FROM generate file
        arr_hist = np.array(get_percentages(category))
        edges = np.array([x for x in range(len(arr_hist)+1)])

        # Divide the counts by the total to get a proportion and create df
        arr_df = pd.DataFrame({'proportion': arr_hist, 
                               'left': edges[:-1], 'right': edges[1:] })

        # Format the proportion 
        arr_df['f_proportion'] = ['%0.5f' % proportion for proportion in arr_df['proportion']]

        # Format the interval
        arr_df['f_interval'] = ['%d years' % left for left in arr_df['left']]

        # Assign the carrier for labels
        arr_df['name'] = category

        # Color each carrier differently
        #print(Category20c[i], i)
        colors = ['#225ea8', '#41b6c4', '#a1dab4', '#ffffcc']
        arr_df['color'] = Spectral5[i]
        if i == 3:
            print("i", i)
            i = 0

        # Add to the overall dataframe
        for_category = for_category.append(arr_df)
        i += 1
    # Overall dataframe
    for_category = for_category.sort_values(['name', 'left'])
    print(for_category.head())
    
    # Convert dataframe to column data source
    return ColumnDataSource(for_category)





def make_plot(src):
    # Blank plot with correct labels
    p = figure(plot_width = 20, plot_height = 500, 
              title = 'Age of suspect by incident category',
              x_axis_label = 'Age (years)', y_axis_label = 'Proportion')

    # Quad glyphs to create a histogram
    p.quad(source = src, bottom = 0, top = 'proportion', left = 'left', right = 'right',
           color = 'color', fill_alpha = 0.8, hover_fill_color = 'color', legend = 'name',
           hover_fill_alpha = 1.0, line_color = 'black')

    # Hover tool with vline mode
    hover = HoverTool(tooltips=[('Category', '@name'), 
                                ('Age', '@f_interval'),
                                ('Proportion', '@f_proportion')],
                      mode='vline')

    p.add_tools(hover)
    # Styling
    p = style(p)

    return p 


# Update function takes three default parameters
def update(attr, old, new):
    # Get the list of carriers for the graph
    categories_to_plot = [category_selection.labels[i] for i in 
                        category_selection.active]

    # Make a new dataset based on the selected carriers and the 
    # make_dataset function defined earlier
    new_src = make_dataset(categories_to_plot,
                           range_start = 0,
                           range_end = 100,
                           bin_width = 0.1)

    # Update the source used in the quad glpyhs
    src.data.update(new_src.data)    


def main():
    from bokeh.io import show, output_file
    src = make_dataset(categories)
    p = make_plot(src)
    output_file("ages_victim.html")
    show(p)
    




main()