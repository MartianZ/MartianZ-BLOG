---
layout: post
title: "MatriTunes 自动整理填充iTunes歌曲专辑图片、歌词辅助工具"
date: 2012-02-02 15:08
comments: true
categories: ideas
---
今天早上有一位朋友给我发评论，晓之以理动之以情，说MXiTunes这款软件不能用了什么什么什么，我的MusicSorter不好用什么什么（我承认那是个败笔之作，我投入了大量精力在界面设计上，导致软件的功能欠缺太多）。


于是我就去看了一下MXiTunes是什么东西，原来是一款Windows下的整理iTunes列表的软件，很不错的样子。不过原作者的官方网站打不开，经过检查是因为cn域名被暂停解析的缘故，而且在我的英文版Windows 7 64Bit上也死活无法打开……

然后我就又去敲代码了，三个小时搞定了这款软件——MatriTunes。

<!-- more -->


![MatriTunes](http://i.imgur.com/KjbTV.png)


###软件介绍、使用说明：

1. 因为时间紧张，采用.Net Framework 2.0开发（Windows 7自带）

2. 支持自动歌曲搜索

3. 支持批量获取歌词、专辑图片，支持手动设置专辑图片

4. 批量搜索效果与您当前的MetaData关系很大，如果批量搜索效果不佳推荐您一个一个慢慢来

5. 软件开发仓促，有任何问题请给我发Mail或者从这个post下面留言

6. 我实在是懒得开多线程了，所以批量下载的时候尽量一次不要选择太多歌曲，同时软件工作时不要乱去戳它=。=

7. 尽量把DNS改成本地的DNS，不然豆瓣下载专辑图片速度会很慢



###下载地址：


<http://martianlaboratory.com/matritunes/MatriTunes.zip>