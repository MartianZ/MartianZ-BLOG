---
layout: post
title: "使用aria2c＋loli.lu实现高速免费迅雷离线下载"
date: 2011-12-10 23:57
comments: true
categories: notes
---
众所周知，Windows下有一款经典的下载软件，叫迅雷，下载速度一直是非常理想的

但是这款软件没有Linux版本，Mac版本也非常的烂并且没有离线下载功能

这篇教程旨在帮助大家动手打造一个方便的高速下载平台，下载工具采用aria2c，中转网站采用loli.lu（迅雷离线分享）

<!-- more -->

教程在Mac OS X Lion 10.7.2下编写，Linux用户操作方法大同小异，Windows用户请自主研究。


前期准备：下载并编译aria2c（只需进行一次即刻，以后可以直接调用～）

第一步：登录 <http://aria2.sourceforge.net/> 下载aria2c

或者，你可以通过这个地址直接下载（推荐还是去sourceforge下载最新版本）：<http://superb-sea2.dl.sourceforge.net/project/aria2/stable/aria2-1.13.0/aria2-1.13.0.tar.gz>

![image](http://i.imgur.com/2t8HQ.png)

![image](http://i.imgur.com/tNAcz.png)


第二步：解压下载的文件，放到一个你记住的位置

![image](http://i.imgur.com/4nd8d.png)

第三步：编译aria2c

进入应用程序 － 实用工具 － 终端

输入命令： cd 文件夹位置（右键 － 查看简介可以看到）/文件夹名

比如按照第二步所示，我的文件夹放在/Users/Martian/Documents，文件夹名是aria2-1.13.0，就输入 cd /Users/Martian/Documents/aria2-1.13.0，然后按下回车键

![image](http://i.imgur.com/2q6Go.png)

第四步：输入命令“./configure; make; make install”（不含引号），然后回车，就会自动配置、编译、安装aria2c

备注：编译aria2c需要安装g++，如果您已经安装了xcode套装则已经自动安装，否则请查阅相关教程先安装g++，这里不再赘述

或者参阅这篇教程，独立安装gcc：<http://www.memoryz.info/install-gcc-on-mac.html>


![image](http://i.imgur.com/i9AeI.png)

![image](http://i.imgur.com/QoJM7.png)

![image](http://i.imgur.com/WcDKq.png)
 



这样，我们就编译安装好了一款多线程、轻量级的下载工具：aria2c

下面开始使用loli.lu实现迅雷离线下载

第一步：登录http://loli.lu ，选择一个您要下载的资源，单击

![image](http://i.imgur.com/4fM96.png)

第二步：在弹出的悬浮框中，选择批量下载 － aria2c

![image](http://i.imgur.com/5TiAE.png)
 

第三步：在出来的文本框中，按Command+C复制下载地址

![image](http://i.imgur.com/gGRwy.png)

第四步：启动终端，cd到一个你要下载保存的目录，比如下载到桌面，输入 cd ~/Desktop

然后，把刚才的下载地址粘贴进去（Command+V），按回车键开始下载

出现如下图所示的内容代表已经开始下载了！


![image](http://i.imgur.com/tqnCz.png)
 

备注：aria2c支持断点续传，下次下载的话cd到下载保存目录，然后重新运行之前的下载命令即可

这样，我们就实现了通过迅雷离线服务器高速下载文件。当然Loli.lu不仅可以让用户下载与分享其他用户上传好的资源，同样可以发布资源

比如，我从极影的BT站找到了一个动漫的种子然后想要下载

![image](http://i.imgur.com/uvcYc.png)

首先我要做的就是把种子的地址复制下来，比如 http://bt.ktxp.com/down/1323442938/065d7936de1b6cd5351688b8841bef62835562ab.torrent

然后打开http://loli.lu，选择右上角的登录，输入用户名密码登录

（Loli.lu采用Google Open ID系统，与Gmail同步登录，无需重复注册，您的资料会被保密）

登录后，您可以选择右上角的发布资源（推荐），或者选择“我要直接获得资源下载地址”（需要任务即时被迅雷秒杀才可以，推荐选择发布资源）


![image](http://i.imgur.com/cAuz6.png)

![image](http://i.imgur.com/mD0pa.png)

稍等片刻，任务提交成功后，会自动跳到下载地址，然后按照教程前面所叙述的方法下载即可！

![image](http://i.imgur.com/mD0pa.png)

教程到此结束，如果大家有任何问题，欢迎到Google Plus里+Martian Z（博客留言由于近期比较繁忙，暂时不能回复，抱歉）

Loli.lu目前是一个发展中的项目，我们回在后期增加对Mac、Linux系统的专门优化（譬如客户端添加资源），同时也会增加用户RSS订阅功能，推送订阅下载地址等，希望您能支持并关注我们的发展。