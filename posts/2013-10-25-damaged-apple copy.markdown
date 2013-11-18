---
title: "U-Boot 启动过程初步分析"
date: 2013-11-18 23:25
---

最近购入一块Cubieboard，使用Buildroot构建交叉编译链以后编译官方移植好的U-Boot，根据CPU Allwinner A10的资料，启动过程大概可分为5步：BootRom，SPL，Uboot，Kernel，RootFileSystem，先来研究RootRom到U-Boot的过程吧。

A10处理器在复位时从地址0x0开始执行指令，把BootRom映射到这一地址。A10将启动设备选择程序固化在CPU内部的一个32KB ROM中，根据Datasheet，默认的启动时序为SD Card0，NAND FLASH，SD Card2，SPI NOR FLASH。也可以通过一个电阻选择USB启动模式（有必要研究一下方便调试）。

为了不纠结于Nand分区的问题，直接用TF卡启动，根据官方Wiki，使用dd写入

	dd if=spl/sunxi-spl.bin of=/dev/sdX bs=1024 seek=8
	dd if=u-boot.img of=/dev/sdX bs=1024 seek=40
	
其中seek=40可在U-boot源代码u-boot-sunxi/include/configs/sunxi-common.h查看CONFIG_SYS_MMCSD_RAW_MODE_U_BOOT_SECTOR定义得到

可以参考 <https://github.com/linux-sunxi/u-boot-sunxi/commit/6a690123f9baa1965a76f8cdf4a34f5273caf773> 这个Commit。（Increase SPL max size to 0x7600 and move u-boot.img start to 40KB offset）

直接找到ARM的start.S启动文件，找到the actual reset code。。

ARM的汇编代码真心看得比较纠结，可以看出屏蔽了FIQ和IRQ Interrupts，设置了vector，和一些更底层的初始化，具体可以留到以后再研究。然后就bl _main了。

_main在crt0.S里，这个commit：<https://github.com/linux-sunxi/u-boot-sunxi/commit/e05e5de7fae5bec79617e113916dac6631251156> 把C runtime setup code从start.S移到一个单独的crt0.S，作为一个ARM架构的单独的lib，这样方便各个不同的ARM芯片调用。

进去以后看一下一部分汇编：

	//为 board_init_f 调用准备GD和堆栈的RAM空间
	#if defined(CONFIG_SPL_BUILD) && defined(CONFIG_SPL_STACK)
	ldr	sp, =(CONFIG_SPL_STACK)
	#else
	ldr	sp, =(CONFIG_SYS_INIT_SP_ADDR)
	#endif
	bic	sp, sp, #7	/* 8-byte alignment for ABI compliance 8字节对齐*/
	/*SP这里是一个64位的向下生长的stack，清空后3位让它变成8的倍数*/
	sub	sp, #GD_SIZE	/* allocate one GD above SP */
	bic	sp, sp, #7	/* 8-byte alignment for ABI compliance */
	mov	r8, sp		/* GD is above SP */
	mov	r0, #0
	bl	board_init_f //传递参数 r0 = 0

其中全局变量gd的定义在arch/arm/include/asm/global_data.h：

	#define DECLARE_GLOBAL_DATA_PTR     register volatile gd_t *gd asm ("r8")

直接使用了ARM的r8寄存器，ARM的寄存器相比PPC多很多，像PPC的一些扁平设备树的动态接口设计可能就不再需要了吧。

board_init_f定义在board.c，主要服务就是硬件的初始化init_sequence数组，设置gd的信息。

接着crt0.S里面清除BSS段，进一步完善环境，执行board_init_r进入第二阶段的初始化。

这个过程涉及好多知识，在阅读汇编代码的过程中各种翻ARM汇编和ARM寄存器的手册，看得还是不太懂，也涉及到C语言的底层问题例如函数调用与堆栈的变化。先看到这，有时间再硬啃这三个（start.S、crt0.S、relocate.S）汇编文件。