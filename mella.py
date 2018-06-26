import stategender as s
from bokeh.io import show, output_file

years = ['2014', '2015', '2016', '2017']

for year in years:
    plotinci = s.statesincident(year)
    output_file("gender_states_incidents" + year + ".html")
    show(plotinci)
    plotpercen = s.statespercentage(year)
    output_file("gender_states_percentages" + year + ".html")
    show(plotpercen)