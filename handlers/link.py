#/usr/bin/env python
# -*- encoding: utf8 -*-
# author: MartianZ <fzyadmin@gmail.com>

from .base import BaseHandler
import os

class LinkHandler(BaseHandler):
	def get(self):
		post_path = self.link_dir + os.sep + 'link.markdown'
		article = self.markdown_parser(post_path)
		self.render("link.html", title=self.site_name, url=self.site_url, article = article)


handlers = [
	(r"/link", LinkHandler),
	]
