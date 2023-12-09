import subprocess
import random
import sys
import re
import os
from multiprocessing import Pool, cpu_count

plugins_path = "/home/kali/volatility/volatility/plugins"

def random_emoji():
    emoji_list = ['🎉', '🚀', '🚩', '💥', '🔥', '💭', '🎯', '🤗', '💖']
    return random.choice(emoji_list)

def run_vol_command(args):
    key, value, image_path, profile, plugins_path, dir_path = args
    print(f"{random_emoji()} 当前进行的任务为:{key}")
    try:
        command = f'python2 /home/kali/volatility/vol.py --plugins={plugins_path} -f {image_path} --profile={profile} {value} > {dir_path}/{value}.txt'
        subprocess.run(command, shell=True, stderr=subprocess.PIPE, universal_newlines=True)
        print(f"✅ {key}已执行完成")
    except Exception as e:
        print(f"😭 {key}任务执行出现了一点问题, Error: {e}")

try:
    image_path = sys.argv[1]
    image_name = image_path.split('/')[-1]
except:
    sys.exit("😢 请输入待分析的内存镜像的路径...")

profile_command = f'python2 /home/kali/volatility/vol.py -f {image_path} imageinfo'
print(f"🥰 开始分析{image_name},请稍候...")
res = subprocess.check_output(profile_command, shell=True, stderr=subprocess.PIPE, universal_newlines=True)
p = re.compile(r"Profile\(s\) : (.*),")
profiles = p.findall(res)[0].split(', ')
print("🌟 该内存镜像可能的版本为：")
for index,profile in enumerate(profiles):
    print(f"[{index+1}] {profile}")
    
profile_index = int(input("🎯 请选择内存镜像的Profile："))
print(f"✅ Profile:{profiles[profile_index-1]}选择成功，开始分析...")
vol_command = {'列出系统中所有的ATOM表': 'atoms', 
               '扫描所有的ATOM表': 'atomscan', 
               '显示系统的安全审计策略': 'auditpol', 
               '从BIOS中提取键盘缓冲区': 'bioskbd', 
               '列出所有的回调函数': 'callbacks', 
               '显示剪贴板内容': 'clipboard', 
               '显示进程的命令行参数': 'cmdline', 
               '扫描所有进程的内存，查找所有的命令行参数': 'cmdscan', 
               '列出所有的控制台窗口': 'consoles', 
               '显示有关崩溃的信息': 'crashinfo', 
               '扫描所有进程的内存，查找所有的桌面句柄': 'deskscan', 
               '显示系统的设备树': 'devicetree', 
               '列出进程加载的所有DLL': 'dlllist', 
               '列出所有的驱动程序IRP': 'driverirp', 
               '列出所有的驱动程序模块': 'drivermodule', 
               '扫描内核内存，查找所有的驱动程序': 'driverscan', 
               '扫描所有进程的内存，查找所有的编辑框': 'editbox', 
               '显示进程的环境变量': 'envars', 
               '列出所有的GDI定时器': 'gditimers', 
               '列出所有的系统中的SID': 'gitsids', 
               '列出所有的注册表键': 'hivelist', 
               '显示InternetExplorer的历史记录': 'iehistory', 
               '列出所有的作业和进程之间的链接': 'joblinks', 
               '列出所有的LDR_MODULE结构': 'ldrmodules', 
               '查找可能的恶意软件进程': 'malfind', 
               '扫描所有的模块': 'modscan', 
               '列出所有的模块': 'modules', 
               '扫描内存中的网络连接': 'netscan', 
               '扫描所有的记事本句柄': 'notepad', 
               '扫描所有的对象类型': 'objtypescan', 
               '显示注册表键的内容': 'printkey', 
               '列出所有进程': 'pslist', 
               '扫描内存中的进程': 'psscan', 
               '显示进程之间的父子关系': 'pstree', 
               '显示隐藏进程': 'psxview', 
               '列出所有的会话': 'sessions', 
               '显示应用程序兼容性缓存': 'shimcache', 
               '显示系统关闭时间': 'shutdowntime', 
               '列出所有的套接字': 'sockets', 
               '扫描内存中的套接字': 'sockscan', 
               '列出所有的服务': 'svcscan', 
               '显示用户最近使用的文件和程序': 'userassist',
               '扫描进程缓存的文件':'filescan',
               '使用mimikatz插件爆破用户名和密码':'mimikatz',
               '使用usbstor插件获取USB连接信息':'usbstor',
               '获取内存镜像的基本信息':'imageinfo',
               '获取chrome的浏览记录':'chromehistory'
               }

dir_path = image_path.replace(image_name, "vol_output")
os.makedirs(dir_path, exist_ok=True) # 当目标目录已存在时,不新建目录

num_cores = cpu_count()  # 获取CPU核心数量
# 使用该核心数量初始化Pool
with Pool(processes=num_cores) as p:
    args_list = [(key, value, image_path, profiles[profile_index-1], plugins_path, dir_path) for key, value in vol_command.items()]
    p.map(run_vol_command, args_list)
