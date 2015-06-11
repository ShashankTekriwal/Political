import pickle
import matplotlib.pyplot as plt
import pandas
import numpy as np
import itertools

dfDelhi = pickle.load(open('Election_13/dataframe.pickle','rb'))
dfNation = pickle.load(open('Election_14/dataframe.pickle','rb'))

dfD = dfDelhi.ix[:, 1:] = dfDelhi.ix[:,1:].astype(np.float64)
dfN = dfNation.ix[:, 1:] = dfNation.ix[:,1:].astype(np.float64)

dfDelhi['date'] = pandas.to_datetime(dfDelhi['date'])
dfNation['date'] = pandas.to_datetime(dfNation['date'])

def plot_diff(df, a1, a2):
	x = df['date'].tolist()
	leg = a1 + '-' + a2
	a1 = df[a1]
	a2 = df[a2]
	y = (a1 - a2).tolist()
	# print len(y)
	fig = plt.figure(figsize = (16,12), dpi = 96)
	plt.plot(x, y, 'o-', label = leg)
	plt.axhline(0, color = 'black')
	plt.legend(loc = 'upper left')
	fig.savefig("Election_13/difference_graphs/"+leg+".png", bbox_inches='tight')
	plt.clf()
	fig.clf()
	plt.close(fig)

cols = list(dfD.columns.values)
comb = set(itertools.permutations(cols,2))
for x in comb:
	plot_diff(dfDelhi, x[0], x[1])