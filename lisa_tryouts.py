import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json

df = pd.read_csv('gunfire.csv', sep=',', encoding='latin-1')
#print(df[:10])
df = df.to_json('gunfire.json', orient='records')
#print(df[:10])
jsObject = json.parse("df")
