import pandas as pd
from cluster_method.source.duration_Cal import DurationCal

data = pd.read_csv('../0a0aaa2c5802f17d89ac93dc57633b76.csv')

data['duration'] = 0

for i in range(2374):
    aa = data['START_TIME'][i + 1]
    data['duration'][i] = DurationCal(str(data['START_TIME'][i]), str(data['START_TIME'][i+1]))


data.to_csv('tt.csv',index = False)