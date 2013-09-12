#!/usr/bin/env python

import sys, os
import httplib2
from bs4 import BeautifulSoup
import re

class ZListPage:
	def __init__(self, http, url):
		self.http = http
		self.url = url

	def parse(self):
		response, content = self.http.request(self.url)
		# with open('page.html', 'wb') as f:
		# 	f.write(content)
		# clean_content = re.sub('<script\s+.*?<\/script>', '', content.decode(), flags = re.I + re.S)
		# print(clean_content.encode('utf-8'))
		soup = BeautifulSoup(content)
		
		for td_tag in soup.find_all('td', class_='searchitem product'):
			a_tag = td_tag.find('a')
			url = a_tag['href']
			img_url = a_tag.find('img')['src']
			name = td_tag.find('span', class_='srTitle').text

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
	url = 'http://www.amazon.cn/b/ref=sa_menu_applia_l3_b874269051?ie=UTF8&node=874269051'
	limit = 10
	if len(sys.argv) == 3:
		url = sys.argv[-2]
		limit = int(sys.argv[-1])
	
	http = httplib2.Http('.cache')
	list_page = ZListPage(http, url)
	products = list(list_page.parse())
	for p in products[:limit]:
		print(p)