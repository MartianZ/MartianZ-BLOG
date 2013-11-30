---
title: "《The Linux Kernel Primer》第2章习题"
date: 2013-11-30 19:09
---

第2章习题：

1. Describe how hash tables are implemented in the Linux kernel.

	参考：<http://blog.csdn.net/shendl/article/details/6605207>
	
	PDF下载：<http://d.download.csdn.net/down/3441424/shendl>
	
2. A structure that is a member of a doubly linked list will have a *list_head* structure. Before the adoption of the *list_head* structure in the kernel, the structure would have the fields *prev* and *next* pointing to other like structures. What is the purpose of creating a structure solely to hold the *prev* and *next* pointers?

    第一个优点：
    如果使用传统的链表数据结构，即：

        struct list_node {
        data_type data;
        list_node *next, *prev;
        }
        
    则对于不同的数据类型，必须声明不同的结构体。Linux的链表恰恰相反，是将链表节点嵌入到数据结构中，所以无论什么数据，链表操作都得到了统一。

    第二个优点：
    一个Container数据结构可以含有多个list_head成员，这样就可以同时挂到多个不同的链表中，例如Linux内核中会将进程数据结构(task_struct)同时挂到任务链表、优先级链表等多个链表上。
    
    参考文档：<http://www.cnblogs.com/stephenjy/archive/2010/02/09/1666166.html>
    
3. 什么是内联汇编（inline assembly）?为什么要使用它？

	内联汇编不需要调用单独编译好的会变成旭，可以通过特定的结构告诉编译器将代码组合到一起，而不是编译该代码块。能大大提高C函数的可读性和执行效率。
	
4. Assume you write a device driver that accesses the serial port registers. Would you mark these addresses volatile? Why or why not?

	我会。不然编译器会尝试优化缓存这些值。同时对连续多次连续操作可能会被当做冗余操作去除。
	
5. Given what __init does, what types of functions would you expect to use this macro?

	这个宏告诉编译器相关的函数或变量仅用于初始化。编译器将标有  __init 的所有代码存储到宏所代表的section中，初始化结束后就释放这段内存。
	
	对设备驱动的初始化过程一般用 __init 标记。
	
	提高系统效率，同时一部分内核初始化机制依赖与它，参考：<http://blog.chinaunix.net/uid-25871104-id-2854544.html>