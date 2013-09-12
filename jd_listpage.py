#!/usr/bin/env python

import sys, os
import httplib2
from bs4 import BeautifulSoup

class JdListPage:
	def __init__(self, http, url):
		self.http = http
		self.url = url

	def parse(self):
		response, content = self.http.request(self.url)
		# print(content)
		soup = BeautifulSoup(content.decode('gbk'))
		# <ul class="list-h"><li>
		for li_tag in soup.find('ul', class_='list-h').find_all('li'):
			
			# <img width='220' height='220' alt='...' data-lazyload='http://...' data-img="1"/> or
			# <img width='220' height='220' alt='...' src='http://...' data-img="1"/>
			img_node = li_tag.find('img')
			img_url = img_node.get('src')
			if img_url is None:
				img_url = img_node.get('data-lazyload')
			
			# 产品名称：<div class='p-name'><a target='_blank' href='http://item.jd.com/480897.html'>夏普(SHARP) LCD-60LX540A...
			a_tag = li_tag.find('div', class_='p-name').find('a')
			name = a_tag.text
			url = a_tag['href']

			# save product image
			img_file = self.save_image(img_url)
						
			yield dict(name = name, url = url, img_file = img_file)

	def save_image(self, img_url):
		response, content = self.http.request(img_url)
		if not os.path.exists('images'):
			os.mkdir('images')
		filename = os.path.join('images', img_url.split('/')[-1])
		with open(filename, 'wb') as f:
			f.write(content)

		return filename

if __name__ == '__main__':
	url = 'http://list.jd.com/737-794-798-0-0-0-0-0-0-0-1-1-1-1-1-72-33.html'
	limit = 10
	if len(sys.argv) == 3:
		url = sys.argv[-2]
		limit = int(sys.argv[-1])
	
	http = httplib2.Http('.cache')
	list_page = JdListPage(http, url)
	products = list(list_page.parse())
	for p in products[:limit]:
		print(p)