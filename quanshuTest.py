# -*- coding:utf-8 -*-

import urllib
import urllib2
import requests
import os
from lxml import etree

# 用于发送请求
def request(url,headers):
	res = requests.get(url,headers=headers)
	return res.content
	# 创建代理处理器对象
	# httpproxy_handler = urllib2.ProxyHandler({"http":"112.95.190.4:9999"})
	# opener = urllib2.build_opener(httpproxy_handler)
	# urllib2.install_opener(opener)
	# request = urllib2.Request(url,headers=headers)
	# html = urllib2.urlopen(request).read()
	# return html


class Quanshu(object):
	def __init__(self,headers):
		self.headers = headers
		self.num = -1
	def load_home(self,url):
		"""
		用来解析小说网首页
		:param url:
		:return:  首页中的12本小说的href值
		"""
		html = request(url,headers=self.headers)
		content = etree.HTML(html)
		href_list = content.xpath('//a[@class="msgBorder"]/@href')
		return href_list

	def load_page2(self,href_list):
		"""
		用来解析点击某个小说后的网页
		"""
		# 遍历首页的12个链接

		for href in href_list :
			# 请求每本小说链接
			html = request(href,headers=self.headers)
			content = etree.HTML(html)
			# 得到开始阅读的链接,list
			href_list2 = content.xpath('//a[@class="reader"]/@href')
			# print str(href_list2)
			self.load_page3(href_list2)

	def load_page3(self,href_list):
		"""
		用来解析点击开始阅读后的网页
		:param href_list:
		"""
		for href in href_list :
			html = request(href,headers=self.headers)
			content = etree.HTML(html)
			# 得到一本书中每一章节的超链接href
			href_list3 = content.xpath('//div[@class="clearfix dirconone"]/li/a/@href')
			title_list = content.xpath('//div[@class="clearfix dirconone"]/li/a/@title')
			self.load_page4(href,href_list3,title_list)

	def load_page4(self,link,href_list,title_list):
		"""
		用来遍历请求每一章节的链接,并且写入本地文件中
		:param link: 章节Url的前部分
		:param href_list: 章节Url后部分的集合
		:param title_list: 每一章节的名字
		:return:
		"""
		for href,title in zip(href_list,title_list) :
			fullhref = link + "/" + href
			html = request(fullhref,self.headers)
			content = etree.HTML(html)
			data_list = content.xpath('//div[@class="mainContenr"]/text()')
			self.num += 1
			for data in data_list :
				os.chdir("../txts")
				print "stratDomload::" + title
				f = open(str(self.num) + "-" +title+".txt","a")
				f.write(data.encode("utf-8"))
				print "Domloaded"

			# with open(title + ".txt","w") as f :
			# 	print "start~:" + title
			# 	f.write(data.encode("utf-8"))
			# 	print "domloaded!"
			# print "start~:" + title
			# f = open(title,"a")
			# f.write(data)
			# print "domloaded!"
if __name__ == '__main__':
	url = "http://www.quanshuwang.com/"
	headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"}

	a = Quanshu(headers)
	href_list = a.load_home(url)
	a.load_page2(href_list)


