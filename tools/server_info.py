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

def init_env():
    """
    添加环境变量
    """
    # sys.path.append('/usr/seafile_client/seafile-cli-3.1.5/bin')
    sys.path.append('/usr/haiwen/seafile-server-3.1.7/seafile/lib64/python2.6/site-packages')
    # os.environ['PATH'] += '/usr/seafile_client/seafile-cli-3.1.5/bin:'
    # os.environ['PATH'] += '/usr/haiwen/seafile-server-3.1.7/seafile/bin:'
    # os.environ['SEAFILE_LD_LIBRARY_PATH'] = '/usr/seafile_client/seafile-cli-3.1.5/lib:/usr/seafile_client/seafile-cli-3.1.5/lib64:'
    reload(sys)

init_env()
import seaserv
from seaserv import seafile_api

def get_quota_usage(username):
    # https://github.com/haiwen/seahub/blob/master/seahub/api2/views.py#L310
    used = seafile_api.get_user_self_usage(username) + seafile_api.get_user_share_usage(username)
    total = seafile_api.get_user_quota(username)
    if used > 0:
        used = float(used)
    if total == -2:
        total = float(2)
    elif total > 0:
        total = float(total)
    return used, total

print get_quota_usage('clangllvm@126.com')
print get_quota_usage('1@qq.com')

EMPTY_SHA1 = '0000000000000000000000000000000000000000'

def get_repo_dirents(repo, commit, path, offset=-1, limit=-1):
    dir_list = []
    file_list = []
    dirent_more = False
    if commit.root_id == EMPTY_SHA1:
        return ([], []) if limit == -1 else ([], [], False)
    else:
            if limit == -1:
                dirs = seafile_api.list_dir_by_commit_and_path(commit.repo_id, commit.id, path, offset, limit)
            else:
                dirs = seafile_api.list_dir_by_commit_and_path(commit.repo_id, commit.id, path, offset, limit + 1)
                if len(dirs) == limit + 1:
                    dirs = dirs[:limit]
                    dirent_more = True
    for dirent in dirs:
        file_list.append(dirent)
    dir_list.sort(lambda x, y : cmp(x.obj_name.lower(),
                                        y.obj_name.lower()))
    file_list.sort(lambda x, y : cmp(x.obj_name.lower(),
                                         y.obj_name.lower()))
    if limit == -1:
        return (file_list, dir_list)
    else:
        return (file_list, dir_list, dirent_more)

def test_repo(repo_id):
    repo = seafile_api.get_repo(repo_id)
    print vars(repo)
    current_commit = seaserv.get_commit(repo.id, repo.version, repo.head_cmmt_id)
    print vars(current_commit)
    path = '/'
    file_list, dir_list = get_repo_dirents(repo, current_commit, path)
    for f in file_list:
        print vars(f)

test_repo('7ee2b674-5b1a-4f50-9346-3c1b57dc69d2')
# https://github.com/haiwen/seahub/blob/b51d64d8e7ce056505affb8aa4d6678f2a16df66/seahub/views/__init__.py#L727
# https://github.com/haiwen/seahub/blob/master/seahub/templates/repo_history.html
commits_all = seaserv.get_commits('7ee2b674-5b1a-4f50-9346-3c1b57dc69d2', 0,
                              27)
print commits_all
for commit in commits_all:
    print commit.id, commit.creator_name, commit.props.desc

print seaserv.seafserv_threaded_rpc.get_system_default_repo_id()
# https://github.com/haiwen/seahub/blob/b51d64d8e7ce056505affb8aa4d6678f2a16df66/seahub/views/ajax.py#L1609
# diff
# https://github.com/haiwen/seahub/blob/b51d64d8e7ce056505affb8aa4d6678f2a16df66/seahub/views/__init__.py#L867