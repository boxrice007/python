#coding:utf-8
# import modules
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import uniout
import pandas

# define function
class getNewsDetail():
	# 初始化形参值 newsurl  commneturl
	def __init__(self, newsurl, commenturl):
		self.newsurl = newsurl
		self.commenturl = commenturl

	# 获取某一个新闻具体信息
	def getnewsinfo(self, Url):
		commenturl = self.commenturl
		newsinfo = {}
		res = requests.get(Url)
		res.encoding = 'utf-8'
		soup = BeautifulSoup(res.text, 'html.parser')
		newsinfo['新闻链接'] = Url
		print Url
		try:
			newsinfo['新闻标题'] = soup.select('.main-title')[0].text
			newsinfo['新闻内容'] = ' '.join([i.text.strip() for i in soup.select('.article p')[:-1]])
			newsinfo['发布时间'] = soup.select('.date')[0].text
			newsinfo['新闻源'] = soup.select('.source')[0].text
			newsinfo['责任编辑'] = soup.select('.show_author')[0].text
			newsid = Url.split('/')[-1].rstrip('.shtml').lstrip('doc-i')
			comments = requests.get(commenturl.format(newsid))
			data = json.loads(comments.text)
			newsinfo['参与人数'] = data['result']['count']['total']
			newsinfo['评论数']  = data['result']['count']['show']
			return	newsinfo
		except:
			return newsinfo

		# 获取新闻的url
	def parsernewslink(self):
		loadurl = self.newsurl
		print loadurl
		newsdetails = []
		res = requests.get(loadurl)
		try:
			data = json.loads(res.text.lstrip('newsloadercallback(').rstrip(')\n'))
			for i in data['result']['data']:
				newsdetails.append(self.getnewsinfo(i['url']))
			return newsdetails
		except:
			return newsdetails

def main():
		# 设置加载、评论url
		loadurl = 'http://interface.sina.cn/news/get_news_by_channel_new_v2018.d.html?cat_1=51923&show_num=27&level=1,2&page={}&callback=newsloadercallback&_=1535462364542'
		commenturl = 'http://comment5.news.sina.com.cn/page/info?version=1&format=json&channel=gj&newsid=comos-{}&group=undefined&compress=0&ie=utf-8&oe=utf-8&page=1&page_size=3'
		news_total = []
		for i in range(1, 39):
			info = getNewsDetail(loadurl.format(i),commenturl)
			Info = info.parsernewslink()
			news_total.extend(Info)
			print news_total
			df = pandas.DataFrame(news_total)
			df.to_excel("news.xlsx")
# main
if __name__ == '__main__':
	main()
