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
	page = requests.get(url)
	soup = bs4.BeautifulSoup(page.text,'html5lib')
	return soup

def print_html(soup):
	print soup.prettify().encode('utf-8')

def writeInFile(soup,file):
	f = open(file,'w')
	f.write(soup.prettify().encode('utf-8'))

def error_log(e, url = "", des = ""):
	f = open('error.txt','a')
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

class Hindu:

	def archive(self):#retruns a list of url year with month wise
		url = 'http://www.thehindu.com/archive/'
		links = []
		try:
			soup = get_soup(url)
		except Exception as e:
			Hindu.error_log(str([e,url,'unable to get soup - archive']))
		try:
			req = soup.find('div',class_='archiveBorder').find_all('a')
			# links = get_href(req)
			links = [a.attrs.get('href').encode('utf-8') for a in req]
		except Exception as e:
			Hindu.error_log(e,url,'archive block')
		return links

	def select_date(self,url):# select date page scraper, followed by archive page
		links = []
		try:
			soup = get_soup(url)
			req = soup.find(id='archiveDayDatePicker').table.find_all('a')
			links = get_href(req)
		except Exception as e:
			Hindu.error_log(str([e,url,'select_date']))
		# print links
		return links

	def news_page(self,url):
		links = []
		try:
			r = Render(url)
			html = r.frame.toHtml()
			soup = bs4.BeautifulSoup(str(html.toUtf8()),'html5lib')
		except Exception as e:
			Hindu.error_log(str([e,url,'Unable to get soup - news_page']))
		try:
			# print_html(soup)
			req = soup.find('div',class_='archiveWebListHolder').find_all('a')
			links = get_href(req)
		except Exception as e:
			Hindu.error_log(str([e,url,'news_page block']))
		return links
		# print links[0][1]

	def story_page(self,url):
		article = {}
		try:
			soup = get_soup(url)
		except:
			Hindu.error_log(str([e,url,'Unable to get soup - story_page']))
		try:
			title = soup.find('h1',class_='detail-title').string.encode('utf-8')
			article['title'] = title
		except Exception as e:
			article['title'] = None
			Hindu.error_log(str([e,url,'keywords']))
		try:
			p_tags = soup.find('div',class_='article-text').find_all('p',class_='body')
			# del p_tags[-1]
			# print p_tags
			story = "".join([p.find(text=True).encode('utf-8') for p in p_tags])
			article['story'] = story
		except Exception as e:
			article['story'] = None
			Hindu.error_log(e,url,'story')
		try:
			keys = soup.find(id='articleKeywords').p.find_all('a')
			keywords = [a.string.encode('utf-8') for a in keys]
			article['keywords'] = keywords
		except Exception as e:
			article['keywords'] = None
			Hindu.error_log(str([e,url,'keywords']))
		# print story
		# print keywords
		json_data = json.dumps(article)
		return json_data

	@staticmethod
	def error_log(e,url='',des=''):
		f = open('hindu_error_log.txt','a')
		f.write(str([e,url,des]))
		f.write('\n')
		f.close()

class Ind_Exp:

	base_url = 'http://archive.indianexpress.com/'
	
	def archive_page(self):
		links = []
		try:
			soup = get_soup(Ind_Exp.base_url)
		except Exception as e:
			Ind_Exp.error_log(e , Ind_Exp.base_url , 'Unable to get soup - archive_page')
		try:
			req = soup.find('div',class_='archivetbl').find_all(href=re.compile('^/archive/news/.*(2015|2014|2013)/'))
			links = [urljoin(Ind_Exp.base_url, a.attrs.get('href').encode('utf-8')) for a in req]
		except Exception as e:
			Ind_Exp.error_log(e , Ind_Exp.base_url , 'archive_page')
		return links
		# print links

	def newsPage(self,url):
		links = []
		try:
			soup = get_soup(url)
			req = soup.find('div',id='box_left').find_all('a')
			links = get_href(req)
		except Exception as e:
			Ind_Exp.error_log(e , url , 'newspage')
		return links
		# print links

	def storyPage(self,url):
		article = {}
		try:
			soup = get_soup(url)
			title = soup.find(id='ie2013-content').h1.string.encode('utf-8')
			article['title'] = title
		except Exception as e:
			article['title'] = None
			Ind_Exp.error_log(e, url, 'title')
		try:
			p_tags = soup.find('div',class_='ie2013-contentstory').find_all('p')
			story = "".join([p.find(text=True).encode('utf-8') for p in p_tags])
			article['story'] = story
		except Exception as e:
			article['story'] = None
			Ind_Exp.error_log(e , url, 'story')
		try:
			keys = soup.find('div',class_='tags2013').find_all('a')
			keywords = [a.string.encode('utf-8') for a in keys]
			article['keywords'] = keywords
		except Exception as e:
			article['keywords'] = None
			Ind_Exp.error_log(e, url, 'keywords')
		
		return json.dumps(article)

	@staticmethod
	def error_log(e,url,des):
		f = open('error_Ind_Exp.txt','a')
		f.write(str([e,url,des]))
		f.write('\n')
		f.close()

class Toi:

	def archivePage(self):
		links = []
		url = "http://timesofindia.indiatimes.com/archive.cms" #base page
		try:
			soup = get_soup(url)
			div = soup.find(id = "netspidersosh")
			a_tags = div.find('span',class_='normtxt').find_all('a')
			links = [urljoin(url,a.attrs.get('href').encode('utf-8')) for a in a_tags] #all links in a list
		except Exception as e:
			error_log(e,url,"archivePage Block")
		return links

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
		for q in toi.archivePage():
			if re.match(r'.*2014.*-[1-5][.]cms',q):
				for w in toi.dateSelect(q):
					index = w.find('2')
					index2 = w.find('/archivelist')
					directory = "-".join(w[index:index2].split('/'))
					if not os.path.exists('data/toi/'+directory):
						os.makedirs("data/toi/"+directory)
					x = 1
					# print directory
					for e in toi.newsPage(w):
						data = toi.storyPage(e[0])
						json_file = open('data/toi/'+ directory+ '/' + str(x) + '.json' , 'w')
						json_file.write(data)
						print directory + " >> " + '{0}\r'.format(x),
						x=x+1
						json_file.close()

	def hindu_scrap(self):
		hindu = Hindu()
		for archive in hindu.archive():
			if re.match(r'.*2014/0[1-5]/',archive):
				for date in hindu.select_date(archive):
					date = date[0]
					index2 = date.rfind('/')
					index = date.find('2014')
					directory = 'data/Hindu/' + "-".join(date[index:index2].split('/'))
					if not os.path.exists(directory):
						os.makedirs(directory)
					x = 1
					for news in hindu.news_page(date):
						article = hindu.story_page(news[0])
						f = open(directory + '/' + str(x) + '.json', 'w')
						f.write(article)
						f.close()
						print directory + ' >> ' + '{0}\r'.format(x),
						x = x + 1

	def ind_exp_scrap(self):
		ind = Ind_Exp()
		for x in ind.archive_page():
			# print x
			if re.match(r'.*/\d+/[1-5]/2014/', x):
				directory = '-'.join(x[x.find('news')+5:x.rfind('/')].split('/'))
				if not os.path.exists('data/Ind_Exp/'+directory):
					os.makedirs('data/Ind_Exp/'+directory)
				count = 1
				for y in ind.newsPage(x):
					article = ind.storyPage(y[0])
					f = open('data/Ind_Exp/'+directory+'/'+str(count)+'.json' , 'w')
					f.write(article)
					f.close()
					print directory + ' >> ' + '{0}\r'.format(count),
					count = count + 1
scraper = Scrap()
# print "Starting Indian Express Data scrap..."
# scraper.ind_exp_scrap()
# print "-----------DONE Indian Express Scrap-----------"
print "Starting Hindu Data scrap..."
scraper.hindu_scrap()
print "-----------DONE Hindu Scrap-----------"
# print "Starting TOI Data scrap..."
# scraper.toi_scrap()
# print "-----------Done TOI Scrap---------------"
# print "################### DONE. ##############################"