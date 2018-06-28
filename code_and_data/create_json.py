import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import copy
import re

def delete_columns(csv_file):
    '''run only once first time:
    will delete the koloms we do not want to use from the csv file'''
    df = pd.read_csv(csv_file, sep=',')
    nf = df.drop(['incident_url', 'source_url', 'incident_url_fields_missing', 
        'gun_stolen', 'location_description', 'n_guns_involved', 'participant_relationship', 
        'notes', 'sources', 'congressional_district', 'state_house_district', 'state_senate_district'],axis=1)
    nf.replace('', np.nan, inplace=True)
    nf.to_csv(csv_file, index=False)
    # print(nf)
    return None

def csv_to_json(csv_file, json_file):
    '''create json file from the csv'''
    df = pd.read_csv(csv_file, sep=',', encoding='latin-1')
    df.to_json(json_file, orient='records')

def nice_indent(from_file, to_file):
    '''output readable json'''

    with open(from_file) as f:
        data = json.load(f)

    copydata = copy.deepcopy(data)

    for entry in copydata:
        for key in entry:
            if key == 'date':
                entry[key] = re.split('-', entry[key])

            if 'participant' in key or 'gun_type' in key:
                value = entry.get(key)
                if value == None:
                    continue
                newvalue = value.split("||")
                splitted = {}
                for e in newvalue:
                    newlist = e.split("::")
                    if len(newlist) == 1:
                        continue
                    splitted[newlist[0]] = newlist[1]
                entry[key] = splitted
            if 'characteristics' in key:
                value = entry.get(key)
                if value == None:
                    continue
                newvalue = re.split("[|]+", value)
                entry[key] = newvalue

    with open(to_file, 'w') as f:
        json.dump(copydata, f, indent=2)


# create small gunfire json
# #delete_columns('gunfire_small.csv')
csv_to_json('gunfire_small.csv', 'gunfire_small.json')
nice_indent('gunfire_small.json', 'gunfire_small.json')


# create large gunfire json
# #delete_columns('gunfire.csv')
# csv_to_json('gunfire.csv', 'gunfire.json')
# nice_indent('gunfire.json', 'gunfire.json')


csv_to_json('gunfire.csv', 'gunfire.json')
nice_indent('gunfire.json', 'gunfire.json')
