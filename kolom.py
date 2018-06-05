import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('stage3.csv', sep=',')

nf = df.drop(['incident_url', 'source_url', 'incident_url_fields_missing', 'gun_stolen', 'location_description', 'n_guns_involved', 'participant_relationship', 'notes', 'sources'],axis=1)

nf.replace('', np.nan, inplace=True)
nf.to_csv('gunfire.csv', index=False)
# print(nf)