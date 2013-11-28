#/usr/bin/env python
# -*- encoding: utf8 -*-
# author: MartianZ <fzyadmin@gmail.com>

from .base import BaseHandler
import os

class IndexHandler(BaseHandler):
	def get(self):
		articles = []
		file_list = []

		post_dir = self.posts_dir;
		files = os.listdir(post_dir)

		p = int(self.get_argument('p','0'))

		for f in files:
			file_list.append(post_dir + os.sep + f)
		file_list.sort(reverse=True)
		for single_file in file_list[p:p+3]:
			article = self.markdown_parser(single_file)
			if article:
				if article['e']: article['content'] = "文章已加密，请点击标题进入浏览 =v="
				articles.append(article)

		if p > 2:
			page_prev = True
		else:
			page_prev = False

		if p + 4 <= len(file_list):
			page_next = True
		else:
			page_next = False

		self.render("index.html", title=self.site_name, url=self.site_url, articles = articles, prev=page_prev, pnext=page_next, prevnum=p-3, nextnum=p+3)

handlers = [
	(r"/", IndexHandler),
	]