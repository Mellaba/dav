import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json

def delete_columns():
	'''run only once first time:
	will delete the koloms we do not want to use from the csv file'''

	df = pd.read_csv('gunfire_small.csv', sep=',')
	nf = df.drop(['incident_url', 'source_url', 'incident_url_fields_missing', 'gun_stolen', 'location_description', 'n_guns_involved', 'participant_relationship', 'notes', 'sources'],axis=1)
	nf.replace('', np.nan, inplace=True)
	nf.to_csv('gunfire_small.csv', index=False)
	# print(nf)
	return None

def csv_to_json():
	'''create json file from the csv'''

	df = pd.read_csv('gunfire_small.csv', sep=',', encoding='latin-1')
	df.to_json('gunfire_small.json', orient='records')


delete_columns()
csv_to_json()