#/usr/bin/env python
# -*- encoding: utf8 -*-
# author: MartianZ <fzyadmin@gmail.com>

from .base import BaseHandler
import os
import PyRSS2Gen
from datetime import datetime

class RSSHandler(BaseHandler):
	def RSSMaker(self):
		articles = []
		post_dir = self.posts_dir
		file_list = []
		files = os.listdir(post_dir)

		for f in files:
			file_list.append(post_dir + os.sep + f)
		file_list.sort(reverse=True)

		for single_file in file_list:
			article = self.markdown_parser(single_file)
			if article:
				if article['e'] == 0:
					articles.append(article)

		rss_items = []
		for article in articles:
			link = self.site_url+"/article/"+article["name"]
			rss_item = PyRSS2Gen.RSSItem(
				title = article["title"],
				link = link,
				description = article["content"],
				guid = PyRSS2Gen.Guid(link),
				pubDate = datetime(	int(article["date"][0:4]),
												int(article["date"][5:7]),
												int(article["date"][8:10]),
												int(article["date"][11:13]),
												int(article["date"][14:16])))
			rss_items.append(rss_item)

		rss = PyRSS2Gen.RSS2(
			title = self.site_name,
			link = self.site_url,
			description = "",
			lastBuildDate = datetime.utcnow(),
			items = rss_items)

		rss.write_xml(open("rss.xml", "w"))


	def get(self):
		if not os.path.exists("rss.xml"):
			self.RSSMaker()

		f = open("rss.xml", "r")
		self.write(f.read())
		f.close()

handlers = [
	(r"/.*\.xml", RSSHandler),
	]