import pickle
import numpy as np
from pandas.tools.plotting import autocorrelation_plot, lag_plot
import matplotlib.pyplot as plt
from scipy.stats.stats import pearsonr

dfDelhi = pickle.load(open('Election_13/dataframe.pickle','rb'))
dfNation = pickle.load(open('Election_14/dataframe.pickle','rb'))

df1 = dfDelhi.ix[:, 1:] = dfDelhi.ix[:,1:].astype(np.float64)
df2 = dfNation.ix[:, 1:] = dfNation.ix[:,1:].astype(np.float64)

def correlation(dataframe):
	# print "Corr for Delhi Elections 2013"
	# print df1.corr()
	# print "\n\nCorr for National Elections 2014"
	# print df2.corr()
	corr = dataframe.corr()
	corr.to_csv('Election_13/stats/corr.csv')


def autocorrelation(array, name):
	fig = plt.figure()
	autocorrelation_plot(array)
	plt.legend([name], loc = 'upper left')
	# plt.show()
	fig.savefig("Election_13/stats/"+name+".png", bbox_inches='tight')
	plt.clf()
	fig.clf()

# correlation()
# df1_cols = list (df1.columns.values)
# for x in df1_cols:
# 	array = df1[x]
# 	array = array[~np.isnan(array)]
# 	autocorrelation(array , x)

# correlation(df1)
# print dfNation
# print dfDelhi
# print df2[df2_cols[1]][~np.isnan(df2[df2_cols[1]])]

def acorr(array):
	array = array[~np.isnan(array)]
	array = array.tolist()
	# print len(array)
	# return
	for x in range(0,len(array)):
		x1 = array[0 : len(array)-x]
		x2 = array[x : len(array)]
		print pearsonr(x1,x2)[0]

def autocorr(array, name):
	array = array[~np.isnan(array)]
	array = array.tolist()
	fig = plt.figure()
	plt.acorr(array, maxlags=None, lw = 2)
	plt.xlim([0,len(array)])
	# plt.ylim([-1,1])
	plt.legend([name], loc = 'best')
	fig.savefig('Election_13/acorr/'+name+'.png', bbox_inches='tight')
	plt.clf()
	fig.clf()
	plt.close(fig)

df1_cols = list (df1.columns.values)
for col in df1_cols:
	array = df1[col]
	autocorr(array, col)