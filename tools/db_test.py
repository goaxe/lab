# -*- coding: UTF-8 -*-
import sqlite3

# http://www.cnblogs.com/yuxc/archive/2011/08/18/2143606.html
# DB = 'G:/py/lab/db/morphfile.db'
DB = '/usr/haiwen/seafile-data/seafile.db'
# DB = '/usr/haiwen/seahub.db'

sql = "select peer_ip from RepoTokenPeerInfo join RepoUserToken on RepoTokenPeerInfo.token = RepoUserToken.token where RepoUserToken.email = %s" % '1@qq.com'
def get_ip(email):
    DB = '/usr/haiwen/seafile-data/seafile.db'
    cx = sqlite3.connect(DB)
    cu = cx.cursor()
    cu.execute("select peer_ip from RepoTokenPeerInfo join RepoUserToken on RepoTokenPeerInfo.token = RepoUserToken.token where RepoUserToken.email = :email group by peer_ip", {'email': email})
    print cu.fetchall()

def get_ip_from_seahub(email):
    DB = '/usr/haiwen/seahub.db'
    cx = sqlite3.connect(DB)
    cu = cx.cursor()
    cu.execute("select last_login_ip from api2_tokenv2 where user = :email order by last_accessed desc limit 1", {'email': email})
    print cu.fetchall()

get_ip('clangllvm@126.com')
get_ip('1@qq.com')
get_ip_from_seahub('clangllvm@126.com')
get_ip_from_seahub('1@qq.com')