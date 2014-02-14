---
title: "CentOS 6配置Cisco IPSec VPN服务器记录"
date: 2014-02-14 12:00
---

KxxxWaxx买的VPN过期了，100元一年，自己主要是在iOS设备上用一下，流量完全用不完，实在是觉得没必要继续续费，正好VPS换到的新地方，网络环境相比之前的VPS好太多了，于是果断在VPS上搭建自用的VPN服务器。

参考网络的几个文章，记录下过程。

1. 安装IPSec-Tools / Racoon

		wget ftp://ftp.pbone.net/mirror/ftp.pramberger.at/systems/linux/contrib/rhel5/i386/ipsec-tools-0.8.0-1.el5.pp.i386.rpm
		wget ftp://ftp.pbone.net/mirror/ftp.pramberger.at/systems/linux/contrib/rhel5/i386/ipsec-tools-libs-0.8.0-1.el5.pp.i386.rpm
		yum localinstall --nogpgcheck ipsec-tools-libs-0.8.0-1.el5.pp.i386.rpm ipsec-tools-0.8.0-1.el5.pp.i386.rpm

2. 配置IPSec-Tools / Racoon

	/etc/racoon/racoon.conf

        path pre_shared_key "/etc/racoon/psk.txt";
        path certificate "/etc/racoon/certs";
        listen {
            isakmp xx.xx.xx.xx [500];
            isakmp_natt xx.xx.xx.xx [4500];
        }

        remote anonymous {
            exchange_mode aggressive, main, base;
            mode_cfg on;
            proposal_check obey;
            nat_traversal on;
            generate_policy unique;
            ike_frag on;
            passive on;
            dpd_delay 30;

            proposal {
                lifetime time 28800 sec;
                encryption_algorithm 3des;
                hash_algorithm md5;
                authentication_method xauth_psk_server;
                dh_group 2;
            }
        }

        sainfo anonymous {
            encryption_algorithm aes, 3des, blowfish;
            authentication_algorithm hmac_sha1, hmac_md5;
            compression_algorithm deflate;
        }

        mode_cfg {
            auth_source system;
            dns4 8.8.8.8;
            banner "/etc/racoon/motd";
            save_passwd on;
            network4 192.168.7.100;
            netmask4 255.255.255.0;
            pool_size 100;
            pfs_group 2;
        }

	/etc/racoon/psk.txt

	前面是VPN组名，后面是VPN密钥，VPN连接需要用到这两个值

		# Group Name Group Secret
		mzvpn mzvpn
	
	/etc/racoon/motd

	随便写一个，iOS、Mac OS X系统连接上VPN会显示该欢迎信息。

		Welcome To MartianZ VPN
		
3. 添加系统的用户名和密码

		useradd -MN -b /tmp -s /sbin/nologin USER
		passwd USER

4. 设置iptables的规则

		iptables -A INPUT -p udp -–dport 500 -j ACCEPT
		iptables -A INPUT -p udp --dport 4500 -j ACCEPT
		iptables -t nat -A POSTROUTING -s 10.12.0.0/24 -o eth0 -j MASQUERADE
		iptables -A FORWARD -s 10.12.0.0/24 -j ACCEPT
		iptables-save
		
5. 设置IPv4 forward

	修改/etc/sysctl.conf

		net.ipv4.ip_forward=1
		
	生效
	
		sysctl -p
		
6. 其它

	可以用调试模式启动racoon来看下。
	
		racoon -F
	或者：
	
		service racoon start
		chkconfig racoon on