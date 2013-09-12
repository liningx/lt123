#!/usr/bin/env python
from jd_listpage import JdListPage
from z_listpage import ZListPage
import httplib2

if __name__ == '__main__':
	http = httplib2.Http('.cache')

	limit = 10
	with open('下载列表.txt') as f:
		for line in f:
			url = line.strip()

			print(url + '...')
			list_page = None
			if 'jd.com' in url:
				list_page = JdListPage(http, url)
			if 'amazon.cn' in url:
				list_page = ZListPage(http, url)
			
			products = list(list_page.parse())
			for p in products[:limit]:
				print(p)
