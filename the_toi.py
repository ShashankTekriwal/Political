import requests
import bs4
import sys  
from PyQt4.QtGui import *  
from PyQt4.QtCore import *  
from PyQt4.QtWebKit import *
import re
from urlparse import urljoin
import json
import os

class Render(QWebPage):

	def __init__(self, url):
		self.app = QApplication(sys.argv)
		QWebPage.__init__(self)
		self.loadFinished.connect(self._loadFinished)
		self.mainFrame().load(QUrl(url))  
		self.app.exec_()

	def _loadFinished(self, result):
		self.frame = self.mainFrame()
		self.app.quit()

def get_soup(url):
	heads = {'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'}
	while True:
		try:
			page = requests.get(url, timeout = 30, headers = heads)
			break
		except:
			print '-1 \r',
			continue
	soup = bs4.BeautifulSoup(page.text,'html5lib')
	return soup

def print_html(soup):
	print soup.prettify().encode('utf-8')

def writeInFile(soup,file):
	f = open(file,'w')
	f.write(soup.prettify().encode('utf-8'))

def error_log(e, url = "", des = ""):
	f = open('error_toi.txt','a')
	f.write(str([e,url,des]))
	f.write('\n')
	f.close()

def get_href(li): #li is a list of "a" tags//returns a list of tuples(link,text)
	# return [a.attrs.get('href').encode('utf-8') for a in li]
	return [(a.attrs.get('href').encode('utf-8'),a.string.encode('utf-8')) for a in li]
	# new = []
	# for a in li:
	# 	link = a.attrs.get('href').encode('utf-8')
	# 	text = a.string.encode('utf-8')
	# 	new.append([link,text])
	# return new

class Toi:

	def dateSelect(self,url):
		link = []
		try:
			r = Render(url)  
			html = r.frame.toHtml()
			soup = bs4.BeautifulSoup(str(html.toUtf8()),'html5lib',from_encoding='utf-8')
			a_tags = soup.find(id='calender').find_all('a')
			link = [urljoin(url,a.attrs.get('href').encode('utf-8')) for a in a_tags]
		except Exception as e:
			error_log(e,url,"dateSelect Block")
		return link[3:]

	def newsPage(self,url):
		links=[]
		try:
			soup = get_soup(url)
			news = soup.div.table.next_sibling.table.find_all('a')
			links = get_href(news)
		except Exception as e:
			error_log(e,url,"NewsPage block")
		return links

	def storyPage(self,url):
		soup = get_soup(url)
		article = {}
		try:
			article['title'] = soup.find('span',class_='arttle').h1.string
		except Exception as e:
			article['title'] = None
			error_log(e,url,"Title Block")
		try:
			article['story'] = "".join(soup.find('div',class_='Normal').find_all(text=True))
		except Exception as e:
			article['story'] = None
			error_log(e,url,"Story Block")
		try:
			keys = soup.find(id="keywords").find_all('a')
			article['keywords'] = [a.string.encode('utf-8') for a in keys]
		except Exception as e:
			article['keywords'] = None
			error_log(e,url,"Keywords Block")
		json_data = json.dumps(article)
		return json_data

class Scrap:
	def toi_scrap(self):
		toi = Toi()
		# url = 'http://timesofindia.indiatimes.com/2014/{0}/{1}/archivelist/year-2014,month-{0},starttime-{2}.cms'
		# 0:month 1:day 2:starttime
		# for q in toi.archivePage():
		# 	if re.match(r'.*2014.*-[1-5][.]cms',q):
		# 		for w in toi.dateSelect(q):
		url = 'http://timesofindia.indiatimes.com/archive/year-2014,month-{0}.cms'
		month = sys.argv[1]
		uri = url.format(month)
		w_list = toi.dateSelect(uri)
		for w in w_list:
			index = w.find('2')
			index2 = w.find('/archivelist')
			directory = "-".join(w[index:index2].split('/'))
			if not os.path.exists('data/toi/'+directory):
				os.makedirs("data/toi/"+directory)
			x = 0
			# print directory
			for e in toi.newsPage(w):
				x = x + 1
				f_name = 'data/toi/'+ directory+ '/' + str(x) + '.json'
				if not os.path.exists(f_name):
					data = toi.storyPage(e[0])
					json_file = open( f_name , 'w')
					json_file.write(data)
					json_file.close()
				print directory + " >> " + '{0}\r'.format(x),
				

scraper = Scrap()
scraper.toi_scrap()
