#/usr/bin/env python
# -*- encoding: utf8 -*-
# author: MartianZ <fzyadmin@gmail.com>
import os
import tornado
import logging
from time import time
from tornado import web
from tornado.ioloop import IOLoop, PeriodicCallback
from tornado.options import define, options
from tornado.httpserver import HTTPServer

define("debug", default=True, help="debug mode")
define("bind_ip", default="0.0.0.0", help="the bind ip")
define("port", default=8888, help="the port tornado listen to")
define("site_name", default="MartianZ!", help="blog site name")
define("site_url", default="http://blog.martianz.cn", help="blog site url")
define("posts_dir", default=os.getcwd() + os.sep + "posts", help="posts_dir")
define("link_dir", default=os.getcwd() + os.sep + "link", help="link dir")

class Application(web.Application):
	def __init__(self):
		from handlers import handlers
		settings = dict(
			debug=options.debug,

			template_path=os.path.join(os.path.dirname(__file__), "template"),
			static_path=os.path.join(os.path.dirname(__file__), "static"),

			)
		super(Application, self).__init__(handlers, **settings)

		logging.info("load finished! listening on %s:%s" % (options.bind_ip, options.port))

def main():
	tornado.options.parse_command_line()
	http_server = HTTPServer(Application(), xheaders=True)
	http_server.bind(options.port, options.bind_ip)
	http_server.start()

	IOLoop.instance().start()

if __name__ == "__main__":
	main()
