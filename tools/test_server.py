# -*- coding: UTF-8 -*-
import sys
import subprocess
import time
import os
import stat
DEFAULT_CONF_DIR = '/usr/haiwen/ccnet'
SEAFILE_CONF_DIR = '/usr/haiwen/seafile-data'
DEFAULT_DIR = '/usr/haiwen/seafile-data'
os.environ['CCNET_CONF_DIR'] = DEFAULT_CONF_DIR
os.environ['SEAFILE_CONF_DIR'] = SEAFILE_CONF_DIR

seafile_datadir = DEFAULT_DIR
seafile_worktree = os.path.join(os.path.dirname(seafile_datadir), "seafile")
repo_id = '714a45ac-80b5-4841-a224-99e98ec7b883'

def init_env():
    """
    添加环境变量
    """
    sys.path.append('/usr/seafile_client/seafile-cli-3.1.5/bin')
    sys.path.append('/usr/seafile_client/seafile-cli-3.1.5/lib64/python2.6/site-packages')
    # os.environ['PATH'] += '/usr/seafile_client/seafile-cli-3.1.5/bin:'
    os.environ['PATH'] += '/usr/haiwen/seafile-server-3.1.7/seafile/bin:'
    os.environ['SEAFILE_LD_LIBRARY_PATH'] = '/usr/seafile_client/seafile-cli-3.1.5/lib:/usr/seafile_client/seafile-cli-3.1.5/lib64:'
    reload(sys)

init_env()
from seaserv import seafile_api

def count_files_recursive(repo_id, path='/'):
    num_files = 0
    for e in seafile_api.list_dir_by_path(repo_id, path):
        if stat.S_ISDIR(e.mode):
            num_files += count_files_recursive(repo_id,
                                               os.path.join(path, e.obj_name))
        else:
            num_files += 1
    return num_files

#Get library ID from input
origin_repo_id = repo_id

#Get origin_repo object
origin_repo = seafile_api.get_repo(origin_repo_id)
username = seafile_api.get_repo_owner(origin_repo_id)

# print vars(origin_repo)
#Create a new library, set name, desc and owner
new_repo_id = seafile_api.create_repo(name=origin_repo.name,
                                      desc=origin_repo.desc,
                                      username=username, passwd=None)

#Copy stuffs from old library to new library
# dirents = seafile_api.list_dir_by_path(origin_repo_id, '/')
# for e in dirents:
#     print "copying: " + e.obj_name
#     obj_name = e.obj_name
#     seafile_api.copy_file(origin_repo_id, '/', obj_name, new_repo_id, '/',
#                           obj_name, username, 0, 1)

print "*" * 60
print "OK, verifying..."
print "Origin library(%s): %d files. New Library(%s): %d files." % (
    origin_repo_id[:8], count_files_recursive(origin_repo_id),
    new_repo_id[:8], count_files_recursive(new_repo_id))
print "*" * 60
# print seafile_api.get_repo(repo_id)
print seafile_api.get_repo_size(repo_id)

# import ccnet
# import seafile
# pool = ccnet.ClientPool(DEFAULT_CONF_DIR)
# ccnet_rpc = ccnet.CcnetRpcClient(pool)
# seafile_rpc = seafile.RpcClient(pool, req_pool=False)
# repos = seafile_rpc.get_repo_list(-1, -1)
# print "Name\tID\tPath"
# for repo in repos:
#     print repo.name, repo.id, repo.worktree