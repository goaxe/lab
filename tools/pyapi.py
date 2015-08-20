# -*- coding: UTF-8 -*-
import sys
import os
import subprocess
import ConfigParser
DEFAULT_CONF_DIR = 'G:\\seafile\\seafile_cilent_build_on_windows\\common_for_dist_m\\bin\\mcnet'
os.environ['CCNET_CONF_DIR'] = DEFAULT_CONF_DIR
os.environ['SEAFILE_CONF_DIR'] = DEFAULT_CONF_DIR
os.environ['SEAFILE_LD_LIBRARY_PATH'] = 'G:/seafile/seafile_cilent_build_on_windows/common_for_dist_m/'
sys.path.append('G:/seafile/seafile_cilent_build_on_windows/common_for_dist_m/lib64/python2.6/site-packages')
os.environ['path'] += 'G:\\seafile\\seafile_cilent_build_on_windows\\common_for_dist_m;'
reload(sys)

DEFAULT_DATA_DIR = 'G:\\seafile\\files'
seafile_datadir = DEFAULT_DATA_DIR
seafile_worktree = seafile_datadir + '\\data'

#print sys.path
import ccnet
# from seaserv import seafile_api

def get_env():
    env = dict(os.environ)
    ld_library_path = os.environ.get('SEAFILE_LD_LIBRARY_PATH', '')
    if ld_library_path:
        env['LD_LIBRARY_PATH'] = ld_library_path

    return env

def run_argv(argv, cwd=None, env=None, suppress_stdout=False, suppress_stderr=False):
    '''Run a program and wait it to finish, and return its exit code. The
    standard output of this program is supressed.

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

def start_mcnet(conf_dir=DEFAULT_CONF_DIR):
    seafile_path = 'G:\\seafile\\files'

    if os.path.exists(conf_dir):
        print "mcnet is already init..."
        return

    cmd = [ "mcnet-init", "-c", conf_dir, "-n", "anonymous" ]
    if run_argv(cmd, env=get_env()) != 0:
        print 'failed to init mcnet'
        # sys.exit(1)

    if not os.path.exists(seafile_path):
        print "%s not exists" % seafile_path
        # sys.exit(0)
    seafile_ini = conf_dir + "\\seafile.ini"
    seafile_data = seafile_path + "\\seafile-data"
    fp = open(seafile_ini, 'w')
    fp.write(seafile_data)
    fp.close()
    print "Writen seafile data directory %s to %s" % (seafile_data, seafile_ini)

def start_all():
    start_mcnet()
    conf_dir = DEFAULT_CONF_DIR
    print "starting ccnet daemon ..."
    cmd = [ "mcnet", "--daemon", "-c", conf_dir ]
    if run_argv(cmd, env=get_env()) != 0:
        print 'CCNet daemon failed to start.'
        sys.exit(1)

    print "Started: ccnet daemon ..."

    conf_dir = DEFAULT_CONF_DIR
    print "starting seafile daemon ..."

    cmd = [ "morf-daemon", "--daemon", "-c", conf_dir, "-d", seafile_datadir,
            "-w", seafile_worktree ]
    if run_argv(cmd, env=get_env()) != 0:
        print 'Failed to start seafile daemon'
        sys.exit(1)

    print "Started: seafile daemon ..."

def get_peer_id():
    pool = ccnet.ClientPool(DEFAULT_CONF_DIR)
    ccnet_rpc = ccnet.CcnetRpcClient(pool)
    info = ccnet_rpc.get_session_info()
    return info.id

print os.environ['path']
start_all()
print get_peer_id()