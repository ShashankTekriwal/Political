import os
import json
import matplotlib.pyplot as plt
from datetime import datetime
from pprint import pprint
import re

search_list = ['Arvind Kejriwal','Kejriwal','AAP','Modi','Narendra Modi','BJP','INC','Congress','Rahul Gandhi','Aam Aadmi Party','Bharatiya Janata Party']
# sub_list = ['BJP','AAP','Congress']
# sub_list = ['Kejriwal','Modi','Rahul Gandhi']
sub_list = ['Aam Aadmi Party', 'Bharatiya Janata Party', 'Congress']
# search_list = ['Cong','INC','Congress','Rahul Gandhi']
def frequency ():
	# search_list = ['Arvind Kejriwal','Kejriwal','AAP','Modi','Narendra Modi','BJP']
	rootdir = 'shashank/shashank/data'
	counter = {}
	count=0
	for folder in os.listdir(rootdir):
		counter[folder]={}
		for date in os.listdir(os.path.join(rootdir,folder)):
			counter[folder][date] = {}
			c = {}
			for term in sub_list:
				c[term] = 0
			file_counter = 0
			word_counter = 0
			for files in os.listdir(os.path.join(rootdir,folder,date)):
				f = open(os.path.join(rootdir,folder,date,files),'r')
				s = json.load(f)
				count+=1
				print "{0}\r".format(count),
				f.close()
				story = s['story']
				if story == None or len(story)==0:
					continue
				story = story.strip()
				file_counter = file_counter + 1
				for word in story.split():
					if re.match(r'.*[a-zA-Z].*', word):
						word_counter += 1
				# for term in search_list:
				for term in sub_list:
					c[term] = c[term] + story.count(term)
			#---------------------------------
			if word_counter != 0:
				# for term in search_list:
				for term in sub_list:
					c[term] = (float(c[term]) / word_counter) * 100
				counter[folder][date] = c
			else:
				del(counter[folder][date])
			#--------------------------------------------------
			# counter[folder][date] = c
	print "Creating File"
	f = open('counts_party_2.json','w')
	f.write(json.dumps(counter))
	f.close()
	print "Done"

def graphs () :
	f = open('counts.json','r')
	s = json.load(f)
	s = s['toi']
	f.close()
	y = [[],[],[],[],[],[]]
	x = []
	for dates in s:
		# print dates,
		# print ":",
		# print s[dates]
		d = dates
		d = datetime.strptime(dates,'%Y-%m-%d')
		x.append(d)
		c = 0
		for terms in s[dates]:
			# print terms
			y[c].append(s[dates][terms])
			c = c + 1
	# x,y = zip(*sorted(zip(x,y)))
	# print x
	# print y
	yy=[0,0,0,0,0,0]
	fig = plt.figure(dpi = 96, figsize = (18,12))
	for i in range(0,6):
		xx,yy[i] = zip(*sorted(zip(x,y[i])))
		plt.plot(xx,yy[i])
	# plt.plot(x,y[0])
	# plt.show()
	# print len(xx)
	# print yy[5]
	plt.legend(search_list,loc = 'upper left')
	# plt.show()
	# fig = plt.figure()
	fig.set_canvas(plt.gcf().canvas)
	if not os.path.exists('plots'):
		os.makedirs('plots')
	fig.savefig("plots/foo2" + ".jpg", format='jpg')


def graphs2():
	f = open('counts_party_2.json','r')
	s = json.load(f)
	f.close()
	data = {}
	for paper in s:
		data[paper] = {}
		x = []
		# y = [[],[],[],[],[],[]]
		y = []
		for i in range(0,len(sub_list)):
			y.append([])
		for dates in s[paper]:
			d = dates
			if paper == 'ie':
				d = datetime.strptime(dates,'%d-%m-%Y')
			else:
				d = datetime.strptime(dates,'%Y-%m-%d')
			x.append(d)
			c=0;
			for terms in s[paper][dates]:
				y[c].append(s[paper][dates][terms])
				c = c + 1
		yy=[]
		for i in range(0,len(sub_list)):
			yy.append(0)
			xx,yy[i] = zip(*sorted(zip(x,y[i])))
		data[paper]['x'] = xx
		data[paper]['y'] = yy
	# pprint(data)
	# print len(data['hindu']['x'])
	# print len(data['hindu']['y'][0])
	# f = open('plot.json','w')
	# f.write(json.dumps(str(data)))
	# f.close()
	# fig = plt.figure()
	# plt.plot(data['hindu']['x'],data['hindu']['y'][2])
	# plt.plot(data['toi']['x'],data['toi']['y'][2])
	# plt.plot(data['ie']['x'],data['ie']['y'][2])
	# plt.legend(['hindu','toi','ie'],loc = 'upper left')
	# plt.show()

	leg = []
	for terms in s['hindu']['2014-01-1']:
		leg.append(terms)
	for i in range(0,len(sub_list)):
		fig = plt.figure(figsize=(16,12), dpi = 96)
		for paper in s:
			plt.plot(data[paper]['x'],data[paper]['y'][i])
		plt.legend(['hindu','toi'],loc = 'upper left')
		fig.savefig("plotsNew/"+leg[i] + "_normalisedByTotalWords.jpg", format='jpg',bbox_inches='tight')
		plt.clf()
		fig.clf()
	# sub_list = [2,5,7]
	
	print leg
	for paper in s:
		fig = plt.figure(figsize=(16,12), dpi = 96)
		for i in range(0,len(sub_list)):
		# for i in sub_list:
			plt.plot(data[paper]['x'],data[paper]['y'][i])
		plt.legend(leg,loc = 'upper left')
		fig.savefig("plotsNew/"+ paper + "_party_2.jpg", format='jpg',bbox_inches='tight')
		plt.clf()
		fig.clf()

frequency()
graphs2()