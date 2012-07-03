---
layout: post
title: "使用WPF创建具有渐变效果的按钮特效"
date: 2011-02-17 22:50
comments: true
categories: notes
---
对于我这样的不会C++，不会GDI+，不精通Photoshop的悲催人士来说，想实现华丽的界面，唯有使用WPF，虽然它属于托管平台，运行效率也非常低，但是在UI设计上确实是非常的给力。

先放一张效果图：

正常状态效果：![WPF](http://i.imgur.com/ubqSI.png)

鼠标悬停效果：![WPF](http://i.imgur.com/eBe4B.png)

<!-- more -->

同时这期间含有的渐变外发光特效，图片上看不出来效果，大家可以下载我的320Kbps音乐下载助手即可看到效果，或者将下文的代码自己调试出来即可。

{% blockquote %}
转载请注明 http://www.4321.la 
{% endblockquote %}

第一步，使用Microsoft Expression Blend 4新建一个WPF 3.5工程，如下图所示：

![WPF](http://i.imgur.com/eBe4B.png)

第二步，使用左侧工具栏添加一个Button到客户区中
![image](http://i.imgur.com/XX26G.png)

![image](http://i.imgur.com/SFaaS.png)

第三步，选中按钮，以此单击菜单对象 – 编辑样式 – 编辑副本

![image](http://i.imgur.com/vMyRj.png)

为了方便以后将相同的样式应用到别的按钮中，推荐选择定义位置为“应用程序”，同时起一个好记的名字：

![image](http://i.imgur.com/pSMiG.png)

单击确定按钮以后，程序会自动打开App.xaml文件，如下图所示：

![image](http://i.imgur.com/anP8m.png)

第四步，切换到XAML编辑模式，通过敲代码来实现一个绚丽的按钮，先实现更改默认的颜色

![image](http://i.imgur.com/DNKaf.png)

切换到XAML模式，顿时就会出现很多的代码（如图），不过微软还是比较仗义的，刷子、属性的名称都是用的比较通俗的英语……没有什么mov啊pop啊push啊什么的……

![image](http://i.imgur.com/4YnYm.png)

首先，先修改ButtonNormalBackground这个LinearGradientBrush（线性渐变刷子，更多信息参考MSDN，传送门），把Windows7/Vista自带的那种灰黑渐变的按钮改成白灰渐变。

系统自动生成的代码是：

	<LinearGradientBrush x:Key="ButtonNormalBackground" EndPoint="0,1" StartPoint="0,0">
	  <GradientStop Color="#F3F3F3" Offset="0"/>
	  <GradientStop Color="#EBEBEB" Offset="0.5"/>
	  <GradientStop Color="#DDDDDD" Offset="0.5"/>
	  <GradientStop Color="#CDCDCD" Offset="1"/>
	</LinearGradientBrush>

将他修改成：


	<LinearGradientBrush x:Key="ButtonNormalBackground" EndPoint="0,1" StartPoint="0,0">
	   <GradientStop Color="#fefefe" Offset="0"/> <!--非鼠标Hover的背景颜色-->
	   <GradientStop Color="#fefefe" Offset="0.5"/>
	   <GradientStop Color="#efefef" Offset="0.5"/>
	   <GradientStop Color="#efefef" Offset="1"/>
	</LinearGradientBrush>

（当然如果有自己喜欢的颜色也可以更改上去，或者也可以多加几个颜色渐变，Color是颜色，Offset是位置）

到这里可以F5运行一下，非鼠标Hover的时候，就已经生效了！

第五步，修改鼠标Hover时候的颜色以及渐变效果

这时候发现下面的代码不给力了，微软没有Hover啊什么的这样的敏感关键词在里面，只能自己原创了……

首先在

	<Style x:Key="ButtonStyle" TargetType="{x:Type Button}">

里面添加

	<Style.Resources>

再添加两个Storyboard，用来显示渐变效果（这种时候还是敲代码最好，不推荐用什么可视化设计器）：

![image](http://i.imgur.com/b6K9I.png)

	<Style.Resources>
	  <Storyboard x:Key="ButtonHover">
	    <DoubleAnimationUsingKeyFrames BeginTime="00:00:00" Storyboard.TargetProperty="(UIElement.BitmapEffect).(OuterGlowBitmapEffect.GlowSize)">
	    <SplineDoubleKeyFrame KeyTime="00:00:00.2000000" Value="5" />
	    </DoubleAnimationUsingKeyFrames>
	  </Storyboard>
	  <Storyboard x:Key="ButtonWithoutHover">
	    <DoubleAnimationUsingKeyFrames BeginTime="00:00:00" Storyboard.TargetProperty="(UIElement.BitmapEffect).(OuterGlowBitmapEffect.GlowSize)">
	    <SplineDoubleKeyFrame KeyTime="00:00:00.1000000" Value="0" />
	    </DoubleAnimationUsingKeyFrames>
	  </Storyboard>
	</Style.Resources>

关于上面的代码的作用，大家可以对照MSDN理解一下，<http://www.microsoft.com/china/MSDN/library/windev/longhorn/storyboardstory.mspx?mfr=true>

然后我们在下面添加两个触发器（Style.Triggers），第一个触发器同时实现两个功能：启动Storyboard，修改按钮颜色；第二个触发器绑定的是IsPressed事件，让按钮按住的时候修改背景颜色为灰色，这样就有按下的感觉。

![image](http://i.imgur.com/a3nO9.png)


		<Style.Triggers>
		<Trigger Property="IsMouseOver" Value="True">
		 <Trigger.ExitActions>
		<BeginStoryboard x:Name="ButtonWithoutHover_BeginStoryboard" Storyboard="{StaticResource ButtonWithoutHover}"/>
		 </Trigger.ExitActions>
		 <Trigger.EnterActions>
		<BeginStoryboard Storyboard="{StaticResource ButtonHover}"/>
		 </Trigger.EnterActions>
		 <Setter Property="Background">
		<Setter.Value>
		 <LinearGradientBrush EndPoint="0,1" StartPoint="0,0">
				 <GradientStop Color="White" Offset="0"/> <!--鼠标Hover的背景颜色-->
				 <GradientStop Color="#fbfcfe" Offset="0.5"/>
				 <GradientStop Color="#d4e8fe" Offset="0.5"/>
				 <GradientStop Color="#fbfcfe" Offset="1"/>
			   </LinearGradientBrush>
		</Setter.Value>
		 </Setter>
		 <Setter Property="Foreground" Value="#FF34AFF6"/>
		   </Trigger>
		   <Trigger Property="IsPressed" Value="True">
			<Trigger.ExitActions>
		   <StopStoryboard BeginStoryboardName="ButtonWithoutHover_BeginStoryboard"/>
			</Trigger.ExitActions>
			<Trigger.EnterActions>
		   <BeginStoryboard x:Name="ButtonWithoutHover_BeginStoryboard1" Storyboard="{StaticResource ButtonWithoutHover}"/>
			</Trigger.EnterActions>
			 <Setter Property="Background" Value="#eaeaea" />
			 <Setter Property="Foreground" Value="Gray"/>
		   </Trigger>
		   </Style.Triggers>

再回头看看两个Storyboard，修改了按钮的OuterGlowBitmapEffect（外发光）特性，注意是修改，所以如果原来不存在这个属性的话，会出错，所以再在Triggers后面添加一个Setter

![image](http://i.imgur.com/0VIsb.png)

	<Setter Property="BitmapEffect">
	  <Setter.Value>
	    <OuterGlowBitmapEffect GlowColor="#9ecaf4" GlowSize="0" />
	  </Setter.Value>
	</Setter>

这时候可以按下F5运行一下看一下效果了。

第六步，修复BUG

这时大家会发现，辛苦自己写的外发光、渐变、背景修改等特效全部又被Windows自带的效果给覆盖了。

其实正是因为我们之前选择编辑样式的时候选择了编辑副本，微软自动把默认的按钮样式给Copy进来了，方便进一步修改，所以新建样式的同时也需要删除掉不需要的样式。

首先将<Setter Property="Template">中的<ControlTemplate.Triggers>删掉，删掉默认的触发器。

![image](http://i.imgur.com/LgBpr.png)

再将Microsoft_Windows_Themes:ButtonChrome里的RenderMouseOver="{TemplateBinding IsMouseOver}" RenderPressed="{TemplateBinding IsPressed}" RenderDefaulted="{TemplateBinding IsDefaulted}"这部分删掉即可。

此时整个

	<Setter Property="Template">

的代码为

	<Setter Property="Template">
	 <Setter.Value>
	  <ControlTemplate TargetType="{x:Type Button}">
	   <Microsoft_Windows_Themes:ButtonChrome x:Name="Chrome" BorderBrush="{TemplateBinding BorderBrush}" Background="{TemplateBinding Background}"  SnapsToDevicePixels="true">
		<ContentPresenter HorizontalAlignment="{TemplateBinding HorizontalContentAlignment}" Margin="{TemplateBinding Padding}" RecognizesAccessKey="True" SnapsToDevicePixels="{TemplateBinding SnapsToDevicePixels}" VerticalAlignment="{TemplateBinding VerticalContentAlignment}"/>
	   </Microsoft_Windows_Themes:ButtonChrome>
	  </ControlTemplate>
	 </Setter.Value>
	</Setter>


完成！

这样我们就实现了一个比较漂亮的按钮的样式，F5运行一下，已经没有BUG了。

扩展，将已有的样式应用到新添加的按钮中

如果需要把新建按钮同时应用这个样式的话，很简单，只需要设置Button的Style="{DynamicResource ButtonStyle}"

如下图所示：

![image](http://i.imgur.com/zO3z0.png)

至此就全部完成了，没手工写API，不用自己搞神马HDC，连Photoshop也没开，敲代码就可以实现非常漂亮的按钮样式。

附录   完工后的XAML按钮样式部分代码：

		<Style x:Key="ButtonFocusVisual">
			<Setter Property="Control.Template">
				<Setter.Value>
					<ControlTemplate>
						<Rectangle Stroke="Black" StrokeDashArray="1 2" StrokeThickness="1" Margin="2" SnapsToDevicePixels="true"/>
					</ControlTemplate>
				</Setter.Value>
			</Setter>
		</Style>
		<LinearGradientBrush x:Key="ButtonNormalBackground" EndPoint="0,1" StartPoint="0,0">
			<GradientStop Color="#fefefe" Offset="0"/> <!--非鼠标Hover的背景颜色-->
			<GradientStop Color="#fefefe" Offset="0.5"/>
			<GradientStop Color="#efefef" Offset="0.5"/>
			<GradientStop Color="#efefef" Offset="1"/>
		</LinearGradientBrush>
		<SolidColorBrush x:Key="ButtonNormalBorder" Color="#FF707070"/>
		<Style x:Key="ButtonStyle" TargetType="{x:Type Button}">
			<Style.Resources>
				<Storyboard x:Key="ButtonHover">
					<DoubleAnimationUsingKeyFrames BeginTime="00:00:00" Storyboard.TargetProperty="(UIElement.BitmapEffect).(OuterGlowBitmapEffect.GlowSize)">
						<SplineDoubleKeyFrame KeyTime="00:00:00.2000000" Value="5" />
					</DoubleAnimationUsingKeyFrames>
				</Storyboard>
		 
				<Storyboard x:Key="ButtonWithoutHover">
					<DoubleAnimationUsingKeyFrames BeginTime="00:00:00" Storyboard.TargetProperty="(UIElement.BitmapEffect).(OuterGlowBitmapEffect.GlowSize)">
						<SplineDoubleKeyFrame KeyTime="00:00:00.1000000" Value="0" />
					</DoubleAnimationUsingKeyFrames>
				</Storyboard>
			</Style.Resources>
			<Style.Triggers>
				<Trigger Property="IsMouseOver" Value="True">
					<Trigger.ExitActions>
						<BeginStoryboard x:Name="ButtonWithoutHover_BeginStoryboard" Storyboard="{StaticResource ButtonWithoutHover}"/>
					</Trigger.ExitActions>
					<Trigger.EnterActions>
						<BeginStoryboard Storyboard="{StaticResource ButtonHover}"/>
					</Trigger.EnterActions>
					<Setter Property="Background">
						<Setter.Value>
							<LinearGradientBrush EndPoint="0,1" StartPoint="0,0">
								<GradientStop Color="White" Offset="0"/> <!--鼠标Hover的背景颜色-->
								<GradientStop Color="#fbfcfe" Offset="0.5"/>
								<GradientStop Color="#d4e8fe" Offset="0.5"/>
								<GradientStop Color="#fbfcfe" Offset="1"/>
							</LinearGradientBrush>
						</Setter.Value>
					</Setter>
					<Setter Property="Foreground" Value="#FF34AFF6"/>
				</Trigger>
				<Trigger Property="IsPressed" Value="True">
					<Trigger.ExitActions>
						<StopStoryboard BeginStoryboardName="ButtonWithoutHover_BeginStoryboard"/>
					</Trigger.ExitActions>
					<Trigger.EnterActions>
						<BeginStoryboard x:Name="ButtonWithoutHover_BeginStoryboard1" Storyboard="{StaticResource ButtonWithoutHover}"/>
					</Trigger.EnterActions>
					<Setter Property="Background" Value="#eaeaea" />
					<Setter Property="Foreground" Value="Gray"/>
				</Trigger>
			</Style.Triggers>
			<Setter Property="BitmapEffect">
				<Setter.Value>
					<OuterGlowBitmapEffect GlowColor="#9ecaf4" GlowSize="0" />
				</Setter.Value>
			</Setter>
			<Setter Property="FocusVisualStyle" Value="{StaticResource ButtonFocusVisual}"/>
			<Setter Property="Background" Value="{StaticResource ButtonNormalBackground}"/>
			<Setter Property="BorderBrush" Value="{StaticResource ButtonNormalBorder}"/>
			<Setter Property="BorderThickness" Value="1"/>
			<Setter Property="Foreground" Value="{DynamicResource {x:Static SystemColors.ControlTextBrushKey}}"/>
			<Setter Property="FontFamily" Value="微软雅黑" />
			<Setter Property="HorizontalContentAlignment" Value="Center"/>
			<Setter Property="VerticalContentAlignment" Value="Center"/>
			<Setter Property="Padding" Value="1"/>
			<Setter Property="Template">
				<Setter.Value>
					<ControlTemplate TargetType="{x:Type Button}">
						<Microsoft_Windows_Themes:ButtonChrome x:Name="Chrome" SnapsToDevicePixels="true" Background="{TemplateBinding Background}" BorderBrush="{TemplateBinding BorderBrush}" >
							<ContentPresenter HorizontalAlignment="{TemplateBinding HorizontalContentAlignment}" Margin="{TemplateBinding Padding}" VerticalAlignment="{TemplateBinding VerticalContentAlignment}" SnapsToDevicePixels="{TemplateBinding SnapsToDevicePixels}" RecognizesAccessKey="True"/>
						</Microsoft_Windows_Themes:ButtonChrome>
					</ControlTemplate>
				</Setter.Value>
			</Setter>
		</Style>