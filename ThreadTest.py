# encoding:utf-8
import threading
import Queue
import requests
from lxml import etree
import time
import json

class Threadcrawl(threading.Thread):
	def __init__(self,thread_name,pageQueue,dataQueue):
		# 调用父类初始化方法
		super(Threadcrawl,self).__init__()
		self.thread_name = thread_name
		self.pageQueue = pageQueue
		self.dataQueue = dataQueue
		self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"}

	def run(self):
		print "启动" + self.thread_name
		while not CRAWL_EXIT :
			try :
				# 从page队列中取出一个页数,先进先出
				# 如果参数为True,队列为空时,不会结束,进入阻塞状态
				# 如果为False,队列为空时,会弹出异常
				page = self.pageQueue.get(False)
				url = "https://www.qiushibaike.com/8hr/page/" + str(page) + "/"
				# 请求后得到网页代码
				content = requests.get(url,headers=self.headers).text
				time.sleep(1)

				# 将代码数据放入data队列
				self.dataQueue.put(content)
			except :
				pass
		print "结束" + self.thread_name

class Threadparse(threading.Thread):
	def __init__(self,thread_name,filename,dataQueue,lock):
		super(Threadparse, self).__init__()
		self.thread_name = thread_name
		self.filename = filename
		self.dataQueue = dataQueue
		self.lock = lock

	def run(self):
		print "启动"+ self.thread_name
		while not PARSE_EXIT :
			try :
				html = self.dataQueue.get(False)
				self.parse(html)
			except :
				pass
		print "退出" + self.thread_name

	def parse(self,html):
		content = etree.HTML(html)

		node_list = content.xpath('//div[contains(@id,"qiushi_tag")]')


		# 遍历一次在文件中写入一个段子信息
		for node in node_list:
			# 取到用户名
			user = node.xpath('./div[@class="author clearfix"]/a/h2/text()')
			# 取到图片链接
			# image = node.xpath('//div[contains(@id,"qiushi_tag")]//div[@class="thumb"]//img/@src')

			# 取到内容
			content = node.xpath('./a/div/span/text()')[0]

			# 取到点赞数
			zan = node.xpath('.//i/text()')[0]

			# 评论
			comment = node.xpath('.//i/text()')[1]

			# 定义一个字典
			data_item = {
				"user": user,
				# "image" : image,
				"content": content,
				"zan": zan,
				"commtent": comment
			}
			with self.lock:
				self.filename.write(json.dumps(data_item, ensure_ascii=False).encode("utf-8") + "\n")



# 定义两个开关,一个是采集,一个是解析
CRAWL_EXIT = False
PARSE_EXIT = False

def main():
	# 定义页码的队列
	pageQueue = Queue.Queue(20)

	# 将1-20放入队列
	for i in range(1,21) :
		pageQueue.put(i)

	# 采集结果,参数为空表示不限制
	dataQueue = Queue.Queue()

	filename = open("duanzi.txt","a")
	# 创建锁
	lock = threading.Lock()
	# 三个采集线程的名字
	crawl_list = ["采集线程1","采集线程2","采集线程3"]

	# 定义列表将采集线程放入
	thread_crawl = []
	for thread_name in crawl_list :
		thread = Threadcrawl(thread_name,pageQueue,dataQueue)
		# 启动线程
		thread.start()
		# 将线程添加到列表中
		thread_crawl.append(thread)


	parse_list = ["解析线程1","解析线程2","解析线程3"]

	# 定义列表将解析线程放入
	thread_parse = []
	for thread_name in parse_list :
		thread = Threadparse(thread_name,filename,dataQueue,lock)
		thread.start()
		thread_parse.append(thread)

	# 等待page队列为空,当为空时,采集线程推出循环
	while not pageQueue.empty() :
		pass
	global CRAWL_EXIT
	CRAWL_EXIT = True
	print "pageQueue为空"

	for thread in thread_crawl :
		thread.join()
		print "1"


	while not dataQueue.empty():
		pass
	global PARSE_EXIT
	PARSE_EXIT = True
	print "dataQueue为空"

	for thread in thread_parse :
		thread.join()
		print "2"

	with lock :
		filename.close()

	print "谢谢使用!"


if __name__ == '__main__':
	main()