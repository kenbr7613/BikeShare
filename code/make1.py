import pandas as pd
import os
import datetime

#read input
data = pd.read_csv("data/train.csv")
#convert datetime from string to datetime object
data['datetime'] = data.convert_objects(convert_dates='coerce')
#pull hours from datetime
data['hours'] = data['datetime'].map(lambda x: x.hour)


answer = data.groupby('hours')['count'].sum()

testdata = pd.read_csv("data/test.csv")
testdata['datetime'] = testdata.convert_objects(convert_dates='coerce')
testdata['hours'] = testdata['datetime'].map(lambda x: x.hour)

testdata['count'] = testdata['hours'].map(lambda x: answer[x] / (len(data.index) / 24))

testdata[['datetime', 'count']].to_csv("submissions/sub1"+ datetime.date.today().strftime("i%Y%m%d-%H%M") +".csv",index=False)
