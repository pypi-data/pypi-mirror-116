# -*- coding: utf-8 -*-
# @Time    : 2021/8/9 9:04
# @Author  : liumingming
# @FileName: __init__.py.py
# @Company ：http://www.iqi-inc.com/

import platform

from AiDragonfly.aiqi_main import *

run_system = platform.system()

if run_system == "Darwin":
    pass
elif run_system == "Windows":
    platform.release()
    if platform.release() == '10':
        pass
        win_ver = platform.version()
        win_verlist = win_ver.split('.')
        ver_h = win_verlist[0]
        ver_M = win_verlist[1]
        ver_L = win_verlist[2]
        print(run_system + " " + platform.release() + ' ' + platform.version())
    else:
        print(run_system+" "+platform.release()+' '+platform.version())
        print('系统不支持')
        sys.exit('系统不支持')
    pass
else:
    print('系统不支持')
    sys.exit('系统不支持')

