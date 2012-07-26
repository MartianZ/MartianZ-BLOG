---
title: "fakeThunder - OS X迅雷离线非官方客户端[Beta]"
date: 2012-07-24 10:53
---


fakeThunder，其实我本来想叫他fxxkThunder的，但是想到一个叫fxxk的软件在大家的Dock上也实在是太低俗了，就叫fake好了。

之所以对迅雷这么无奈，一来是因为我平常的大部分下载都是用µTorrent，Windows上的迅雷用户给µTorrent上传速度那叫一个可怜，一堆迅雷的上传速度赶不上一个用µTorrent的朋友的上传速度；二来是因为迅雷在11年发布的OS X下的客户端，据说是团队内部一个OS X爱好者自己业余开发的，BUG一堆，不支持迅雷离线，而且一年没更新了。尼玛就算是个人开发的软件也不能这么渣啊！何况你还有一堆美工妹子帮你设计呢！还给放在迅雷软件中心显眼的位置，纯粹坑OS X的用户啊。没有诚意就别出客户端，既然以公司的名义出了就好好的迭代更新，实在不行你开源也成啊！


好了，废话说了这么多，进入正题。经过一段时间的开发，搞定了一款迅雷离线客户端，相比普通的迅雷，这个只支持迅雷离线下载，不支持普通任务的下载，您可以将软件作为一个辅助，下载一些坏链、BT软件拖不动的资源。

####软件已完成的功能：

1. 与迅雷云端离线列表 http://lixian.xunlei.com 保持同步，支持从客户端添加任务

	![img](http://ww2.sinaimg.cn/large/a6131aedjw1dv75pzu9f8j.jpg)

2. 多任务同时下载，支持下载队列

	![img](http://ww1.sinaimg.cn/large/a6131aedjw1dv75sui5jbj.jpg)
	
3. 支持BT任务自动下载，保持原BT种子中的文件目录排列。

	![img](http://ww2.sinaimg.cn/large/a6131aedjw1dv75tmsxe5j.jpg)

4. 使用MPlayerX播放迅雷云点播  

	![img](http://ww2.sinaimg.cn/large/a6131aedjw1dv7anjhyqvj.jpg)
	
	**TIP**:需要在MPlayerX设置中**取消**使用ffmpeg处理流！否则无法播放视频
	
	MPlayerX设置窗口：
	![img](http://ww2.sinaimg.cn/large/a6131aedjw1dv7axuffcoj.jpg)
	
####补充说明：

1. 软件支持10.7和10.8，不支持10.6操作系统。
2. 软件不提供任何破解迅雷会员的功能，您必须使用自己的迅雷VIP账户登录。
3. 迅雷API部分修改自开源项目[loli.lu](http://loli.lu) - <https://github.com/binux/lixian.xunlei>
4. 下载核心部分修改自开源项目aria2 - <http://aria2.sourceforge.net/>

####特殊感谢

感谢Keefo(<http://lianxu.me>)和Binux(<http://binux.me/>)在开发过程中的技术支持=。=

####捐赠

fakeThunder是一款免费开源软件，软件当前处于Beta阶段，仍有很大的开发空间。如果您喜欢这款软件，点击这里 <http://donate.4321.la> 捐赠作者以支持后续的开发和相关的维护费用！

####源代码、二进制包下载地址：

详情请查看软件发布页面：<http://martianz.cn/fakethunder/>

####反馈

有任何使用上的问题，请在当前文章下方留言回复。

软件BUG、技术问题请到这里反馈： <https://github.com/MartianZ/fakeThunder/issues>