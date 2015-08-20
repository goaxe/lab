# -*- coding: UTF-8 -*-
import os
import sys
import subprocess
import time
import requests
import traceback
import json

SEAF_CLI_VERSION = '3.5.5'
DEFAULT_CONF_DIR = "/usr/seafile_client/tconf"
# DEFAULT_CONF_DIR = '/usr/haiwen/ccnet'
SEAFILE_CONF_DIR = '/usr/haiwen/seafile-data'
DEFAULT_DIR = "/usr/seafile_client/data/"
# DEFAULT_DIR = '/usr/haiwen/seafile-data'
BIN_PATH = "/usr/seafile_client/seafile-cli-3.1.5/bin/"
seafile_datadir = DEFAULT_DIR
seafile_worktree = os.path.join(os.path.dirname(seafile_datadir), "seafile")

repo_id = '714a45ac-80b5-4841-a224-99e98ec7b883'

def init_env():
    """
    添加环境变量
    """
    sys.path.append('/usr/seafile_client/seafile-cli-3.1.5/bin')
    sys.path.append('/usr/seafile_client/seafile-cli-3.1.5/lib64/python2.6/site-packages')
    os.environ['PATH'] += '/usr/seafile_client/seafile-cli-3.1.5/bin:'
    os.environ['PYTHONPATH'] = '/usr/seafile_client/seafile-cli-3.1.5/lib64/python2.6/site-packages'
    os.environ['PATH'] += '/usr/haiwen/seafile-server-3.1.7/seafile/bin:'
    os.environ['SEAFILE_LD_LIBRARY_PATH'] = '/usr/seafile_client/seafile-cli-3.1.5/lib:/usr/seafile_client/seafile-cli-3.1.5/lib64:'
    reload(sys)

init_env()
import ccnet
import seafile

def get_env():
    env = dict(os.environ)
    ld_library_path = os.environ.get('SEAFILE_LD_LIBRARY_PATH', '')
    if ld_library_path:
        env['LD_LIBRARY_PATH'] = ld_library_path

    return env

def run_argv(argv, cwd=None, env=None, suppress_stdout=False, suppress_stderr=False):
    '''Run a program and wait it to finish, and return its exit code. The
    standard output of this program is supressed.
    http://stackoverflow.com/questions/6735917/redirecting-stdout-to-nothing-in-python
    '''
    with open(os.devnull, 'w') as devnull:
        if suppress_stdout:
            stdout = devnull
        else:
            stdout = sys.stdout

        if suppress_stderr:
            stderr = devnull
        else:
            stderr = sys.stderr

        proc = subprocess.Popen(argv,
                                cwd=cwd,
                                stdout=stdout,
                                stderr=stderr,
                                env=env)
        return proc.wait()

def start_ser():
    """
    start ccnet
    """
    ccnet_conf_dir = DEFAULT_CONF_DIR
    if os.path.exists(ccnet_conf_dir):
        print "%s is exists" % ccnet_conf_dir
    else:
        cmd = [BIN_PATH + "ccnet-init", "-c", ccnet_conf_dir, "-n", "anonymous" ]
        if run_argv(cmd, env=get_env()) != 0:
            print 'failed to init ccnet'
            sys.exit(1)
    _start_ccnet()
    time.sleep(1)
    _start_seafile()

def _start_ccnet():
    conf_dir = DEFAULT_CONF_DIR
    print "starting ccnet daemon ..."
    cmd = [BIN_PATH + "ccnet", "--daemon", "-c", conf_dir ]
    if run_argv(cmd, env=get_env()) != 0:
        print 'CCNet daemon failed to start.'
        sys.exit(1)

    print "Started: ccnet daemon ..."

def _start_seafile():
    conf_dir = DEFAULT_CONF_DIR
    print "starting seafile daemon ..."

    cmd = [BIN_PATH + "seaf-daemon", "--daemon", "-c", conf_dir, "-d", seafile_datadir,
            "-w", seafile_worktree ]
    if run_argv(cmd, env=get_env()) != 0:
        print 'Failed to start seafile daemon'
        sys.exit(1)

    print "Started: seafile daemon ..."

def stop_ser():
    conf_dir = DEFAULT_CONF_DIR
    pool = ccnet.ClientPool(conf_dir)
    client = pool.get_client()
    try:
        client.send_cmd("shutdown")
        print 'stop ccnet and daemon'
    except Exception:
        # ignore NetworkError("Failed to read from socket")
        # print "Error: Failed to read from socket"
        pass

def get_rpc_client():
    pool = ccnet.ClientPool(DEFAULT_CONF_DIR)
    ccnet_rpc = ccnet.CcnetRpcClient(pool)
    seafile_rpc = seafile.RpcClient(pool, req_pool=False)
    return ccnet_rpc

def get_searpc_client():
    pool = ccnet.ClientPool(DEFAULT_CONF_DIR)
    seafile_rpc = seafile.RpcClient(pool, req_pool=False)
    return seafile_rpc

def get_peer_id():
    pool = ccnet.ClientPool(DEFAULT_CONF_DIR)
    ccnet_rpc = ccnet.CcnetRpcClient(pool)
    info = ccnet_rpc.get_session_info()
    print vars(info)
    return info.id

def get_token(url, username, password):
    platform = 'linux'
    device_id = get_peer_id()
    device_name = 'terminal-' + os.uname()[1]
    client_version = SEAF_CLI_VERSION
    platform_version = ''
    data = {
        'username': username,
        'password': password,
        'platform': platform,
        'device_id': device_id,
        'device_name': device_name,
        'client_version': client_version,
        'platform_version': platform_version,
    }
    token_json = requests.post("%s/api2/auth-token/" % url, data=data).text
    tmp = json.loads(token_json)
    token = tmp['token']
    return token

def get_repo_downlod_info(url, token):
    headers = { 'Authorization': 'Token %s' % token }
    repo_info = requests.post(url, headers=headers).text
    return json.loads(repo_info)

def test():
    # 测试ccnet rpc api
    rpc = get_rpc_client()
    peer = rpc.get_peer('b3910ffdcac4f464ed3e3b1392fae1169ddf1437')
    print "peer", vars(peer)
    print rpc.list_peers()
    print "roles", rpc.get_peers_by_role()
    # print rpc.count_procs_alive() #无法调用
    # print rpc.list_peer_stat(-1, -1) 无法调用
    # print get_peer_id()
    # print get_token('http://104.131.130.151', 'clangllvm@126.com', 'naruto2013')
    seafile_rpc = get_searpc_client()
    repos = seafile_rpc.get_repo_list(-1, -1)
    print "Name\tID\tPath"
    for repo in repos:
        print repo.name, repo.id, repo.worktree
    tasks = seafile_rpc.get_clone_tasks()
    print "# Name\tStatus\tProgress"
    for task in tasks:
        if task.state == "fetch":
            tx_task = seafile_rpc.find_transfer_task(task.repo_id)
            print "%s\t%s\t%d/%d, %.1fKB/s" % (task.repo_name, "downloading",
                                        tx_task.block_done, tx_task.block_total,
                                        tx_task.rate/1024.0)
        elif task.state == "checkout":
            checkout_task = seafile_rpc.get_checkout_task(task.repo_id)
            print "%s\t%s\t%d/%d" % (task.repo_name, "checkout",
                                   checkout_task.finished_files,
                                   checkout_task.total_files)
        elif task.state == "error":
            tx_task = seafile_rpc.find_transfer_task(task.repo_id)
            if tx_task:
                err = tx_task.error_str
            else:
                err = task.error_str
            print "%s\t%s\t%s" % (task.repo_name, "error", err)
        elif task.state == 'done':
            # will be shown in repo status
            pass
        else:
            print "%s\t%s" % (task.repo_name, "unknown")
    # os.environ['CCNET_CONF_DIR'] = DEFAULT_CONF_DIR
    # os.environ['SEAFILE_CONF_DIR'] = SEAFILE_CONF_DIR
    # from seaserv import seafile_api
    # print seafile_api.get_repo_size(repo_id)

def main():
    try:
        # start_ser()
        test()
    except Exception, e:
        print e, traceback.format_exc()
        # stop_ser()

if __name__ == '__main__':
    main()