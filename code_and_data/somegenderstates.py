import stategender as s
from bokeh.io import show, output_file

interestingstates = ['Illinois', 'District of Columbia', 'Minnesota']
thisthing = s.somestate(interestingstates)
show(thisthing)