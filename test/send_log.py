# -*- coding: UTF-8 -*-
import os
import requests

DIR = 'C:/Users/Administrator/mcnet/logs/'
base_url = "http://localhost:5000/api/"
# base_url = "http://166.111.131.62:5000/api/"
email = '1@qq.com'

def get_all_log():
    root = DIR
    items = os.listdir(root)

    files = []
    for t in items:
        pt = root + t
        # print pt
        # 忽略隐藏文件或者文件夹
        if t.startswith('.') or os.path.isdir(pt):
            # print root + t
            continue
        files.append(t)
    return files


def send_logs():
    files = get_all_log()
    url = base_url + 'send_log'
    for name in files:
        # print name
        f = open(DIR + name, 'r')
        r = requests.post(url, data={
            'email': email,
            'name': name
        }, files={'log': f.read()})
        f.close()
        print r.text, name, url

send_logs()