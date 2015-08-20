# -*- coding: UTF-8 -*-
import random
from datetime import datetime, timedelta
import time
import os
import requests

base_url = "http://localhost:5000/api/"
ip = '192.168.1.31'

def test_upload_speed():
    url = base_url + 'push_upload_speed'
    td = datetime.now() - timedelta(minutes=10)
    ti = time.mktime(td.timetuple())
    r = requests.post(url, data={
        'time': ti,
        'ip': ip,
        'speed': random.randint(100, 300)
    })
    print r.status_code, url, td

def test_disk_status():
    url = base_url + 'push_disk_status'
    t = random.randint(100, 300)
    r = requests.post(url, data={
        'email': 'clangllvm@126.com',
        'total': t + 0.5,
        'used': t - random.randint(0, 100) + 0.01
    })
    print r.status_code, url


def send_log():
    LOG = 'C:/Users/Administrator/mcnet/logs/'

def send_upload_status(n):
    url = base_url + 'push_upload_status'
    t = random.randint(100, 300)
    p = (2000 - n + 80) % 100
    r = requests.post(url, data={
        'email': 'clangllvm@126.com',
        'repo_id': '7ee2b674-5b1a-4f50-934',
        'status': 'u[load',
        'rate': t,
        'percent': p
    })
    print r.status_code, url, str(p) + "%"

def local_usage():
    st = os.statvfs('G:/')
    print st
    pass

def loop():
    n = 2000
    while n > 0:
        # test_upload_speed()
        time.sleep(2)
        # test_disk_status()
        send_upload_status(n)
        n -= 1

# loop()
local_usage()