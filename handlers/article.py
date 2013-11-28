#/usr/bin/env python
# -*- encoding: utf8 -*-
# author: MartianZ <fzyadmin@gmail.com>

from .base import BaseHandler
import os
import base64
import hashlib
from Crypto.Cipher import AES
from markdown import markdown

class ArticleHandler(BaseHandler):
	def auth(self):
		self.set_status(401)
		self.set_header('WWW-Authenticate', 'Basic realm=Please enter your username and password to decrypt this article')
		self._transforms = []
		self.finish()

	def get(self, article_id):
		post_path = self.posts_dir + os.sep + article_id.replace('.','') + '.markdown'
		article = self.markdown_parser(post_path)
		if article['e']:
			auth_header = self.request.headers.get('Authorization')
			if auth_header is None or not auth_header.startswith('Basic '):
				self.auth()
			else:
				try:
					auth_decoded = base64.decodestring(auth_header[6:])
					username, password = auth_decoded.split(':', 2)
					if username == "201314":
						key = hashlib.sha256(password).digest()
						cipher = AES.new(key, AES.MODE_ECB)
						article['content'] = markdown(unicode(cipher.decrypt(base64.decodestring(article['content'])),"utf8"))
						self.render("article.html", title=self.site_name, url=self.site_url, article = article)
					else:
						self.auth()
				except:
					self.auth()
		else:
			self.render("article.html", title=self.site_name, url=self.site_url, article = article)

handlers = [
	(r"/article/(.*)", ArticleHandler),
	]