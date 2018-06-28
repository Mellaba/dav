from bokeh.core.properties import value
from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, FactorRange
from bokeh.plotting import figure
from bokeh.transform import factor_cmap
from bokeh.palettes import Spectral5
from bokeh import plotting
from bokeh.palettes import Category20_16
from bokeh.models.widgets import CheckboxGroup

from bokeh.io import show, output_notebook, push_notebook
from bokeh.plotting import figure

from bokeh.models import CategoricalColorMapper, HoverTool, ColumnDataSource, Panel
from bokeh.models.widgets import CheckboxGroup, Slider, RangeSlider, Tabs

from bokeh.layouts import column, row, WidgetBox
from bokeh.palettes import Category20_16

from bokeh.application.handlers import FunctionHandler
from bokeh.application import Application


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


def modify_doc(doc):

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
            p.plot_width = 2000
            return p

    def get_percentages(cat):
        variables = [str(x) for x in range(100)]
        name = 'age'
        values_s = []
        values_v = []
        for var in variables:
            values_s.append(cat_data[cat]['suspect'][name][var])
            values_v.append(cat_data[cat]['victim'][name][var])
        percentages_s = []
        #percentages_v = []
        if sum(values_s) == 0:
            percentages_s = [x for x in values_s]
        # if sum(values_v) == 0:
        #     percentages_v = [x for x in values_v]
        if sum(values_s) != 0:
            percentages_s = [x/float(sum(values_s)) for x in values_s]
        # if sum(values_v) != 0:
        #     percentages_v = [x/float(sum(values_v)) for x in values_v]
        return percentages_s

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
            arr_df['f_interval'] = ['%d to %d years' % (left, right) for left, 
                                    right in zip(arr_df['left'], arr_df['right'])]

            # Assign the carrier for labels
            arr_df['name'] = category

            # Color each carrier differently
            print(Category20_16[i], i)
            arr_df['color'] = Category20_16[i]
            if i == 15:
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
        p = figure(plot_width = 700, plot_height = 700, 
                  title = 'Histogram of Arrival Delays by Carrier',
                  x_axis_label = 'Delay (min)', y_axis_label = 'Proportion')

        # Quad glyphs to create a histogram
        p.quad(source = src, bottom = 0, top = 'proportion', left = 'left', right = 'right',
               color = 'color', fill_alpha = 0.7, hover_fill_color = 'color', legend = 'name',
               hover_fill_alpha = 1.0, line_color = 'black')

        # Hover tool with vline mode
        hover = HoverTool(tooltips=[('Carrier', '@name'), 
                                    ('Delay', '@f_interval'),
                                    ('Proportion', '@f_proportion')],
                          mode='vline')

        p.add_tools(hover)
        
        p.legend.click_policy = 'hide'

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
                               range_start = -60,
                               range_end = 120,
                               bin_width = 5)

        # Update the source used the quad glpyhs
        src.data.update(new_src.data)

        
    category_selection = CheckboxGroup(labels=categories, active = [0, 1])
    category_selection.on_change('active', update)
    
    controls = WidgetBox(category_selection)
    
    initial_categories = [category_selection.labels[i] for i in category_selection.active]
    
    src = make_dataset(initial_categories,
                      range_start = -60,
                      range_end = 120,
                      bin_width = 5)
    
    p = make_plot(src)
    
    layout = row(controls, p)
    doc.add_root(layout)
    
# Set up an application
handler = FunctionHandler(modify_doc)
app = Application(handler)
show(app)