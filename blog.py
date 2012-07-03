import tornado.ioloop
import tornado.web
import string, os, sys
import markdown
import codecs

site_config = {
	"title" : "MartianZ!",
	"url" : """http://blog.4321.la""",
	"post_dir": os.getcwd() + os.sep + 'posts',
}

settings = {
	"static_path": os.path.join(os.path.dirname(__file__), "static")
}

def SingleFileHandler(file_path):
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
	index = 1

	for line in lines[1:]:
		index += 1
		if line.find('title: ') == 0:
			title = line.replace('title: "','')[0:-2]
		if line.find('date: ') == 0:
			date = line.replace('date: ','')[0:-1]
		if line.find('---') == 0:
			break

	content = u'';
	for line in lines[index:]:
		content += line
		
	if title:
		ret['title'] = title
		ret['date'] = date
		ret['content'] = markdown.markdown(content)
		ret['name'] = file_path.split(os.sep)[-1].split('.')[0]
	return ret
	
class MainHandler(tornado.web.RequestHandler):
	def get(self):
		articles = []
		post_dir = site_config["post_dir"]
		file_list = []
		files = os.listdir(post_dir)

		p = int(self.get_argument('p','0'))

		for f in files:
			file_list.append(post_dir + os.sep + f)
		file_list.sort(reverse=True)
		for single_file in file_list[p:p+3]:
			article = SingleFileHandler(single_file)
			if article: articles.append(article)

		if p > 2:
			prev = True
		else:
			prev = False

		if p + 4 < len(file_list):
			pnext = True
		else:
			pnext = False
		
			 
		self.render("template/index.html", title=site_config['title'], url=site_config["url"], articles = articles, prev=prev, pnext=pnext, prevnum=p-3, nextnum=p+3)

class ArticleHandler(tornado.web.RequestHandler):
	def get(self, article_id):
		post_path = site_config["post_dir"] + os.sep + article_id.replace('.','') + '.markdown'
		article = SingleFileHandler(post_path)
		
		self.render("template/article.html", title=site_config['title'], url=site_config["url"], article = article)

application = tornado.web.Application([
	(r"/", MainHandler),
	(r"/article/(.*)", ArticleHandler),
], **settings)

if __name__ == "__main__":
	application.listen(8888)
	print "MartianZ Burogu Sutato!"
	tornado.ioloop.IOLoop.instance().start()
