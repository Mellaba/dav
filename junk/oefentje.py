def make_dataset(carrier_list, range_start = -60, range_end = 120, bin_width = 5):

    # Check to make sure the start is less than the end!
    assert range_start < range_end, "Start must be less than end!"
    
    by_carrier = pd.DataFrame(columns=['proportion', 'left', 'right', 
                                       'f_proportion', 'f_interval',
                                       'name', 'color'])
    range_extent = range_end - range_start
    
    # Iterate through all the carriers
    for i, carrier_name in enumerate(carrier_list):

        # Subset to the carrier
        subset = flights[flights['name'] == carrier_name]

        # Create a histogram with specified bins and range
        arr_hist, edges = np.histogram(subset['arr_delay'], 
                                       bins = int(range_extent / bin_width), 
                                       range = [range_start, range_end])

        # Divide the counts by the total to get a proportion and create df
        arr_df = pd.DataFrame({'proportion': arr_hist / np.sum(arr_hist), 
                               'left': edges[:-1], 'right': edges[1:] })

        # Format the proportion 
        arr_df['f_proportion'] = ['%0.5f' % proportion for proportion in arr_df['proportion']]

        # Format the interval
        arr_df['f_interval'] = ['%d to %d minutes' % (left, right) for left, 
                                right in zip(arr_df['left'], arr_df['right'])]

        # Assign the carrier for labels
        arr_df['name'] = carrier_name

        # Color each carrier differently
        arr_df['color'] = Category20_16[i]

        # Add to the overall dataframe
        by_carrier = by_carrier.append(arr_df)

    # Overall dataframe
    by_carrier = by_carrier.sort_values(['name', 'left'])
    
    # Convert dataframe to column data source
    return ColumnDataSource(by_carrier)

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

        # Styling
        p = style(p)

        return p 

from bokeh.models.widgets import CheckboxGroup
# Create the checkbox selection element, available carriers is a  
# list of all airlines in the data
carrier_selection = CheckboxGroup(labels=available_carriers, 
                                  active = [0, 1])

# Select the airlines names from the selection values
[carrier_selection.labels[i] for i in carrier_selection.active]
['AirTran Airways Corporation', 'Alaska Airlines Inc.']

# Update function takes three default parameters
def update(attr, old, new):
    # Get the list of carriers for the graph
    carriers_to_plot = [carrier_selection.labels[i] for i in 
                        carrier_selection.active]
    # Make a new dataset based on the selected carriers and the 
    # make_dataset function defined earlier
    new_src = make_dataset(carriers_to_plot,
                           range_start = -60,
                           range_end = 120,
                           bin_width = 5)
    # Update the source used in the quad glpyhs
    src.data.update(new_src.data)

# Link a change in selected buttons to the update function
carrier_selection.on_change('active', update)