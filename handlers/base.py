# -*- encoding: utf8 -*-
# author: MartianZ <fzyadmin@gmail.com>

from tornado.web import RequestHandler
from tornado.options import options
import codecs
from markdown import markdown
import os

class BaseHandler(RequestHandler):
	@property
	def site_name(self):
		return options.site_name;
	@property
	def site_url(self):
		return options.site_url;
	@property
	def posts_dir(self):
		return options.posts_dir;

        @property
        def link_dir(self):
                return options.link_dir;

	def markdown_parser(self, file_path):
		f = codecs.open(file_path, mode='r', encoding='utf8')
		lines = []
		try:
			lines = f.readlines()
		except:
			pass
		f.close()

		ret = {}
		title = ''
		date = ''
		encrypt = 0
		index = 1

		for line in lines[1:]:
			index += 1
			if line.find('title: ') == 0:
				title = line.replace('title: "','')[0:-2]
			if line.find('date: ') == 0:
				date = line.replace('date: ','')[0:-1]
			if line.find('encrypt: 1') == 0:
				encrypt = 1
			if line.find('---') == 0:
				break

		content = u'';
		for line in lines[index:]:
			content += line

		if title:
			ret['title'] = title
			ret['date'] = date
			if encrypt:
				ret['content'] = content
			else:
				ret['content'] = markdown(content)
			ret['e'] = encrypt
			ret['name'] = file_path.split(os.sep)[-1].split('.')[0]
		return ret
