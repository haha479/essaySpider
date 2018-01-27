# encoding:utf-8

import urllib2
import urllib
from lxml import etree
import os

class Imagespider(object):
	def __init__(self,headers):
		self.headers = headers

	def load_page(self,url):
		"""
		下载整个页面的源码
		:param url: 要爬取的贴吧网址
		:return:
		"""
		request = urllib2.Request(url)
		html = urllib2.urlopen(request).read()


		# 解析html文档
		content = etree.HTML(html)

		# 通过xpath获得每个帖子的超链接href ://div[@class="threadlist_lz clearfix"]/div/a/@href
		href_list = content.xpath('//div[@class="threadlist_lz clearfix"]/div/a/@href')
		# 遍历所有的href,并且跟页面的url拼接
		for href in href_list :
			fullurl =  "https://tieba.baidu.com" + href
			# print fullurl
			self.loadImage(fullurl)

	def loadImage(self,url):
		"""
		访问一个帖子,并且获得一个帖子中所有的图片src
		:param url: 一个帖子的url
		:return:
		"""
		request = urllib2.Request(url,headers=self.headers)
		html = urllib2.urlopen(request).read()

		content = etree.HTML(html)
		# 得到当前帖子中所有图片的src
		src_list = content.xpath('//div[@class="d_post_content j_d_post_content "]/img[@class="BDE_Image"]/@src')

		for src in src_list :
			# 每遍历一张图片就调用写入方法
			self.write_image(src)

	def write_image(self,src):
		"""
		将图片写入本地文件
		:param src: 图片的src地址
		:return:
		"""
		request = urllib2.Request(src,headers=self.headers)
		image = urllib2.urlopen(request).read()
		filename = src[-10:]
		# 写入
		print "downloading->" + filename

		# 进入到images目录
		os.chdir(r"../images/")
		with open(filename,"wb") as f :
			f.write(image)
		print "download completion"
	def spider(self,url,start,end):

		for page in range(start,end+1):
			pn = (page-1)*50

			# 得到指定页面的url
			fullurl = url + "&pn=" + str(pn)
			self.load_page(fullurl)

if __name__ == '__main__':
	headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"}
	key = raw_input("name:")
	start = int(raw_input("start:"))
	end = int(raw_input("end:"))
	wd = {"kw":key}
	wd = urllib.urlencode(wd)
	fullurl = "https://tieba.baidu.com/f?" + wd
	s = Imagespider(headers)
	s.spider(fullurl,start,end)