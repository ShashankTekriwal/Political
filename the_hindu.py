import requests
import bs4
import os
import sys
from PyQt4.QtGui import *  
from PyQt4.QtCore import *  
from PyQt4.QtWebKit import *
import json
from urlparse import urljoin

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
			page = requests.get(url, timeout = 20, headers = heads)
			break
		except:
			print 'Unable to connect : '+ url
			continue
	soup = bs4.BeautifulSoup(page.text,'html5lib')
	return soup

def news_page(url):
		links = []
		while True:
			try:
				r = Render(url)
				html = r.frame.toHtml()
				soup = bs4.BeautifulSoup(str(html.toUtf8()),'html5lib')
				break
			except Exception as e:
				# error_log(str([e,url,'Unable to get soup - news_page']))
				print "News Page Dammit : " + e
				continue
		try:
			# print_html(soup)
			req = soup.find('div',class_='archiveWebListHolder').find_all('a')
			links = [a.attrs.get('href').encode('utf-8') for a in req]
		except Exception as e:
			error_log(str([e,url,'news_page block']))
		return links

def story_page(url):
		article = {}
		try:
			soup = get_soup(url)
		except:
			error_log(str([e,url,'Unable to get soup - story_page']))
		try:
			title = soup.find('h1',class_='detail-title').string.encode('utf-8')
			article['title'] = title
		except Exception as e:
			article['title'] = None
			error_log(str([e,url,'keywords']))
		try:
			p_tags = soup.find('div',class_='article-text').find_all('p',class_='body')
			# del p_tags[-1]
			# print p_tags
			story = "".join([p.find(text=True).encode('utf-8') for p in p_tags])
			article['story'] = story
		except Exception as e:
			article['story'] = None
			error_log(e,url,'story')
		try:
			keys = soup.find(id='articleKeywords').p.find_all('a')
			keywords = [a.string.encode('utf-8') for a in keys]
			article['keywords'] = keywords
		except Exception as e:
			article['keywords'] = None
			error_log(str([e,url,'keywords']))
		# print story
		# print keywords
		json_data = json.dumps(article)
		return json_data

def error_log(e,url='',des=''):
		f = open('hindu_error_log.txt','a')
		f.write(str([e,url,des]))
		f.write('\n')
		f.close()

url = 'http://www.thehindu.com/archive/web/2014/0{0}/{1}/'
no_of_days = [31,28,31,30,31]
x = sys.argv[1]
y = sys.argv[2]
# for x in range(2,6):
# 	for y in range(2,no_of_days[x]):
if y <= 9:
	uri = url.format(str(x),'0'+str(y))
else:
	uri = url.format(str(x),str(y))
index2 = uri.rfind('/')
index = uri.find('2014')
directory = 'data/Hindu/' + "-".join(uri[index:index2].split('/'))
if not os.path.exists(directory):
	os.makedirs(directory)
	# print 'made directory : ' + directory
count = 0
# print 'count = ' + str(count)
li = news_page(uri)
# print len(li)
for news in li:
	count = count + 1
	f_name = directory+'/'+ str(count) +'.json'
	# print 'f_name is ' + f_name
	if not os.path.exists(f_name):
		f = open(f_name , 'w')
		json_data = story_page(news)
		f.write(json_data)
		f.close()
	print '{0} >> {1}\r'.format(directory , count),


