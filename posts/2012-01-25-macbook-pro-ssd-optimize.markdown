---
layout: post
title: "MacBook Pro ＋ Mac OS X Lion SSD优化总结［基于镁光M4］"
date: 2012-01-25 18:25
comments: true
categories: notes
---
我在买来这台MacBook Pro还是11年的事情，买来以后我就感觉被坑得很彻底——显卡性能渣到集显程度、开机速度太慢、发热、Flash太渣看Bilibili太不爽⋯⋯

Lion出来以后上述问题更加明显，甚至连Chrome都不好用了。于是只能在再次掏腰包升机硬件了，先把内存4G升级到8G，结果发现几乎没有改善，尤其是Xcode，超级吃内存，于是一狠心，我就买了个镁光M4的SSD。

我买的SSD只有64GB，因为这东西的单位储存成本实在是太高了。SSD对我来说是个新鲜物，买来以后听 [+Shadowmourne G](https://plus.google.com/106587986552086492432/posts) 忽悠一阵子，才知道这东西还得优化，于是谷歌了半天，加上也用了一段时间了，总结一下，方便以后自己用还有其他朋友参考。

<!-- more -->

##性能优化：

1、 关闭紧急运动传感器：

这个东西就是在瞬间移动的时候给HDD一个信号，让他停止读写拿开磁头。对于SSD是完全没必要的，可以通过下面的命令完全关闭：

	$ sudo pmset -a sms 0

**需要特别说明的是，我把SSD更换上以后，把光驱拆下来，把原来的HDD放到了光驱上，经过查询资料，MBP的光驱位是没有紧急运动传感器的。**

2、 **Trim**

Trim这东西，很坑爹。网上几乎所有人都说要开启Trim，为了减少性能衰减和延长SSD的寿命。我当时看了我朋友的MacBook Air，SSD的Trim是默认开启的，但是我换上M4以后，Lion下并没有自动开启。

在几个论坛上搜索了一下，有一个软件叫Tri Enabler可以强制开启，后来发现[M4还有垃圾回收机制](http://hardforum.com/showthread.php?p=1037771689)，于是我又纠结了。

最后我找到了这篇文章：

<http://digitaldj.net/2011/07/21/trim-enabler-for-lion/>

这篇文章中提到：

> DO NOT USE TRIM ENABLER (VERSION 1.1 OR 1.2) TO ENABLE TRIM ON LION.（可以通过终端开启）

> There has also been some confusion about garbage collection and TRIM. TRIM is ALWAYS preferred over Garbage Collection and will likely yield better results. If you have garbage collection, you don’t necessarily need TRIM, but it’ll probably offer better performance and there’s always a chance there’ll be a degradation of speed over time. Therefore, when using Garbage Collection, you may have to take the drive out and do a secure erase so that everything is re-marked as free space.

> Running garbage collection and TRIM at the same time is NOT a problem. They’re designed to work together. You can look at it like so: TRIM is called by your OS each time space is freed up. Garbage Collection is run by the drive’s firmware when idle and determines which parts of the drive can be cleaned up and rearranged. TRIM is obviously more efficient and obviously the drive’s firmware is aware of the TRIM commands and accounts for this.

> While it’s true that using TRIM and garbage collection at the same time is essentially using two mechanisms to do the same thing, the firmware on your SSD drive is designed to handle these things. All SSD manufacturers, GC or not, recommend the use of TRIM.

作者在文中说明了关于垃圾回收和Trim的关系，**所以你的SSD不管有没有GC**，都推荐开启Trim。综上，我们所做的就是开启Trim，但是**不要通过那个TRIM ENABLER软件**。方法仍然可以参照那篇文章所说的在命令行里面开启，这里不再赘述。

3、用noatime方式挂载SSD系统盘

> 用 noatime 方式挂载系统盘，这样可以减少不必要的 I/O 次数，虽然 SSD 做这些操作非常快速，但考虑到最后访问时间这个属性其实很少用到，大家关心的一般都是最后修改时间和创建时间，所以完全可以关闭这个属性，这在 Unix/Linux 下是非常常见的文件系统优化选项。

在**/Library/LaunchDaemons**里面创建一个**noatime.plist**，内容为：

	<?xml version="1.0" encoding="UTF-8"?>
	<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
    "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
	<plist version="1.0">
    <dict>
        <key>Label</key>
        <string>noatime</string>
        <key>ProgramArguments</key>
        <array>
            <string>mount</string>
            <string>-vuwo</string>
            <string>noatime</string>
            <string>/</string>
        </array>
        <key>RunAtLoad</key>
        <true/>
    </dict>
	</plist>

然后修改权限：

	$ sudo chown root:wheel /Library/LaunchDaemons/noatime.plist 

重启，查看是否生效，可以输入：

	mount | grep " / "

如果看到返回下面的信息，说明OK（注意有noatime）：

	/dev/disk0s2 on / (hfs, local, journaled, noatime)

##榨干空间：

1、关闭休眠：

> 默认的在 MB/MBP 上, 系统会在磁盘上维护一个和内存等大的 sleepimage 文件, 当电量耗尽时将内存中所有数据写入磁盘, 系统进入深度休眠状态, 下次唤醒时再从磁盘文件恢复状态. SSD 寸土寸金, 保留一个 8GB 大小又很少被用到的文件是很奢侈的行为.

	$ sudo pmset -a hibernatemode 0
	$ sudo rm /var/vm/sleepimage*

2、关闭Time Machine本地备份

	$ sudo tmutil disablelocal

3、清理垃圾：

推荐下载[CleanMyMac](http://macpaw.com/)或者[Disk Diet](http://itunes.apple.com/cn/app/disk-diet/id445512770?l=en&mt=12)这两块软件进行清理。


这样，我们就搞定了大部分的优化。有任何问题请在下面询问，或者Google一下。(>_<)

参考文章：

[分享下 SSD for Macbook Pro 的优化](http://hi.baidu.com/omys/blog/item/67fc8a0e3a7d84fd37d1220b.html)

[Mac下优化SSD](http://davidx.me/2011/09/24/optimize-ssd-on-mac/)

[TRIM Enabler for Lion](http://digitaldj.net/2011/07/21/trim-enabler-for-lion/)

[Mac OS X 下与 SSD 相关的优化](http://blog.jjgod.org/2010/04/17/macosx-ssd-tweaks/)

[Macbook Pro SSD 优化小结](http://yuzhuohui.info/blog/2011/12/19/macbook-pro-ssd-optimize/)

[M4 Garbage Collection?](http://hardforum.com/showthread.php?p=1037771689)