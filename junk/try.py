from bokeh.core.properties import value
from bokeh.models import ColumnDataSource, HoverTool
from bokeh import plotting
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, FactorRange, CategoricalColorMapper, HoverTool, ColumnDataSource, Panel
from bokeh.plotting import figure
from bokeh.palettes import Category20_16
from bokeh.io import show, output_notebook, push_notebook, output_file, save
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

#output_notebook()
#output_file("plswork.html")


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
        variables = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
        name = 'month'
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
        
        for_category = pd.DataFrame(columns=['proportion', 'x', 
                                           'f_proportion', 'f_interval',
                                           'name', 'color'])
        range_extent = range_end - range_start
        
        # Iterate through all the carriers
        i = 0
        for category in categories:
            #GET THESE PERCENTAGES FROM generate file
            arr_hist = np.array(get_percentages(category))
            edges = np.array([x for x in range(1, len(arr_hist)+1)])

            # Divide the counts by the total to get a proportion and create df
            arr_df = pd.DataFrame({'proportion': arr_hist, 
                                   'x': edges})

            # Format the proportion 
            arr_df['f_proportion'] = ['%0.5f' % proportion for proportion in arr_df['proportion']]

            # Format the interval
            arr_df['f_interval'] = ['%d years' % x for x in 
                                    arr_df['x']]

            # Assign the carrier for labels
            arr_df['name'] = category

            # Color each carrier differently
            arr_df['color'] = Category20_16[i]
            if i == 15:
                i = 0

            # Add to the overall dataframe
            for_category = for_category.append(arr_df)
            i += 1
        # Overall dataframe
        for_category = for_category.sort_values(['name', 'x'])
        
        # Convert dataframe to column data source
        return ColumnDataSource(for_category)
        
    def make_plot(src):
        # Blank plot with correct labels
        p = figure(plot_width = 700, plot_height = 700, 
                  title = 'Suspects ',
                  x_axis_label = 'Age (years)', y_axis_label = 'Proportion')

        # Quad glyphs to create a histogram
        p.quad(source = src, bottom = 0, top = 'proportion', x = 'x', right = 'right',
               color = 'color', fill_alpha = 0.6, hover_fill_color = 'color', legend = 'name',
               hover_fill_alpha = 1.0, line_color = 'black')

        p.vbar(x=[1, 2, 3], width=0.5, bottom=0,
               top=[1.2, 2.5, 3.7], color="firebrick")

        # Hover tool with vline mode
        hover = HoverTool(tooltips=[('Category', '@name'), 
                                    ('Age', '@f_interval'),
                                    ('Proportion', '@f_proportion')],
                          mode='vline')

        p.add_tools(hover)
        
        p.legend.click_policy = 'hide'

        # Styling
        p = style(p)

        return p
    
    # Update function takes three default parameters
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
        variables = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
        name = 'month'
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
        
        for_category = pd.DataFrame(columns=['proportion', 'x', 'right', 
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
                                   'x': edges[:-1], 'right': edges[1:] })

            # Format the proportion 
            arr_df['f_proportion'] = ['%0.5f' % proportion for proportion in arr_df['proportion']]

            # Format the interval
            arr_df['f_interval'] = ['%d years' % x for x in 
                                    arr_df['x']]

            # Assign the carrier for labels
            arr_df['name'] = category

            # Color each carrier differently
            arr_df['color'] = Category20_16[i]
            if i == 15:
                i = 0

            # Add to the overall dataframe
            for_category = for_category.append(arr_df)
            i += 1
        # Overall dataframe
        for_category = for_category.sort_values(['name', 'x'])
        
        # Convert dataframe to column data source
        return ColumnDataSource(for_category)
        
    def make_plot(src):
        # Blank plot with correct labels
        p = figure(plot_width = 700, plot_height = 700, 
                  title = 'Suspects ',
                  x_axis_label = 'Age (years)', y_axis_label = 'Proportion')

        # Quad glyphs to create a histogram
        p.quad(source = src, bottom = 0, top = 'proportion', x = 'x', right = 'right',
               color = 'color', fill_alpha = 0.6, hover_fill_color = 'color', legend = 'name',
               hover_fill_alpha = 1.0, line_color = 'black')


        # Hover tool with vline mode
        hover = HoverTool(tooltips=[('Category', '@name'), 
                                    ('Age', '@f_interval'),
                                    ('Proportion', '@f_proportion')],
                          mode='vline')

        p.add_tools(hover)
        
        p.legend.click_policy = 'hide'

        # Styling
        p = style(p)

        return p
    
    # Update function takes three default parameters
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
#show(app)


''' Present a scatter plot with linked histograms on both axes.
Use the ``bokeh serve`` command to run the example by executing:
    bokeh serve selection_histogram.py
at your command prompt. Then navigate to the URL
    http://localhost:5006/selection_histogram
in your browser.

import numpy as np

from bokeh.layouts import row, column
from bokeh.models import BoxSelectTool, LassoSelectTool, Spacer
from bokeh.plotting import figure, curdoc

# create three normal population samples with different parameters
x1 = np.random.normal(loc=5.0, size=400) * 100
y1 = np.random.normal(loc=10.0, size=400) * 10

x2 = np.random.normal(loc=5.0, size=800) * 50
y2 = np.random.normal(loc=5.0, size=800) * 10

x3 = np.random.normal(loc=55.0, size=200) * 10
y3 = np.random.normal(loc=4.0, size=200) * 10

x = np.concatenate((x1, x2, x3))
y = np.concatenate((y1, y2, y3))

TOOLS="pan,wheel_zoom,box_select,lasso_select,reset"

# create the scatter plot
p = figure(tools=TOOLS, plot_width=600, plot_height=600, min_border=10, min_border_left=50,
           toolbar_location="above", x_axis_location=None, y_axis_location=None,
           title="Linked Histograms")
p.background_fill_color = "#fafafa"
p.select(BoxSelectTool).select_every_mousemove = False
p.select(LassoSelectTool).select_every_mousemove = False

r = p.scatter(x, y, size=3, color="#3A5785", alpha=0.6)

# create the horizontal histogram
hhist, hedges = np.histogram(x, bins=20)
hzeros = np.zeros(len(hedges)-1)
hmax = max(hhist)*1.1

LINE_ARGS = dict(color="#3A5785", line_color=None)

ph = figure(toolbar_location=None, plot_width=p.plot_width, plot_height=200, x_range=p.x_range,
            y_range=(-hmax, hmax), min_border=10, min_border_left=50, y_axis_location="right")
ph.xgrid.grid_line_color = None
ph.yaxis.major_label_orientation = np.pi/4
ph.background_fill_color = "#fafafa"

ph.quad(bottom=0, left=hedges[:-1], right=hedges[1:], top=hhist, color="white", line_color="#3A5785")
hh1 = ph.quad(bottom=0, left=hedges[:-1], right=hedges[1:], top=hzeros, alpha=0.5, **LINE_ARGS)
hh2 = ph.quad(bottom=0, left=hedges[:-1], right=hedges[1:], top=hzeros, alpha=0.1, **LINE_ARGS)

# create the vertical histogram
vhist, vedges = np.histogram(y, bins=20)
vzeros = np.zeros(len(vedges)-1)
vmax = max(vhist)*1.1

pv = figure(toolbar_location=None, plot_width=200, plot_height=p.plot_height, x_range=(-vmax, vmax),
            y_range=p.y_range, min_border=10, y_axis_location="right")
pv.ygrid.grid_line_color = None
pv.xaxis.major_label_orientation = np.pi/4
pv.background_fill_color = "#fafafa"

pv.quad(left=0, bottom=vedges[:-1], top=vedges[1:], right=vhist, color="white", line_color="#3A5785")
vh1 = pv.quad(left=0, bottom=vedges[:-1], top=vedges[1:], right=vzeros, alpha=0.5, **LINE_ARGS)
vh2 = pv.quad(left=0, bottom=vedges[:-1], top=vedges[1:], right=vzeros, alpha=0.1, **LINE_ARGS)

layout = column(row(p, pv), row(ph, Spacer(width=200, height=200)))

curdoc().add_root(layout)
curdoc().title = "Selection Histogram"

def update(attr, old, new):
    inds = np.array(new['1d']['indices'])
    if len(inds) == 0 or len(inds) == len(x):
        hhist1, hhist2 = hzeros, hzeros
        vhist1, vhist2 = vzeros, vzeros
    else:
        neg_inds = np.ones_like(x, dtype=np.bool)
        neg_inds[inds] = False
        hhist1, _ = np.histogram(x[inds], bins=hedges)
        vhist1, _ = np.histogram(y[inds], bins=vedges)
        hhist2, _ = np.histogram(x[neg_inds], bins=hedges)
        vhist2, _ = np.histogram(y[neg_inds], bins=vedges)

    hh1.data_source.data["top"]   =  hhist1
    hh2.data_source.data["top"]   = -hhist2
    vh1.data_source.data["right"] =  vhist1
    vh2.data_source.data["right"] = -vhist2

r.data_source.on_change('selected', update)


'''