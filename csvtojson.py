import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json

df = pd.read_csv('gunfire.csv', sep=',', encoding='latin-1')
df = df.to_json('gunfire.json', orient='records')
jsObject = json.parse(df)


