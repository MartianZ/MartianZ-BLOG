---
layout: post
title: "[Delphi]Lrc歌词模块实现 Part1——格式化Lrc歌词文件"
date: 2011-02-11 22:29
comments: true
categories: notes
---
最近闲来无事，于是准备开发适合一款播放器，必不可少的就是Lrc歌词显示部分

从网上找了一些现成的算法，不是做得很搓，就是做得太霸气，一点都看不懂，于是自己想了一个思路。

1、按行读取LRC歌词，分析每一行的标签 procedure Anylize(s:string)
2、将所有标签整理出来，歌词的时间标签换算成Longint (ToTime)，存到一个动态数组中

	Lyric=record
		Time:Longint; //时间
		Content:string; //内容
		Line:Integer; //第几行，为以后的GDI+滚动显示做准备
	end;
	var
		Lrc:array of Lyric;

3、进行快速排序，按照Time升序排序。

4、播放时不停进行二分查找，将查找出来的结果显示即可。

<!-- more -->

根据这个思路，我们来编写代码

首先来看一段LRC歌词，了解一下LRC歌词的结构：
[ti:Crawling]

[ar:Linkin Park]

[al:Hybrid Theory]

[00:00.00]Linkin Park – Crawling

[00:11.50]

[02:23.74][01:26.89][00:23.40]Crawling in my skin

[02:28.11][01:31.31][00:27.74]These wounds they will not heal

[02:32.58][01:35.70][00:32.35]Fear is how I fall

[02:37.11][01:40.27][00:36.60]Confusing what is real

[00:41.90]

………………

[03:00.99]There’s something inside me that pulls beneath the surface

[03:05.49]Consuming, confusing what is real

[03:09.78]This lack of self control I fear is never ending

[03:14.42]Controlling, confusing what is real

[03:22.93][03:21.08]

[03:26.09]****END****

上面的[ti:Crawling]等等是标识标签(ID-Tags)，用来标示艺人名、歌曲名、专辑名、LRC编者、时间补偿等，对我们来说最有用的是时间补偿，处理也相对简单，不过经过我的测试这个东西实际应用起来不是很多，尤其是从网上下载的歌词，所以暂时不考虑，有兴趣的朋友可以在算法上加上这个时间补偿的处理。

形式为"[mm:ss.ff]"或"[mm:ss.fff]"的标签为时间标签(Time-Tags)，数字都是非负整数，形式也很简单，但是需要注意的是后面毫秒的位数，如果是小于三位的话需要从后面补零。

准备工作完毕，开工！


第一步：

读入Lrc歌词文件。

这个毫无技术含量，与普通文本文件读取方式一样，放到String里即可。

我使用的是TFileStream类读入的文件，不再赘述，大家可以直接谷歌搜索delphi读取文本文件的例子就可以。

第二步：

使用正则表达式，每行每行的分析Lrc文件。

参考正则表达式的手册（- – 每次写正则必须看，那语法简直……），写了一个正则表达式


	^((\[\d+:\d+\.\d+\])+)(.*?)$


这个正则表达式能够一行一行（preMultiLine）的（^$）的匹配含有时间标签的Lrc歌词，同时将正则匹配结果的分组[1]和分组[3]即时时间标签的内容和当前行的歌词内容提取出来，非常方便。需要注意的是每行歌词中可能含有多个时间标签，在正则中使用+限定符即可正常匹配。

实现代码如下：

	procedure Anylize(s:string); //通过正则表达式解析歌词
	const
	 RegEx:string='^((\[\d+:\d+\.\d+\])+)(.*?);' //正则表达式
	var
	 Reg:TPerlRegEx;
	 a,b:String;
	 I,ACount:Integer;
	 AStrings: TStringList;
	begin 	
	Reg:=TPerlRegEx.Create();
	Reg.Options:=[preMultiLine,preCaseLess]; //重要：设置匹配模式：多行
	Reg.Subject:=s;
	Reg.RegEx:=RegEx;
	 try
	   while Reg.MatchAgain do
	   begin
	    a:=Reg.Groups[1]; //时间标签
	    b:=Reg.Groups[3]; //歌词内容
	   	 AStrings:=TStringList.Create;
	    try
	      ACount:=ExtractStrings(['[',']'], [], PChar(a), AStrings);
	      //将时间标签的[]括号替换掉，同时进行文本分割，将多个时间标签分分割成TStringList
	      for I := 0 to ACount-1 do
	      begin
	        SetLength(Lrc,Length(Lrc)+1);
	        //加入成员
	        Lrc[Length(Lrc)-1].Time:=ToTime(AStrings[I]);
	        Lrc[Length(Lrc)-1].Content:=b;
	        //对于单行多个时间标签的情况 自动拆开处理
	        //例如：[02:37.11][01:40.27][00:36.60]Confusing what is real
	        //将识别为三句 即每句分别是
	        //[02:37.11]Confusing what is real
	        //[01:40.27]Confusing what is real
	        //[00:36.60]Confusing what is real
	      end;
	    finally
	      AStrings.Free;
	    end;
	   end;
	 finally
	   Reg.Free;
	 end;

	QuickSort(0, Length(Lrc)-1); //快排
	//Lrc歌词大多数已经局部有序，除非是单行多标签情况或者编写者故意找事，所以使用快排时间复杂度不会很高
	Lrc[0].Line:=3;	
	//设置首行为第三行 这样进行滚动显示时 第一行歌词显示在中间，在以后的篇章中会详细说明
	 LrcInAll:=Lrc[0].Content;
	 for I := 1 to Length(LRC) - 1 do
	 begin
	  Lrc[I].Line:=Lrc[I-1].Line+CalculateLines(I-1);
	  LrcInAll:=LrcInAll+ #13#10 + Lrc[I].Content;
	 end; //将所有歌词都保存一遍
	end;

第三步：

关于将时间标签转换成Longint，只需要将各个部分做乘法然后想加即可

具体实现代码：

	function ToTime(s:string):Longint;
	const
	 RegEx:string='^(\d+):(\d+)(\.(\d+))?;'
	 //使用正则表达式将每部分分别取出来，当然也可以进行字符串分割，我这里比较懒就直接用正则了
	var
	 Reg:TPerlRegEx;
	 ans:Integer;
	 ms:string;
	begin
	 Reg:=TPerlRegEx.Create();
	 try
	   Reg.Options:=[preCaseLess];
	   Reg.Subject:=s;
	   Reg.RegEx:=RegEx;
	   if Reg.Match then
	   begin
	     ms:=Reg.Groups[4];
	     if Length(ms)=1 then ms:=ms+'00';
	     if Length(ms)=2 then ms:=ms+'0'; //对于毫秒，进行补零操作
	     ans:=(StrToInt(Reg.Groups[1]) * 60 * 1000)+(StrToInt(Reg.Groups[2])*1000)+StrToInt(ms);
	   end;
	 finally
	   Reg.Free;
	   Result:=ans;
	 end;
	end;

第四步：

快速排序算法，这个实在是没有什么好说的，排序的目的是为了将歌词按正常顺序全部输出，方便做滚动字幕，同时也方便二分查找。

	procedure QuickSort(const left, right: Integer);
	//QSort 不解释
	  procedure swap(const i, j: Integer);
	  var
	    vT: Integer;
	    vS: String;
	  begin
	    if i = j then Exit;
	    vT := Lrc[i].Time;
	    Lrc[i].Time := Lrc[j].Time;
	    Lrc[j].Time := vT; 
	    vS := Lrc[i].Content;
	    Lrc[i].Content := Lrc[j].Content;
	    Lrc[j].Content := vS;
	  end;
	var
	  vL, vR: Integer;
	begin
	  if left >= right then Exit;
	  vL := left;
	  vR := right + 1;
	  while True do
	  begin
	    while vL + 1 < Length(Lrc) do
	    begin
	      Inc(vL);
	      if Lrc[vL].Time >= Lrc[left].Time then Break;
	    end;
	    while vR - 1 < Length(Lrc) do
	    begin
	      Dec(vR);
	      if Lrc[vR].Time <= Lrc[left].Time then Break;
	    end;
	    if vL >= vR then Break;
	    swap(vL, vR);
	  end;
	  swap(left, vR);
	  QuickSort(left, vR - 1);
	  QuickSort(vR + 1, right);
	end;


这样，我们就已经成功地解析了Lrc歌词，并将它存放在内存（动态数组）里