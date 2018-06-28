from bokeh.core.properties import value
from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.transform import dodge
from bokeh.layouts import gridplot
from bokeh.layouts import column
import json
import math

def somestate(thestates):
    with open('gunfire.json') as f:
        data = json.load(f)

    listyears = ['2014', '2015', '2016', '2017']

    states2 = {}
    for incident in data:
        yeartje = incident["date"][0]
        if yeartje in listyears:
            genders = incident["participant_gender"]
            victims = incident["participant_type"]
            state = incident["state"]
            if genders == None or victims == None or state == None:
                continue
            if state not in states2:
                states2[state] = {'Male suspect': 0, 'Female suspect': 0, 'Male victim':0, 'Female victim':0}
            for key in genders:
                gender = genders.get(key)
                thetype = victims.get(key)
                if gender == 'Male' and thetype == 'Subject-Suspect':
                    states2[state]['Male suspect'] += 1
                elif gender == 'Female' and thetype == 'Subject-Suspect':
                    states2[state]['Female suspect'] += 1
                elif gender == 'Male' and thetype == 'Victim':
                    states2[state]['Male victim'] += 1
                elif gender == 'Female' and thetype == 'Victim':
                    states2[state]['Female victim'] += 1
   
    statelist = []
    countlist = []
    with open('populationstate2017.txt') as s:
        temp = s.read().splitlines()
        for elem in temp:
            state, amount = elem.split(',')
            statelist.append(state)
            countlist.append(amount)


    howmanystates = 0
    allbitches = {'Male suspect': 0, 'Female suspect': 0, 'Male victim': 0, 'Female victim': 0}
    for state in states2:
        indexnum = int(statelist.index(state))
        howmanystates += 1
        for key in state:
            allbitches['Male suspect'] += (int(states2[state].get('Male suspect'))/((int(countlist[indexnum]))*4))*10000
            allbitches['Male victim'] += (int(states2[state].get('Male victim'))/((int(countlist[indexnum]))*4))*10000
            allbitches['Female suspect'] += (int(states2[state].get('Female suspect'))/((int(countlist[indexnum]))*4))*10000
            allbitches['Female victim'] += (int(states2[state].get('Female victim'))/((int(countlist[indexnum]))*4))*10000
    for key in allbitches:
        allbitches[key] = (allbitches[key]/howmanystates)
        
    states2['Average'] = allbitches
    thestates.append('Average')


    for iets in statelist:
        indexnum = int(statelist.index(iets))
        for key in states2[iets]:
            howmany = int(states2[iets].get(key))
            standardized = (howmany/(int(countlist[indexnum])*4))*100000
            states2[iets][key] = standardized

    sort = sorted(thestates)

    fruits2 = [key for key in sort]

    data = {'fruits2' : fruits2,
            'Male Victim'   : [states2[key]['Male victim'] for key in sort],
            'Male Suspect'   : [states2[key]['Male suspect'] for key in sort],
            'Female Victim' : [states2[key]['Female victim'] for key in sort],
            'Female Suspect' : [states2[key]['Female suspect'] for key in sort]}

    source = ColumnDataSource(data=data)

    p2 = figure(x_range=fruits2, y_range=(0, 60), plot_height=350, title=str("Types per gender per state 1 op de 100.000"),
            toolbar_location=None, tools="")

    p2.vbar(x=dodge('fruits2', -0.25, range=p2.x_range), top='Male Victim', width=0.2, source=source,
        color="#aeaeb8", legend=value("Male Victim"))

    p2.vbar(x=dodge('fruits2',  0.0,  range=p2.x_range), top='Male Suspect', width=0.2, source=source,
        color="#0d3362", legend=value("Male Suspect"))

    p2.vbar(x=dodge('fruits2',  0.25,  range=p2.x_range), top='Female Victim', width=0.2, source=source,
        color="#e69584", legend=value("Female Victim"))

    p2.vbar(x=dodge('fruits2',  0.5,  range=p2.x_range), top='Female Suspect', width=0.2, source=source,
        color="#c64737", legend=value("Female Suspect"))

    p2.xaxis.major_label_orientation = math.pi/2
    p2.x_range.range_padding = 0.1
    p2.xgrid.grid_line_color = None
    p2.legend.location = "top_left"
    p2.legend.orientation = "horizontal"

    return p2

def statesincident(year):
    with open('gunfire.json') as f:
        data = json.load(f)

    states2 = {}
    for incident in data:
        yeartje = incident["date"][0]
        if yeartje == year:
            genders = incident["participant_gender"]
            victims = incident["participant_type"]
            state = incident["state"]
            if genders == None or victims == None or state == None:
                continue
            if state not in states2:
                states2[state] = {'Male suspect': 0, 'Female suspect': 0, 'Male victim':0, 'Female victim':0}
            for key in genders:
                gender = genders.get(key)
                thetype = victims.get(key)
                if gender == 'Male' and thetype == 'Subject-Suspect':
                    states2[state]['Male suspect'] += 1
                elif gender == 'Female' and thetype == 'Subject-Suspect':
                    states2[state]['Female suspect'] += 1
                elif gender == 'Male' and thetype == 'Victim':
                    states2[state]['Male victim'] += 1
                elif gender == 'Female' and thetype == 'Victim':
                    states2[state]['Female victim'] += 1

    statelist = []
    countlist = []
    with open('populationstate2017.txt') as s:
        temp = s.read().splitlines()
        for elem in temp:
            state, amount = elem.split(',')
            statelist.append(state)
            countlist.append(amount)

    for iets in statelist:
        indexnum = int(statelist.index(iets))
        for key in states2[iets]:
            howmany = int(states2[iets].get(key))
            standardized = howmany/int(countlist[indexnum])*100000
            states2[iets][key] = standardized

    sort = sorted(states2)

    fruits2 = [key for key in sort]
    years = ['Male Victim', 'Male Suspect', 'Female Victim', 'Female Suspect']
    colorsmen = ["#c9d9d3", "#718dbf"]
    colorswomen = ["#718dbf", "#e84d60"]

    data = {'fruits2' : fruits2,
            'Male Victim'   : [states2[key]['Male victim'] for key in sort],
            'Male Suspect'   : [states2[key]['Male suspect'] for key in sort],
            'Female Victim' : [states2[key]['Female victim'] for key in sort],
            'Female Suspect' : [states2[key]['Female suspect'] for key in sort]}

    source = ColumnDataSource(data=data)

    p2 = figure(x_range=fruits2, y_range=(0, 50), plot_height=350, plot_width=2000, title=str("Types per gender per state " + year),
            toolbar_location=None, tools="")

    p2.vbar(x=dodge('fruits2', -0.25, range=p2.x_range), top='Male Victim', width=0.2, source=source,
        color="#aeaeb8", legend=value("Male Victim"))

    p2.vbar(x=dodge('fruits2',  0.0,  range=p2.x_range), top='Male Suspect', width=0.2, source=source,
        color="#0d3362", legend=value("Male Suspect"))

    p2.vbar(x=dodge('fruits2',  0.25,  range=p2.x_range), top='Female Victim', width=0.2, source=source,
        color="#e69584", legend=value("Female Victim"))

    p2.vbar(x=dodge('fruits2',  0.5,  range=p2.x_range), top='Female Suspect', width=0.2, source=source,
        color="#c64737", legend=value("Female Suspect"))

    p2.xaxis.major_label_orientation = math.pi/2
    p2.x_range.range_padding = 0.1
    p2.xgrid.grid_line_color = None
    p2.legend.location = "top_left"
    p2.legend.orientation = "horizontal"

    return p2


def statespercentage(year):
    with open('gunfire.json') as f:
        data = json.load(f)

    # Maak een dict aan voor elke state met daarin een dictionary die bijhoudt hoe vaak een
    # type van een bepaald gender voorkomt. 
    states = {}
    for incident in data:
        yeartje = incident["date"][0]
        if yeartje == year:
            genders = incident["participant_gender"]
            victims = incident["participant_type"]
            state = incident["state"]
            if genders == None or victims == None or state == None:
                continue
            if state not in states:
                states[state] = {'Male suspect': 0, 'Female suspect': 0, 'Male victim':0, 'Female victim':0}
            for key in genders:
                if genders[key] == 'Male' and victims[key] == 'Subject-Suspect':
                    states[state]['Male suspect'] += 1
                if genders[key] == 'Female' and victims[key] == 'Subject-Suspect':
                    states[state]['Female suspect'] += 1
                if genders[key] == 'Male' and victims[key] == 'Victim':
                    states[state]['Male victim'] += 1
                if genders[key] == 'Female' and victims[key] == 'Victim':
                    states[state]['Female victim'] += 1

    # Maakt een dictionary aan met elke state daarin en het aantal mensen die voor is gekomen
    # bij alle incidenten
    total_victim_susp = {}
    for incident in data:
        yeartje = incident["date"][0]
        if yeartje == year:
            genders = incident["participant_gender"]
            victims = incident["participant_type"]
            state = incident["state"]
            if genders == None or victims == None or state == None:
                continue
            if state not in total_victim_susp:
                total_victim_susp[state] = {'total': 0}
            for key in genders:
                if genders[key] == 'Male' and victims[key] == 'Subject-Suspect':
                    total_victim_susp[state]['total'] += 1
                if genders[key] == 'Female' and victims[key] == 'Subject-Suspect':
                    total_victim_susp[state]['total'] += 1
                if genders[key] == 'Male' and victims[key] == 'Victim':
                    total_victim_susp[state]['total'] += 1
                if genders[key] == 'Female' and victims[key] == 'Victim':
                    total_victim_susp[state]['total'] += 1

    # Maakt een percentage van elke state en elke type en elk gender
    for state in states:
        procent_ms = (states[state]['Male suspect']/total_victim_susp[state]['total']) * 100
        procent_mv = (states[state]['Male victim']/total_victim_susp[state]['total']) * 100
        procent_fs = (states[state]['Female suspect']/total_victim_susp[state]['total']) * 100
        procent_fv = (states[state]['Female victim']/total_victim_susp[state]['total']) * 100
        states[state]['Male suspect'] = procent_ms
        states[state]['Male victim'] = procent_mv
        states[state]['Female suspect'] = procent_fs
        states[state]['Female victim'] = procent_fv


    sort = sorted(states)

    fruits1 = [key for key in sorted(states)]
    years = ['Male Victim', 'Male Suspect', 'Female Victim', 'Female Suspect']
    colorsmen = ["#c9d9d3", "#718dbf"]
    colorswomen = ["#718dbf", "#e84d60"]


    data = {'fruits1' : fruits1,
            'Male Victim'   : [states[key]['Male victim'] for key in sort],
            'Male Suspect'   : [states[key]['Male suspect'] for key in sort],
            'Female Victim' : [states[key]['Female victim'] for key in sort],
            'Female Suspect' : [states[key]['Female suspect'] for key in sort]}

    source = ColumnDataSource(data=data)

    p1 = figure(x_range=fruits1, y_range=(0, 100), plot_height=500, plot_width=3000, title=str("Types per gender per state in percentages " + year),
            toolbar_location=None, tools="")

    p1.vbar(x=dodge('fruits1', -0.5, range=p1.x_range), top='Male Victim', width=0.2, source=source,
        color="#aeaeb8", legend=value("Male Victim"))

    p1.vbar(x=dodge('fruits1',  -0.25,  range=p1.x_range), top='Male Suspect', width=0.2, source=source,
        color="#0d3362", legend=value("Male Suspect"))

    p1.vbar(x=dodge('fruits1',  0.0,  range=p1.x_range), top='Female Victim', width=0.2, source=source,
        color="#e69584", legend=value("Female Victim"))

    p1.vbar(x=dodge('fruits1',  0.25,  range=p1.x_range), top='Female Suspect', width=0.2, source=source,
        color="#c64737", legend=value("Female Suspect"))


    p1.xaxis.major_label_orientation = math.pi/2
    p1.x_range.range_padding = 0.1
    p1.xgrid.grid_line_color = None
    p1.legend.location = "top_left"
    p1.legend.orientation = "horizontal"


    return p1


