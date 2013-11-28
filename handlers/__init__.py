# -*- encoding: utf8 -*-
# author: MartianZ <fzyadmin@gmail.com>

handlers = []

modules = ["index", "article", "rss", "error"]

for module in modules:
	module = __import__("handlers."+module, fromlist=["handlers"])
	handlers.extend(module.handlers)