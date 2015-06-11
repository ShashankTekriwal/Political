import os
import json
from datetime import datetime, timedelta
from pandas import DataFrame
from pprint import pprint
import re
import pickle

date = []
# date1 = '2013-8-1'
# date2 = '2013-12-31'
date1 = '2014-1-1'
date2 = '2014-5-31'
start_date = datetime.strptime(date1, '%Y-%m-%d')
end_date = datetime.strptime(date2, '%Y-%m-%d')
step = timedelta(days = 1)

while start_date <= end_date:
	date.append(str(start_date.date()))
	start_date += step
# print date

cols = []
names = []
cols.append(date)
names.append('date')

f = open('Election_14/count_all.json', 'r')
s = json.load(f)
f.close()

terms = ['Kejriwal','AAP','Modi','BJP','INC','Rahul Gandhi']
paper = ['hindu','toi']
# paper = ['hindu','toi','ie']

for t in terms:
	for p in paper:
		temp = []
		for d in date:
			if p == 'ie':
				d = datetime.strptime(d, '%Y-%m-%d')
				d = datetime.strftime(d, '%d-%m-%Y')
			d = d.split('-')
			d = "-".join([str(int(a)) for a in d])
			#------------------for election-14--------------------------------
			if p == 'hindu':
				d = d.replace('-','-0',1)
			#----------------------------------------------------------------
			if d in s[p]:
				temp.append(float(s[p][d][t]))
			else:
				temp.append(None)
		cols.append(temp)
		# print temp
		names.append(t + '_' + p)

dataframe = DataFrame(cols)
dataframe = DataFrame(data = dataframe.T)
dataframe.columns = names
pprint(dataframe)
f = open('Election_14/dataframe.pickle','wb')
pickle.dump(dataframe, f)
f.close()
# pprint(dataframe['AAP_hindu'][3])
dataframe.to_csv('Election_14/dataframe.csv')