# -*- coding: utf-8 -*-
# @Time    : 2020/7/19 21:09
# @Author  : Ruirui
# @File    : cmsScan.py
# @Software: PyCharm

import requests, hashlib, getopt
import threading
import time, sys
import urllib3
urllib3.disable_warnings()

#status_code = False
th = 200
result = '未找到相关cms'
url = ''
dict_md5 = ''
echo = True

def get_cmd_data():
    global url, th, dict_md5
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'u:t:f:h', ['url', 'th', 'file', 'help'])
    except:
        print('格式：cmsScan.py -u <URL> -f <字典文件> -t <线程，默认150线程>')
        sys.exit()
    if '-u' not in [i for i,_ in opts]:
        print('格式：cmsScan.py -u <URL> -f <字典文件> -t <线程，默认150线程>')
        sys.exit()
    elif '-f' not in [i for i,_ in opts]:
        print('格式：cmsScan.py -u <URL> -f <字典文件> -t <线程，默认150线程>')
        sys.exit()

    for i,j in opts:
        if i in ['-u', '--url']:
            url = j
        if i in ['-t', '--th']:
            th = int(j)
        if i in ['-f', '--file']:
            dict_md5 = j
        if i in ['-h', '--help']:
            pass

def get_urlcms_md5(url):
    header = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",}
    req = requests.get(url, headers=header, timeout=1, verify=False).content
    return hashlib.md5(req).hexdigest()

def check(lit):
    global status_code, result
    for i in lit:
        try:
            if get_urlcms_md5(url + i[0]) == i[2]:
                result = i[1]
                #status_code = True
                break
            else:
                if echo:
                    print('[\033[0;33;40mPass\033[0m]' + ' not {} '.format(i[1])+'\033[1;33;40m==>\033[0m'+' URL：{}'.format(url + i[0]))
                    continue
                elif echo:
                    pass
        except:
            if echo:
                print('[\033[0;31;40mError\033[0m]' + ' not {} '.format(i[1])+'\033[1;33;40m==>\033[0m'+' URL：{}'.format(url + i[0]))
                continue
            elif echo:
                pass


def run(th):
    try:
        with open(dict_md5, 'r') as t:
            datas = [i.replace('\n', '').split('|') for i in t]
            threads = []
            bs = int(len(datas) / th)
            for i in range(0, len(datas), bs):
                data = datas[i:i + bs]
                T = threading.Thread(target=check, args=(data,))
                #T.daemon = 1
                T.start()
                threads.append(T)
            for j in threads:
                j.join()

            # while True:
            #     if status_code:
            #         break


    except Exception as e:
        print('文件目录错误 {}'.format(e))
        sys.exit()

def run_time():
    t1 = time.time()
    run(th)
    t2 = time.time()
    return result, str(t2 - t1)[0:4]

if __name__=='__main__':
    print('''
  _____                _____                 
 / ____|              / ____|                
| |     _ __ ___  ___| (___   ___ __ _ _ __  
| |    | '_ ` _ \/ __|\___ \ / __/ _` | '_ \ 
| |____| | | | | \__ \____) | (_| (_| | | | |
 \_____|_| |_| |_|___/_____/ \___\__,_|_| |_|  --by: Ruirui
 
---------------------------------------------------------------------------------------------------------''')
    get_cmd_data()
    time.sleep(1)
    cmsname, ytime = run_time()
    print('---------------------------------------------------------------------------------------------------------')
    print('Webcms：{} 用时{}s'.format(cmsname, ytime))

