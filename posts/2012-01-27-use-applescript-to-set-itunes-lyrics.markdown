---
layout: post
title: "使用AppleScript来自动获取填充iTunes歌曲歌词"
date: 2012-01-27 19:31
comments: true
categories: ideas
---
Martian真的是懒死了⋯⋯Martian既不想开搜索引擎搜歌词，也不想开那内存吃货Xcode来帮忙⋯⋯

于是我就用PHP和AppleScript写了一个小脚本来实现自动获取iTunes的歌曲歌词～

<!-- more -->

脚本源代码：


	--AppleScript By Martian
	--Ver 1.1
	--http://blog.4321.la
	--https://plus.google.com/100204491389909955903/
	--http://twitter.com/martian_zhu
	--http://about.me/martian_z

	property myProgram : "4321.La"
	property baseURL : "http://lyrics.sinaapp.com/"

	--因为我实在是不想操心AppleScript的语法，所以一部分代码采用PHP编写
	--为了获得最好的整理效果，PHP脚本挂在SAE上面，大陆用户的访问速度应该非常不错
	--但是SAE的价格是按照请求次数计费，实在是不便宜，如果您能自己架设PHP服务器并且提供分流服务，我会非常感激！
	--PHP源代码可以见我的博客帖子，里面有说明

	--使用说明：
	--1、打开iTunes，选择要添加歌词的歌曲，可以批量选择
	--2、点击脚本上的“运行”即可，整理结束时iTunes会有提示
	--3、虽然脚本支持批量整理，但是程序自动化整理永远不可能那么智能，不能保证歌曲歌词全部正确，可能需要您后期再次加工
	--4、如果您的歌曲中含有繁体汉字，程序无法自动搜索歌词，这会在后续版本中修正

	tell application "iTunes"
		if selection is not {} then
			set k to count (item of selection)
		else
			return
		end if
	set i to 1
	repeat
		set theTrack to (item i of selection)
		set this_artist to (get artist of theTrack)
		set this_title to (get name of theTrack)
		
		set requestData to "title=" & this_title & "&artist=" & this_artist
		set songLyrics to do shell script "curl -d '" & requestData & "' " & baseURL
		if length of songLyrics > 1 then
			set lyrics of theTrack to songLyrics
		end if
		set i to i + 1
		if i > k then exit repeat
	end repeat
	display dialog return & "整理结束！" buttons {"确定"} default button 1 with icon 1 giving up after 15 with title myProgram
	end tell




###使用说明：

1、打开 应用程序 － 实用工具 － AppleScript编辑器.app

2、将上述代码粘贴进去

**3、然后去看脚本里面的说明进一步操作**





附录：PHP服务端源代码（只在自己搭建服务端需要）：


	<?

	function SingleDecToHex($dec)  { 
	$tmp=""; 
	$dec=$dec%16; 
	if($dec<10) return $tmp.$dec; 
	$arr=array("A","B","C","D","E","F"); 
	return $tmp.$arr[$dec-10]; 
	} 
	function SetToHexString($str)  { 
	if(!$str) return false; 
	$tmp=""; 
	for($i=0;$i<strlen($str);$i++) 
	{ 
		$ord=ord($str[$i]); 
		$tmp.=SingleDecToHex(($ord-$ord%16)/16); 
		$tmp.=SingleDecToHex($ord%16); 
	} 
	return $tmp; 
	} 
	function qianqian_code($str) { 
	$s=strtolower($str); 
        $keys = array(" ","'","(",")","[","]",",",".","'","\""," ", "`", "~", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "=", "+", ",", "<", ".", ">", "/", "?", ";", ":", "\"", "[", "{", "]", "}", "\\", "|", "€","　", "。", "，", "、", "；", "：", "？", "！", "…", "—", "·","ˉ", "¨", "‘", "’", "“", "”", "々", "～", "‖", "∶", "＂", "＇","｀", "｜", "〃", "〔", "〕", "〈", "〉", "《", "》", "「", "」", "『", "』", "．", "〖", "〗", "【", "】", "（", "）", "［", "］","｛", "｝", "≈", "≡", "≠", "＝", "≤", "≥", "＜", "＞", "≮", "≯", "∷", "±","＋", "－", "×", "÷", "／", "∫", "∮", "∝", "∞", "∧", "∨", "∑", "∏", "∪","∩", "∈", "∵", "∴", "⊥", "∥", "∠", "⌒", "⊙", "≌", "∽", "√", "§", "№","☆", "★", "○", "●", "◎", "◇", "◆", "□", "℃", "‰", "■", "△", "▲", "※", "→","←", "↑", "↓", "〓", "¤", "°", "＃", "＆", "＠", "＼", "︿", "＿", "￣", "―","♂", "♀", "Ⅰ", "Ⅱ", "Ⅲ", "Ⅳ", "Ⅴ", "Ⅵ", "Ⅶ", "Ⅷ", "Ⅸ", "Ⅹ", "Ⅺ","Ⅻ", "⒈", "⒉", "⒊", "⒋", "⒌", "⒍", "⒎", "⒏", "⒐", "⒑", "⒒", "⒓","⒔", "⒕", "⒖", "⒗", "⒘", "⒙", "⒚", "⒛", "㈠", "㈡", "㈢", "㈣", "㈤","㈥", "㈦", "㈧", "㈨", "㈩", "①", "②", "③", "④", "⑤", "⑥", "⑦", "⑧", "⑨", "⑩","⑴", "⑵", "⑶", "⑷", "⑸", "⑹", "⑺", "⑻", "⑼", "⑽", "⑾", "⑿", "⒀","⒁", "⒂", "⒃", "⒄", "⒅", "⒆", "⒇", "┌", "┍", "┎", "┏", "┐", "┑", "┒","┓", "─", "┄", "┈", "└", "┕", "┖", "┗", "┘", "┙", "┚", "┛", "━", "┅", "┉","├", "┝", "┞", "┟", "┠", "┡", "┢", "┣", "│", "┆", "┊", "┤", "┥", "┦", "┧", "┨","┩", "┪", "┫", "┃", "┇", "┋", "┬", "┭", "┮", "┯", "┰", "┱", "┲", "┳", "┴", "┵","┶", "┷", "┸", "┹", "┺", "┻", "┼", "┽", "┾", "┿", "╀", "╁", "╂", "╃", "╄", "╅","╆", "╇", "╈", "╉", "╊", "╋");
	foreach ($keys as $key)
        {
        	$s=str_replace($key,"",$s); 
        }
	return SetToHexString(iconv('UTF-8','UTF-16LE',$s));
} 

	function conv($num) { 
	$tp = bcmod($num,4294967296); 

	if(bccomp($num,0)>=0 && bccomp($tp,2147483648)>0) 
	$tp=bcadd($tp,-4294967296); 
	if(bccomp($num,0)<0 && bccomp($tp,2147483648)<0) 
	$tp=bcadd($tp,4294967296); 

	return $tp; 
	} 
	function CodeFunc($Id,$artist,$title) { 
	$Id=(int)$Id; 
	$utf8Str=SetToHexString($artist.$title); 
	$length=strlen($utf8Str)/2; 
	for($i=0;$i<=$length-1;$i++) 
		eval('$song['.$i.'] = 0x'.substr($utf8Str,$i*2,2).';'); 
	$tmp2=0; 
	$tmp3=0; 
	$tmp1 = ($Id & 0x0000FF00) >> 8; //右移8位后为0x0000015F 

	if ( ($Id & 0x00FF0000) == 0 ) { 
		$tmp3 = 0x000000FF & ~$tmp1; //CL 0x000000E7 
	}else { 
		$tmp3 = 0x000000FF & (($Id & 0x00FF0000) >> 16); //右移16位后为0x00000001 
	} 
    $tmp3 = $tmp3 | ((0x000000FF & $Id) << 8); //tmp3 0x00001801 
    $tmp3 = $tmp3 << 8; //tmp3 0x00180100 
    $tmp3 = $tmp3 | (0x000000FF & $tmp1); //tmp3 0x0018015F 
    $tmp3 = $tmp3 << 8; //tmp3 0x18015F00 
    if ( ($Id & 0xFF000000) == 0 ) { 
        $tmp3 = $tmp3 | (0x000000FF & (~$Id)); //tmp3 0x18015FE7 
    } else { 
        $tmp3 = $tmp3 | (0x000000FF & ($Id >> 24)); //右移24位后为0x00000000 
    } 
    $i=$length-1; 
	while($i >= 0){ 
		$char = $song[$i]; 
		if($char >= 0x80) $char = $char - 0x100; 
		$tmp1 = ($char + $tmp2) & 0x00000000FFFFFFFF; 
		$tmp2 = ($tmp2 << ($i%2 + 4)) & 0x00000000FFFFFFFF; 
		$tmp2 = ($tmp1 + $tmp2) & 0x00000000FFFFFFFF; 
		$i -= 1; 
	} 
	$i=0; 
	$tmp1=0; 
	while($i<=$length-1){ 
		$char = $song[$i]; 
		if($char >= 128) $char = $char - 256; 
		$tmp7 = ($char + $tmp1) & 0x00000000FFFFFFFF; 
		$tmp1 = ($tmp1 << ($i%2 + 3)) & 0x00000000FFFFFFFF; 
		$tmp1 = ($tmp1 + $tmp7) & 0x00000000FFFFFFFF; 
		$i += 1; 
    } 
	$t = conv($tmp2 ^ $tmp3); 
	$t = conv(($t+($tmp1 | $Id))); 
	$t = conv(bcmul($t , ($tmp1 | $tmp3))); 
	$t = conv(bcmul($t , ($tmp2 ^ $Id))); 

	if(bccomp($t , 2147483648)>0) 
	$t = bcadd($t , -4294967296); 
	return $t;
	} 
	header("Content-Type:text/html;charset=UTF-8");
        $artist = $_POST["artist"];
        $title = $_POST["title"];
        
	$doc = new DOMDocument(); 
	$doc->load("http://lrccnc.ttplayer.com/dll/lyricsvr.dll?sh?Artist=".qianqian_code($artist)."&Title=".qianqian_code($title)."&Flags=0"); 

	$lrcNode = $doc->getElementsByTagName("lrc"); 
	$code = 0;
	foreach($lrcNode as $lrc) 
	{ 
		
		$artist=$lrc->getAttribute("artist"); 
		$title=$lrc->getAttribute("title"); 
          	if ( ($code == 0)  || strpos($title,"中") || strpos($artist,"中") )
                {
                	$id=$lrc->getAttribute("id"); 
			$code=CodeFunc($id,$artist,$title); 
                        
                }
	
	} 
        
	if ($code != 0)	{
        	$lrcstr=file_get_contents("http://lrccnc.ttplayer.com/dll/lyricsvr.dll?dl?Id=".$id."&Code=".$code); 
         	$lrcstr=preg_replace("/\[(.+?)\]/","",$lrcstr); //替换掉时间标签
          	$lrcstr=preg_replace("/((.*)QQ:(.*))/","",$lrcstr); // 替换联系QQ什么的广告
                $lrcstr=preg_replace("/((.*)QQ：(.*))/","",$lrcstr);
        	echo trim($lrcstr); 
        }


	?>


###本文作者：Martian http://blog.4321.la 转载请注明