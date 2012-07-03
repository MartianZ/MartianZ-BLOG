---
layout: post
title: "使用SAE和Automator在Mac OS X上创建截图并自动上传的小应用"
date: 2012-02-12 17:25
comments: true
categories: ideas
---
先说点题外话……

大家都知道有一个很好用的IM，叫腾讯QQ……

没错，这东西确实是好用，至少在Windows和Mac OS X下很好用，在各个主流手机平台上也不错，唯独在Linux下比较可悲，官方的解决方案就是让我们用那个为了技术而技术、为了平台而平台的臃肿的WebQQ，当然也有第三方的一些开源项目，来分析QQ的协议实现客户端，但是总归腾讯QQ的协议是封闭的，实际效果也难尽如人意。

跟妹子们聊天用QQ足矣，我Mac党表示很舒坦，但是跟各位Linuxer技术宅聊天就蛋疼了，只能用其他的IM，比如Google Talk或者Skype。

这些IM虽然有在Linux下提供客户端，但是实在是让人郁闷的要死，最憋人的就是不能随时发送图片。之前我是通过Cloud、YunIO这些应用解决，但是还是觉得不够舒服，而且Cloud的服务器还被墙了，别人看图片也不方便。

于是，我就敲了几行代码来解决这个问题，采用Sina App Engine搭建服务端，本地采用Automator，如果你是Linux系统，也可以写一个很小的bash脚本解决。

<!-- more -->

第一步：从Sina App Engine上新建一个项目，然后从项目的管理里面启用Storage服务，新建一个domain，我这里给domain命名叫h，然后关闭domain的防盗链。具体操作不再赘述。

第二步：将下面的php代码部署上去：

		<?php
		
		function extend($file_name) 
		{ 
			$extend = pathinfo($file_name); 
			$extend = strtolower($extend["extension"]); 
			return $extend; 
		} 

		$target_path = SAE_TMP_PATH;
		$basename = basename( $_FILES['file']['name']);
		$domain = 'h';
		$uuid = md5(uniqid(rand(), true));
		$target_path = $target_path.$uuid;

		if(move_uploaded_file($_FILES['file']['tmp_name'], $target_path)) {
		} else{
		    echo "There was an error uploading the file, please try again!\n";
		}


		$s = new SaeStorage();

		echo $s->upload($domain, $uuid.".".extend($basename),$target_path)."\n";


		//echo $url;

		?>


php代码很简单，就是接受post请求然后把文件保存到Storage里面，之后输出文件的访问地址

第三步：从终端里面测试

使用curl命令我们来上传一个图片试试：

		curl http://项目地址.sinaapp.com/php.php -F file="@1.jpg"

其中1.jpg是当前目录下面的一张图片

如果没有错误的话就可以看到终端里面输出了上传后的文件地址：

![img](http://i.imgur.com/8Nx42.png)

第四步：建立新的Automator应用程序项目，如图所示：

其中两个Growl Notification分别提示开始上传和上传结束。

![automator](http://i.imgur.com/mDGbI.png)

之后将Automator项目保存即可，放到Dock上，以后可以随时运行截图然后自动上传。
