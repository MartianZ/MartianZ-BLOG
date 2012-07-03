---
layout: post
title: "MusicSeekerX – 搜索与下载音乐"
date: 2011-08-28 23:47
comments: true
categories: ideas
---


好吧，写歌词软件写得有些吐血，我就顺带完善一下之前的软件——给MusicSeeker开发了Mac版本，拉着Madimo一块开发了一下，两天的时间就完工了。

MusicSeekerX是一款仿MusicSeeker的软件（废话），用来辅助Mac用户在Mac系统下（还是废话）下载音乐。

![image](http://i.imgur.com/eXcFL.png)

软件的特性还是啰嗦一下吧：

1、支持无损音乐（flac）的搜索下载，支持下载无损音乐后自动转换为iTunes可识别的无损格式（alac m4a）

2、支持下载MP3音乐后自动添加专辑封面、添加歌词

3、优先选择高码率，音乐质量一目了然，适合各种无损控。

软件的下载保存目录、软件的一些设置都在菜单 – 偏好设置里面，推荐大家先进行设置。

软件的缺点我也不多说了，毕竟是两天就完工的作品，我在软件里面加入了比较完善的自动更新机制（废话，别人的现成的库），后续的功能还有BUG的修复软件会自动检查更新的。

如果您在使用过程中发现什么问题的话，别忘了反馈一下，谢谢支持～

如果软件确实对您起到了帮助，可以考虑捐赠作者以平衡域名、空间支出费用，捐赠地址：http://blog.4321.la/2011/09/474.html

 

再次感谢各位的支持！

<!-- more -->

下载地址：
<http://dl.4321.la/MusicSeekerX.zip>


非Lion用户请尝试通过下面的方法修改以运行软件：

经简单修改即可在Mac OS X 10.6下运行，解压后，右键单击MusicSeeker.app，选择显示包内容

方法是将原Contents/Info.plist里的

LSMinimumSystemVersion

10.7

改为

LSMinimumSystemVersion

10.6

在10.6.6下测试通过。

（由G+上面的朋友H Liang提供，10.6的朋友可以试一下，我会在下个版本完美支持10.6版本）

出现全部音乐不能下载情况的朋友，请尝试将DNS改为Google Public Dns：8.8.8.8/8.8.4.4后重试。
