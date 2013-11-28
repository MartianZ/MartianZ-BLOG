#/usr/bin/env python
# -*- encoding: utf8 -*-
# author: MartianZ <fzyadmin@gmail.com>

from .base import BaseHandler

class NotFoundHandler(BaseHandler):
	def prepare(self):
		self.set_status(404)
		self.render("404.html")

handlers = [
	(r"/.*", NotFoundHandler),
	]