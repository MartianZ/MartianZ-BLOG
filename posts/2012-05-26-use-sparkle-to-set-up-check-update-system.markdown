---
layout: post
title: "使用Sparkle为OS X App添加自动更新功能"
date: 2012-05-26 21:01
comments: true
categories: notes
---
如果你细心的话，会发现OS X下面的很多应用的自动更新机制都非常相似，没错，他们都用的是**Sparkle**这个framework。（App Store里面的应用除外，因为苹果禁止使用第三方更新系统）

同类的framwork还有Google的[Update Engine](http://code.google.com/p/update-engine/)，相比较要强大一些，不过对于一般的应用来说Sparkle就足够了。

![Sparkle](http://sparkle.andymatuschak.org/Screenshot.jpg)

如何为我的程序添加自动更新系统？

### 基本设定

1. **在你的项目中添加 Sparkle framwork**

	* 下载Sparkle <http://sparkle.andymatuschak.org/>，解压
	* 将 **Sparkle.framework** 拖拽到项目的Framework folder中，同时确定勾选Xcode提示框中的“Copy items into the destination group’s folder”
	* 在Project Navigator中单击你的项目，选择你的Target，切换到Build Phases选项卡
	* 单击右下角的Add Build Phase，选择Copy Files
	
		![Imgur](http://i.imgur.com/ji1h0.png)
		
	* 在Destination中选择Frameworks，然后把Sparkle.framwork拖拽进去	
		![Imgur](http://i.imgur.com/dcQBu.png)
		
		
2. **设置 Sparkle Updater Object**

	* 打开你的MainMenu.nib
	* 选择 View → Utilities → Object Library，找到Object，双击添加
	* 单击刚刚添加的Object
	* 在Custom Class里面输入SUUpdater
	* 如果需要，你也可以创建一个Menu Item，然后把它的taeget设置到SUUpdater实例的checkForUpdates:方法
	
3. **数字签名**

	为了确保更新是来自开发者的服务器并经过开发者的授权，不被第三方篡改，Sparkle添加了数字签名机制。
	
	* 打开终端，cd到Sparkle目录的Extras/Signing\ Tools文件夹下
	* ruby generate_keys.rb
		稍等片刻就可以看到如下提示：
		![Imgur](http://i.imgur.com/7eJuV.png)
		
		这时目录中就会出现dsa_pub.pem和dsa_priv.pem两个文件，保存好dsa_priv.pem这个似有的密钥。
	* 将Public Key (dsa_pub.pem) 添加到项目的资源文件夹中
	* 在项目的Info.plist中添加一个SUPublicDSAKeyFile Key，然后将它的值设置为Public Key的文件名称（默认dsa_pub.pem）
	
	
4. **设置更新通知服务、发布新更新**

	* 通知采用一个RSS Feed，具体格式及发布更新的方法参见：<https://github.com/andymatuschak/Sparkle/wiki/publishing-an-update>
	* 在项目的Info.plist中添加一个SUFeedURL Key，然后把它的值设置成RSS的URL。
	* 确保在Info.plist里面有一个合适的CFBundleVersion
	
5. **如果需要，测试整个系统**

	* 确保要新程序的CFBundleVersion要比旧版本的CFBundleVersion值大
	* 程序会在第二次运行的时候提示是否自动检查更新，不在第一次启动的时候就提示是给用户为了留下一个好印象
	
	
这样，整个过程就完成了，后续发布更新可以参照第四步中的引用的URL中的说明进行。
	
