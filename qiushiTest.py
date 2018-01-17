# encoding:utf-8
import urllib2
import json
import jsonpath
from lxml import etree

page = 1
url = "https://www.qiushibaike.com/8hr/page/" + str(page) + "/"
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"}

request = urllib2.Request(url,headers=headers)

html = urllib2.urlopen(request).read()

# 解析html文档
text = etree.HTML(html)

# 使用模糊查询得到所有段子的根节点位置,list
node_list = text.xpath('//div[contains(@id,"qiushi_tag")]')

data_item = {}

# 遍历一次在文件中写入一个段子信息
for node in  node_list:
	# 取到用户名
	user = node.xpath('./div[@class="author clearfix"]/a/h2/text()')

	# 取到图片链接
	# image = node.xpath('//div[contains(@id,"qiushi_tag")]//div[@class="thumb"]//img/@src')

	# 取到内容
	content = node.xpath('./a/div/span')[0].text

	# 取到点赞数
	zan = node.xpath('.//i')[0].text

	# 评论
	comment = node.xpath('.//i')[1].text

	# 定义一个字典
	data_item = {
		"user" : user,
		# "image" : image,
		"content" : content,
		"zan" : zan ,
		"commtent" : comment
	}
	with open("data.txt","a") as f :
		f.write(json.dumps(data_item,ensure_ascii=False).encode("utf-8") + "\n")

