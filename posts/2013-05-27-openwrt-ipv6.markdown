---
title: "电子科技大学清水河校区寝室网络OpenWRT IPv4+IPv6配置"
date: 2013-05-27 22:03
---

在电子科大清水河校区，寝室用的是电信网……配置起来真心略蛋疼……

记录一下整体的配置过程和思路，防止哪次Router悲剧……

###第一步 改ROM、RAM，编译 OpenWRT（记得勾选各种IPv6支持），刷路由器

这里就不多说了……我用的路由器是TP-Link WR843N，热风枪改RAM到16MiB内存，跑OpenWRT就毫无压力了。

###第二步 IPv4 NAT

校园电信网络采用的是WEP 802.1x EAP+PEAP+MSCHAPV2，相比使用锐捷什么的或者修改后的认证算法之类的学校来说还是很厚道了，在Linux下一般使用wpa supplicant进行认证。

OpenWRT自带的是wpad-mini，无法使用802.1x认证……于是首先要卸载wpad-mini，然后安装wpad，wpad就是wpa_supplicant和hostapd的集合。这里具体过程也不再记录了，scp传输文件以后opkg即可。

设置认证的配置文件，我这里把配置文件放在  /etc/802.1x.conf

	ctrl_interface=/var/run/wpa_supplicant
	ap_scan=0
	network={
		key_mgmt=IEEE8021X
		eap=MD5
		identity="用户名"
		password="密码"
		eapol_flags=0
	}
	
接着运行下面的命令

	killall wpa_supplicant

	wpa_supplicant -B -c /etc/802.1x.conf -ieth0 -Dwired
	
推荐把上面的命令设置成开机自动运行，这样每次路由器重启就完全自动连接了。如果没有错误的话就认证结束了，这时候到LuCI里面，网络 - 接口，找到WAN，配置为DHCP客户端，然后点击右边的 连接，如果没有问题的话就可以获得IPv4和IPv6地址了。如下图：

![img1](http://ww2.sinaimg.cn/large/635877bcjw1e52uemz1yyj20lb0h6q63.jpg)

这个时候应该可以连接到路由器上网了，IPv4的NAT应该都自动配置好了，其他设置按需进行吧。

###第三步 IPv6 NDP

IPv4由于NAT的存在共享上网是想当的简单（随便一个不懂电脑的萌妹子给家里搞一台TP-Link，就知道设置PPPoE认证然后就NAT组建家庭局域网共享上网了……让我等苦逼技术死宅没有了上门帮忙的机会 QAQ），IPv6标准协议里面木有NAT，让我顿时费解了一把，后来谷歌了一下发现北邮有一群学生做了一个创新项目实现了IPv6的NAT，当时感觉是各种膜拜啊……还是内核级的项目啊卧槽……难道我又要改内核代码然后重新编译OpenWRT了啊……

后来仔细研究了一下，果然北邮那个项目还是没啥意思的，有点坑经费的感觉，因为IPv6有一种更好的解决方案：Proxy Neighbour Discovery Protocol（邻居发现协议），具体可以看：<http://en.wikipedia.org/wiki/Neighbor_Discovery_Protocol>。

简单来说，NAT就是把内网终端伪装起来请求出去，同时数据会到有外网地址的Router，再让此Router把数据包转发给客户端机器。由于IPv6的地址空间是相当相当的大，没有必要再公用一个外网地址，可以让每个内网的终端都具有一个外网地址

这个地址依然是不可再路由，这时就需要让具有外网地址的Router帮忙告诉它的上层Router，这些外网地址在这个Router的内网中。

这种方式牛逼之处在于……什么UPnP，什么NAT穿透，全部都不需要了……P2P什么的嘛……完全无压力……

继续配置，我这里外网网卡是eth0，内网是br-lan

先安装ndppd

	opkg update && opkg install ndppd

看一下我的Global IPv6地址：

	root@OpenWrt:/etc# ifconfig eth0
	eth0      Link encap:Ethernet  HWaddr 8C:21:0A:A6:94:B3  
          inet addr:121.48.171.138  Bcast:121.48.171.255  Mask:255.255.255.128
          inet6 addr: 2001:250:2000:7520:8e21:aff:fea6:94b3/64 Scope:Global
          inet6 addr: fe80::8e21:aff:fea6:94b3/64 Scope:Link
          UP BROADCAST RUNNING ALLMULTI MULTICAST  MTU:1500  Metric:1
          RX packets:517397 errors:0 dropped:450 overruns:0 frame:0
          TX packets:777032 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:177017984 (168.8 MiB)  TX bytes:688621714 (656.7 MiB)
          Interrupt:4 
是2001:250:2000:7520:8e21:aff:fea6:94b3/64，因为是/64，所以无法继续划分子网，就要使用刚才说的邻居发现协议。

然后给内网网卡br-lan设置与eth0的地址前64位相同，后64位不同的IPv6地址（不要直接抄袭我的，如果你也在电子科大清水河……这样咱们会冲突的），设置时前缀长度要大于64：

	ip -6 addr add 2001:250:2000:7520:1::1/80 dev br-lan
	
修改/etc/ndppd.conf

	proxy eth0{
		router yes
		timeout 500
		ttl 30000


		rule 2001:250:2000:7520:1::/80 {
	  	  auto
		}
	}

然后运行ndppd：/etc/init.d/ndppd start，这样就配置好了。比内核级的NAT实现要轻松许多。

但是这个时候还不能客户端自动获得IP，radvd配置只能前缀为64，所以还需要dhcpv6 server：

	opkg install radvd
	opkg install wide-dhcpv6-server
	
配置/etc/config/radvd：

	config interface
        option interface        'lan'
        option AdvSendAdvert    1
        option AdvManagedFlag   1
        option AdvOtherConfigFlag 1
        list client             ''

	config prefix
        option interface        'lan'
        # If not specified, a non-link-local prefix of the interface is used
        list prefix             ''
        option AdvOnLink        1
        option AdvAutonomous    1
        option AdvRouterAddr    0

配置/etc/config/dhcp6s，enabled设置为1

配置/etc/dhcp6s.conf

	interface br-lan {
		address-pool pool1 86400;
	};
	pool pool1 {
		range 2001:250:2000:7520:1::200 to 2001:250:2000:7520:1::300 ;
	};
	
启动radvd和dhcpv6 server：

	/etc/init.d/radvd start
	/etc/init.d/dhcp6s start
	
注意顺序，如果遇到错误，可以：

	/etc/init.d/radvd restart
	/etc/init.d/ndppd restart
	
这样我们就配置好了IPv6的邻居发现协议和IP地址的分配，这个时候连上路由器的客户端已经可以自动获得IPv4和IPv6的地址并无障碍访问IPv4和IPv6的网络了：

![img2](http://ww1.sinaimg.cn/large/635877bcjw1e52v0hzts6j20lq0jaabt.jpg)

本地Ping Google IPv6：

	MartiandeMacBook-Pro:~ MartianZ$ ping6 ipv6.google.com
	PING6(56=40+8+8 bytes) 2001:250:2000:7520:1::100 --> 2404:6800:4008:c01::68
	16 bytes from 2404:6800:4008:c01::68, icmp_seq=0 hlim=46 time=110.295 ms
	16 bytes from 2404:6800:4008:c01::68, icmp_seq=1 hlim=46 time=113.267 ms
	16 bytes from 2404:6800:4008:c01::68, icmp_seq=3 hlim=46 time=109.890 ms
	^C
	--- ipv6.l.google.com ping6 statistics ---
	4 packets transmitted, 3 packets received, 25.0% packet loss
	round-trip min/avg/max/std-dev = 109.890/111.151/113.267/1.506 ms

外部Ping本地：

	IPv6 Ping Output:
	PING 2001:250:2000:7520:1::100(2001:250:2000:7520:1::100) 32 data bytes
	40 bytes from 2001:250:2000:7520:1::100: icmp_seq=0 ttl=41 time=373 ms
	40 bytes from 2001:250:2000:7520:1::100: icmp_seq=1 ttl=42 time=374 ms
	40 bytes from 2001:250:2000:7520:1::100: icmp_seq=2 ttl=42 time=373 ms
	40 bytes from 2001:250:2000:7520:1::100: icmp_seq=3 ttl=42 time=372 ms

	--- 2001:250:2000:7520:1::100 ping statistics ---
	4 packets transmitted, 4 received, 0% packet loss, time 3011ms
	rtt min/avg/max/mdev = 372.783/373.540/374.239/0.540 ms, pipe 2



在外面的网络测试了一下，我的IP地址[2001:250:2000:7520:1::100]，直接可以ping通，并且 http://[2001:250:2000:7520:1::100]:8080也可以直接访问我电脑的Web Server，类似一个独立的IP一样。无需再考虑NAT穿透的事情。

全部配置完成~撒花~