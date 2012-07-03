---
layout: post
title: "在Mac OS X上架设属于你的Octopress"
date: 2012-01-25 16:09
comments: true
categories: notes
---
终于，耗时N天，把我的博客从WordPress转到了Octopress，并且很无耻的托管到GitHub上面，免费高速～

这篇文章教大家简单的Octopress的安装与使用。

（如果你用的Windows，你可能会碰到一堆雷⋯⋯强烈推荐Linux或者Mac OS X）

<!-- more -->

##1.安装

Octopress的安装不同于WordPress，WordPress是安装到服务器上面的，Octopress是安装在你本地的（如果选择Deploy到GitHub上）。首先需要准备的是Ruby环境：（下面教程均在Mac OS X Lion 10.7.2测试通过）

1、 参考这篇文章，安装GCC：<http://www.memoryz.info/install-gcc-on-mac.html> 如果你已经安装了Xcode，则无需重负安装GCC

2、 安装[Homebrew](http://mxcl.github.com/homebrew/)（或者你可以参考：<https://github.com/mxcl/homebrew/wiki/installation>）：

	$ /usr/bin/ruby -e "$(curl -fsSL https://raw.github.com/gist/323731)"
	$ brew update

3、 安装Git：

	$ brew install git

4、 安装[RVM](http://beginrescueend.com/)（或者参考：<http://beginrescueend.com/rvm/install/>）：
	
	$ bash -s stable < <(curl -s https://raw.github.com/wayneeseguin/rvm/master/binscripts/rvm-installer)
	
5、 安装Ruby 1.9.2

	$ rvm install 1.9.2
	$ rvm 1.9.2 --default

6、 安装Pow

	$ curl get.pow.cx | sh

7、 先cd到一个好的目录，比如Desktop，然后下载Octopress：

	$ git clone git://github.com/imathis/octopress.git octopress
	$ cd octopress

8、 安装一些东西：

	$ gem install bundler
	$ rbenv rehash
	$ bundle install
	$ rake install


这样，就安装好了Octopress了，输入**rake preview**，从localhost:4000可以预览结果

##2.发布

1、 在GitHub名为 “http://你的GitHub用户名.github.com” 的repository。

2、 在Octopress目录里面设定资料：

	$ rake setup_github_pages

3、 生成HTML：

	$ rake generate

4、 发布：
	
	$ rake deploy

这样等待几分钟，就可以通过 http://你的GitHub用户名.github.com 查看你的全新的Octopress BLOG！

##3.绑定域名

	$ echo '你要绑定的域名' >> source/CNAME
然后，将你要绑定的域名CNAME到 http://你的GitHub用户名.github.com，如果是@纪录，需要加入207.97.227.245。

##4.发布文章

	$ rake new_post['title']

运行上面的命令，Octopress会在source/_posts生成一个markdown（推荐阅读：<http://markdown.tw/>）文件

更多的如何编辑文档，请参阅：<http://octopress.org/docs/>

在Mac下，Markdown编辑器推荐一款国产的小软件：Mou <http://mouapp.com/>

当你把Markdown文档编辑好以后再运行rake generate和rake deploy发布到GitHub上面

##5.总结

很多的技巧，比如修改模板，Octopress官方上有详细的说明，于是我不再赘述。经过几天使用，这东西确实是Geek向，包括修改模板、导入评论等等已经让我无奈了N次⋯⋯

如果你对PHP＋MYSQL的WordPress的臃肿和那难用后台编辑器不能忍受，不妨尝试一下Octopress。同时，托管到GitHub上面也无需再支出高昂的空间费用。
