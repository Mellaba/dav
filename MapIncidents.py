# from geopy.geocoders import Nominatim
import json

from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource, LogColorMapper
# from bokeh.palettes import Viridis6 as palette

from bokeh.sampledata.us_counties import data as counties
from bokeh.sampledata.us_states import data as states

with open('gunfire.json') as f:
	    data = json.load(f)

longtitude = []
latitude = []
for incident in data:
    if incident["latitude"] != None and incident["longitude"] != None:
        if incident["latitude"] < 50 and incident["latitude"] > 23 and incident["longitude"] > -128 and incident["longitude"] < -60:
            latitude.append(incident["latitude"])
            longtitude.append(incident["longitude"])

del states["HI"]
del states["AK"]

EXCLUDED = ("ak", "hi", "pr", "gu", "vi", "mp", "as")

state_xs = [states[code]["lons"] for code in states]
state_ys = [states[code]["lats"] for code in states]

county_xs=[counties[code]["lons"] for code in counties if counties[code]['state'] not in EXCLUDED]
county_ys=[counties[code]["lats"] for code in counties if counties[code]['state'] not in EXCLUDED]

source=ColumnDataSource(data=dict(lat=latitude,
                                    lon=longtitude))

p = figure(title="US map plot", toolbar_location="left",plot_width=1100, plot_height=700)


p.circle(x="lon", y="lat", size=5, fill_color="blue", fill_alpha=0.8, source=source)
p.patches(county_xs, county_ys, fill_color="white", fill_alpha=0.7,
          line_color="gray", line_width=0.5)

p.patches(state_xs, state_ys, fill_alpha=0.0,
          line_color="#884444", line_width=2, line_alpha=0.3)

output_file("USAMAP.html", title="USAMAP.py example")
show(p)
