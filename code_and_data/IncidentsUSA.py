''' This file creates a map of the USA with all points where have been gun incidents.
    Next to view all the incidents its possible to chose whate kind incident characterisic you want to view.
    Suicide, Gang involvement or/and Mass shootings.
'''

import json
from bokeh.plotting import figure, show, output_file
from bokeh.sampledata.us_states import data as states

def get_lat_lon(data, characteristic1, characteristic2, characteristic3, characteristic4):
    ''' Function returns the latitude and longitude of an incident.
        Also gets longitude and latitude of the characteristic incidents.
    '''
    lat1 = []
    lon1 = []
    lat2 = []
    lon2 = []
    lat3 = []
    lon3 = []
    lat4 = []
    lon4 = []
    for incident in data:
        lat = incident["latitude"]
        lon = incident["longitude"]
        if lat != None and lon != None:
            if lat < 50 and lat > 23 and lon > -128 and lon < -60:
                if incident["incident_characteristics"] and characteristic2 in incident["incident_characteristics"]:
                    lat2.append(lat)
                    lon2.append(lon)
                elif incident["incident_characteristics"] and characteristic3 in incident["incident_characteristics"]:
                    lat3.append(lat)
                    lon3.append(lon)
                elif incident["incident_characteristics"] and characteristic4 in incident["incident_characteristics"]:
                    lat4.append(lat)
                    lon4.append(lon)

                lat1.append(lat)
                lon1.append(lon)
                
    return [(lat1, lon1), (lat2, lon2), (lat3, lon3), (lat4, lon4)]

def create_map(d):
    ''' Gets coordinates of all states of America except for states Alaska and Hawaii.
    '''

    del states["HI"]
    del states["AK"]        

    state_xs = [states[code]["lons"] for code in states]
    state_ys = [states[code]["lats"] for code in states]

    return [state_xs, state_ys]

def plot(state_map, coords, characteristics):
    ''' Plots all the found points on the map.
    ''' 

    p = figure(title="US map plot", toolbar_location="left",plot_width=850, plot_height=550)
    p.patches(state_map[0], state_map[1], fill_alpha=0.0,
            line_color="#884444", line_width=2, line_alpha=0.3)

    p.circle(x=coords[0][1], y=coords[0][0], size=3, fill_color="blue", line_color=None, fill_alpha=0.8, legend="All incidents")
    p.circle(x=coords[1][1], y=coords[1][0], size=3, fill_color="red", line_color=None, fill_alpha=0.8, legend="Suicide")
    p.circle(x=coords[2][1], y=coords[2][0], size=3, fill_color="green", line_color=None, fill_alpha=0.8, legend=characteristics[2])
    p.circle(x=coords[3][1], y=coords[3][0], size=3, fill_color="orange", line_color=None, fill_alpha=0.8, legend="Mass shooting")

    p.grid.grid_line_color = None
    p.legend.location = "bottom_left"
    p.legend.click_policy= "hide"

    file_name = "map_incidents.html"
    output_file(file_name, title="USAMAP.py example")
    show(p)

def main():

    with open('gunfire.json') as f:
        d = json.load(f)
    characteristics = [0, "Suicide^", "Gang involvement", "Mass Shooting (4+ victims injured or killed excluding the subject/suspect/perpetrator, one location)"]
    state_map = create_map(d)
    coords = get_lat_lon(d, characteristics[0], characteristics[1], characteristics[2], characteristics[3])
    plot(state_map, coords, characteristics)

if __name__ == "__main__":
    main()
