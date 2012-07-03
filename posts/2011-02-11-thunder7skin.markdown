---
layout: post
title: "WPF仿迅雷7简易文本框焦点移动特效"
date: 2011-02-11 22:45
comments: true
categories: notes
---
![Thunder7](http://i.imgur.com/QLV64.png)


实现原理：

在主窗体上绘制一个Border，然后每次文本框获得或者失去焦点的时候启动一个StoryBoard来移动Border。
<!-- more -->

源代码下载：

<http://down.4321.la/Thunder7Textbox.rar>