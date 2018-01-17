# encoding:utf-8
import urllib2
import urllib
import os
from lxml import etree

class Videospider(object):
	def __init__(self,headers):
		self.headers = headers

	def load_page(self,url):
		"""
		用于下载整个页面
		:param url: 一个页面的url
		:return:
		"""
		request = urllib2.Request(url)
		html = urllib2.urlopen(request).read()
		content = etree.HTML(html)

		data_list = content.xpath('//a[@class="threadlist_btn_play j_m_flash"]/@data-video')
		self.load_video(data_list)

	def load_video(self,data_list):
		"""
		用来请求每个视频的链接
		:param data_list: 每个视频的链接
		:return:
		"""
		for data in data_list :
			request = urllib2.Request(data)
			video = urllib2.urlopen(request).read()
			self.writevideo(data,video)

	def writevideo(self,data,video):
		filename = data[-10:]
		os.chdir("../videos")
		print "startDowload:" + filename
		with open(filename,"wb") as f :
			f.write(video)
			print "Dowloaded~"

	def spider(self,url,start_page,end_page):
		for page in range(start_page,end_page+1) :
			pn = (page-1) * 50
			fullurl = url + "&pn=" + str(pn)
			self.load_page(fullurl)


if __name__ == '__main__':
	headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"}
	a = Videospider(headers)
	key = raw_input("name:")
	start_page = int(raw_input("start_page:"))
	end_page = int(raw_input("end_page:"))
	value = {"kw":key}
	value = urllib.urlencode(value)
	url = "https://tieba.baidu.com/f?" + value
	a.spider(url,start_page,end_page)
