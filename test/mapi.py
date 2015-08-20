# -*- coding: UTF-8 -*-
DEFAULT_CONF_DIR = '/home/morph/mcnet'
SEAFILE_CONF_DIR = '/home/morph/morphfile-data'
DEFAULT_DIR = '/home/morph/morphfile-data'
SEASERVER_PY_PACKAGE = '/usr/local/lib/python2.7/site-packages'

SEAHUB_DB = '/usr/haiwen/seahub.db'
SEAFILE_DB = '/usr/haiwen/seafile-data/seafile.db' #可以不配置

import os
import sys
os.environ['MCNET_CONF_DIR'] = DEFAULT_CONF_DIR
os.environ['MORPHFILE_CONF_DIR'] = SEAFILE_CONF_DIR
sys.path.append(SEASERVER_PY_PACKAGE)
reload(sys)

from morphserv import morphfile_api

def get_quota_usage(username):
    # https://github.com/haiwen/seahub/blob/master/seahub/api2/views.py#L310
    used = morphfile_api.get_user_self_usage(username) + morphfile_api.get_user_share_usage(username)
    total = morphfile_api.get_user_quota(username)
    if used > 0:
        used = float(used)
    else:
        used = 0
    if total > 0:
        total = float(total)
    else:
        total = float(2 * (1 << 30))
    return used, total

print get_quota_usage('1@qq.com')