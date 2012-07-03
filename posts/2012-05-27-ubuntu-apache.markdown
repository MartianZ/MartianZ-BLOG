---
layout: post
title: "Ubuntu Server下配置Apache Web服务器"
date: 2012-05-27 08:52
comments: true
categories: notes
---
其实相关的文章已经很多了，今天配置一台VPS拿来做软件的更新通知服务器以及一些Api，所以记录一下。其中一些比较难记忆资料来自网上的介绍。细节的配置，例如虚拟主机的参数不再说了，因为官方都有详细的文档，只说说整体的思路，如果有错误欢迎拍砖。

----

1. ##Apache介绍
 
	Apache在Web服务器上有着不少的份额，我个人觉得拿来跑PHP之类的服务要比nginx稳定的多，当然如果做反向代理的话还是首选nginx。
	
	Apache的httpd服务器目前有两个分支，Apache 1.3系列和2.x系列，前者已经被Ubuntu自7.1版本开始剔除。在Ubuntu和Debian中，Apache的主要功能模块（Multi-Processing Module，MPM，多道处理模块）被分成了不同的软件包，分别是：
	
	* apache2-mpm-event——事件驱动
	* apache2-mpm-perchild——过渡软件包，依赖worker
	* apache2-mpm-prefork——传统MPM，兼容1.3，无多线程
	* apache2-mpm-worker——多线程、多进程混合模型的高速MPM
	* apache2-mpm-itk——基于prefork实现的多用户MPM


2. ##Apache MPM选择

	Ubuntu提供Apache 2的三个软件包分别是event、prefork、worker。要想让Apache的性能最佳，第一步要做的就是选择合适的MPM。
	
	* event：这个MPM适用于需要有大量持续连接的(KeepAlive)的情况，KeepAlive的好处相信大家都知道，可以在同一个TCP连接中响应多次请求，这种请求方式可以使一个包含很多元素（图片，CSS，etc）的HTML网页加速一半以上。在配置文件中设置KeepAlive为On，就可以开启KeepAlive。
	* perfork：实现了一个非线程的MPM，兼容1.3，虽然速度不是很快，但是非常稳定，能够隔离每一个请求。perfork顾名思义，就是主进程先派生出一堆子进程，这样新的请求来了以后不需要等待服务器产生子进程所花的时间。使用perfork最重要的是设置MacClients的值，要足够大以发挥很好的性能，但是不能太高防止内存爆掉。
	* worker：Apache 2的新MPM。多进程+多线程，资源占用小的同时也比perfork要高效的多，是未来Apache 2的发展趋势吧。该MPM重要的是两个选项：MaxClients和ThreadsPerChild。ThreadsPerChild用来每个子进程允许建立的线程数，MaxClients用来控制允许建立的总线程数。
	
	* 综上所述，如果需要更好的伸缩性，选择worker或event，如果需要更好的稳定性和兼容性，选择perfork。如果无法评估自己的需要，不妨直接选择worker。
	

3. ##安装和配置Apache 2
	
	这里以worker为例，worker也是Apache 2推荐的MPM，在Ubuntu中，使用下面的命令安装软件包，事实上安装的就是apache2-mpm-worker：
	
		$ sudo apt-get install apache2
	
	需要注意的是，Apache的软件包是由Ubuntu官方核心开发组维护的。他们在编译的时候只编译了很少的模块。如果需要其他模块则需要手动添加。默认编译进去的模块有：
		
		$ apache2 -l
		Compiled in modules:
  		core.c
  		mod_log_config.c
  		mod_logio.c
  		worker.c
  		http_core.c
  		mod_so.c
		
	下面说一下Apache 2的配置文件说明（Ubuntu ONLY）
	
		/etc/apache2
		apache2.conf —— 全局配置文件
		conf.d/ —— 一般性配置
		envvars —— 环境变量
		httpd.conf —— 用户配置文件
		mods-available/ —— 已经安装的可用模块
		mods-enabled/ —— 已经启用的模块
		（你可以使用a2enmod和a2dismod命令来查看可用和已经启用的模块）
		ports.conf —— httpd服务的端口
		sites-available —— 可用的虚拟主机
		sites-enabled —— 已经启用的虚拟主机
		
	Apache网页文件存放位置：
	
	默认Apache把网站存放在/var/www目录下，你可以通过DocumentRoot更改这一设置，对于个人而言我觉得还是不要修改，然后使用类似下列的结构安排会获得比较好的效果：
	
		/var/www/www.4321.la
		/var/www/blog.4321.la
		/var/www/martianlaboratory.com
		
	这样存放的好处是显而易见的，当然如果你要开虚拟主机，存放在/home下面是更好的选择，因为用户需要登陆到自己的目录进行管理。
	
4. ##Apache 虚拟主机
	
	安装Apache以后，访问IP地址如果出现**It Works!**这样的字样说明Apache已经在提供服务了。
	
	下面来说明如何创建一个新的虚拟主机：
	
	* 先将默认的虚拟主机复制一份，在此基础上修改
	
			$ cp /etc/apache2/sites-available/default /etc/apache2/sites-available/martianlaboratory.com
			vim /etc/apache2/sites-available/martianlaboratory.com
	
	* 打开的vim编辑中，将DocumentRoot改为DocumentRoot /var/www/martianlaboratory.com/，Directory同时也要修改。**添加ServerName martianlaboratory.com**，绑定到域名。
	* 如果有很多虚拟主机，建议修改ErrorLog和CustomLog的路径。
	* 保存配置文件。
	* 创建 /var/www/martianlaboratory.com 目录，然后重启一下Apache即可看到新的虚拟主机生效了。
			
			sudo mkdir /var/www/martianlaboratory.com
			cd /var/www/martianlaboratory.com
			echo "<h1>Hello</h1>" | sudo tee index.html
			sudo a2ensite martianlaboratory.com
			sudo /etc/init.d/apache2 restart
			
	这样一个Apache的虚拟主机就配置完成了，虚拟主机的配置参数还有很多就不赘述了，网上还有官方有很多参数的详细解释。
	
5. ##Apache HTTPS实现
	
	待续……
	
6. ##优化Apache性能
	
	1. 关闭DNS查询
		
		默认的HostnameLookups在默认情况下已经被设置为off，请保持该设置。如果开启这个设置，每次客户请求的时候都会花时间去获取客户的域名。默认记录IP地址其实已经足够。
	
	2. 优化MaxClients
		对于MacClients的设置是和MPM相关的，在/etc/apache2/e2.conf文件中。以work为例，默认的配置为：
		
			<IfModule mpm_worker_module>
			StartServers          2
    		MinSpareThreads      25
			MaxSpareThreads      75 
			ThreadLimit          64
			ThreadsPerChild      25
			MaxClients          150
			MaxRequestsPerChild   0
			</IfModule>
		
		如果你的Apache 2的错误日志文件中出现以下提示，就应该增大MaxClients了：
		
			[error] server reached MaxClients settings, consider raising the Max Clients setting.
		
	3. 优化KeepAlive
		
		KeepAlive的好处是如果客户端发出多个请求，服务器不必每次都花时间去创建连接。坏处也显而易见，就是这段时间内，即使客户端不再发出请求，这个连接也还是被占着，是一种资源的浪费。
		
		默认情况下KeepAlive是On的，KeepAliveTimeout是15秒。如果服务器的请求较多、内存较小，可以通过禁用、将KeepAliveTimeout改小的方法优化。
		
	4. 启用压缩
		
		在IIS和Apache 1.3里面，gzip模块几乎是必备。在Apache 2里面，取而代之的是deflate模块，压缩比很高，可以极大的节约带宽，当然压缩是需要花费CPU时间的。
		
		要启用该模块，运行：
		
				sudo a2enmod deflate
				sudo /etc/init.d/apache2 force-reload
		
		这个模块的配置文件在：/etc/apache2/modes-enabled/deflate.conf，如果需要可以进行配置，默认的配置已经较为合理。
	
	5. 使用缓存
	
		Apache 2的缓存模块有两个，基于硬盘的disk_cache和基于内存的mem_cache。这里不再赘述，毕竟缓存从服务器层面和从网站层面的优化方法都有很多，需要根据自己的需要进行调整。
		
	6. 禁用日志
		
		写日志是很消耗资源的，如果你的网站不需要日志记录可以关闭，或者采用抽样记录的方式。
	
7. ##Apache 安全设置

	1. 文件权限
	
		有时候传一个cgi文件，传到服务器上，发现Permission Denied，然后果断就chmod 777，虽然能够解决问题，但是这是非常不安全的做法。
		
		正确的权限应该是755（所有人可执行，文件拥有者可以写入）
		
		一般来说，.htaccess应该是644，.htpasswd应该是640，一些不想别人看到的文件，比如config文件，可以给400。如果某些文件需要写入权限的话，可以先设置766，写完后改回755，除非特别需要不要用777权限。
	
	2. 密码认证
		
		待续……
	
	3. 不要用root运行Apache
		
			$ ps auxf | grep apache
			root      1753  0.0  0.1   6160   724 pts/0    S+   22:10   0:00          \_ grep --color=auto apache
			root      1594  0.0  0.6  75700  3316 ?        Ss   21:47   0:00 /usr/sbin/apache2 -k start
			www-data  1695  0.0  0.3  75700  1964 ?        S    22:00   0:00  \_ /usr/sbin/apache2 -k start
			www-data  1696  0.0  0.5 299132  2600 ?        Sl   22:00   0:00  \_ /usr/sbin/apache2 -k start
			www-data  1697  0.0  0.5 299132  2604 ?        Sl   22:00   0:00  \_ /usr/sbin/apache2 -k start
			
		上面可以看出是www-data这个用户运行的Apache，这个用户是安装的时候默认创建的，这样是安全的。如果发现Apache在root下运行，估计……
		
	4. 安全更新
	
		获取安全更新，登陆服务器执行下列命令即可：
		
			sudo apt-get update && sudo apt-get upgrade
			
		如果需要，可以订阅Ubuntu的安全邮件列表。

8. ##Apache日志分析
	待续……
	

-----

嗯，先写这么多，以后抽空把几个问题再补上，配置PHP、MySQL的笔记后续整理整理再补上。