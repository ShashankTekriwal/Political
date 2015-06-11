import os
import json
import matplotlib.pyplot as plt
from datetime import datetime
from pprint import pprint
import re

def frequency(search_list, file_path):

	# rootdir = 'shashank/data_new'
	rootdir = 'shashank/shashank/data'
	counter = {}
	count=0

	for folder in os.listdir(rootdir):
		counter[folder] = {}
		for date in os.listdir(os.path.join(rootdir,folder)):
			counter[folder][date] = {}
			c = {}
			for term in search_list:
				c[term] = 0

			word_counter = 0

			for files in os.listdir(os.path.join(rootdir,folder,date)):
				f = open(os.path.join(rootdir,folder,date,files),'r')
				s = json.load( f )
				count+=1
				print "{0}\r".format(count),
				f.close()

				story = s['story']
				title = s['title']

				if story == None or len(story)==0:
					continue
				if title == None or len(title)==0:
					title = ''

				story = story.strip()
				title = title.strip()
				story += title

				for word in story.split():
					if re.match(r'.*[a-zA-Z].*', word):
						word_counter += 1

				for term in search_list:
					if (term == 'AAP'):
						c[term] += story.count(term) + story.count('Aam Aadmi Party')
					elif (term == 'BJP'):
						c[term] += story.count(term) + story.count('Bharatiya Janata Party')
					elif (term == 'INC'):
						c[term] += story.count(term) + story.count('Congress')
					elif (term == 'Modi'):
						c[term] += story.count(term) + story.count('NaMo')
					else:
						c[term] += story.count(term)

			if word_counter != 0:
				for term in search_list:
					c[term] = (float(c[term]) / word_counter) * 100.0
				counter[folder][date] = c
			else:
				del(counter[folder][date])

	print count
	print "Creating File"
	f = open(file_path,'w')
	f.write(json.dumps(counter))
	f.close()
	print "Done"

def graph1(file_path,sub_list):

	f = open(file_path,'r')
	s = json.load(f)
	f.close()

	for paper in s:
		fig = plt.figure(figsize = (16, 12), dpi= 96)
		for term in sub_list:
			x = []
			y = []
			for date in s[paper]:
				d = date
				if paper == 'ie':
					d = datetime.strptime(date,'%d-%m-%Y')
				else:
					d = datetime.strptime(date,'%Y-%m-%d')
				x.append(d)
				y.append(s[paper][date][term])
			x,y = zip(*sorted(zip(x,y)))
			plt.plot(x, y, 'o-', label = term)
		plt.legend(loc = 'upper left')
		fig.savefig("Election_14/graphs/"+paper+"_leaders.png", bbox_inches = 'tight')
		plt.clf()
		fig.clf()

def graph2(file_path,sub_list):

	f = open(file_path,'r')
	s = json.load(f)
	f.close()

	for term in sub_list:
		fig = plt.figure(figsize = (16, 12), dpi= 96)
		for paper in s:
			x = []
			y = []
			for date in s[paper]:
				d = date
				if paper == 'ie':
					d = datetime.strptime(date,'%d-%m-%Y')
				else:
					d = datetime.strptime(date,'%Y-%m-%d')
				x.append(d)
				y.append(s[paper][date][term])
			x,y = zip(*sorted(zip(x,y)))
			plt.plot(x, y, 'o-', label = paper)
		plt.legend(loc = 'upper left')
		fig.savefig("Election_14/graphs/"+term+".png", bbox_inches = 'tight')
		plt.clf()
		fig.clf()


search_list = ['Kejriwal','AAP','Modi','BJP','INC','Rahul Gandhi']
# sub_list = ['BJP','AAP','INC']
sub_list = ['Modi', 'Kejriwal', 'Rahul Gandhi']
# file_path = 'Election_13/count_all.json'
file_path = 'Election_14/count_all.json'
# frequency(search_list,file_path)
graph2(file_path,sub_list)
graph1(file_path,sub_list)
