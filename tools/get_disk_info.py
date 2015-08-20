# -*- coding: UTF-8 -*-
import os

CLIENT_DEFAULT_DIR = 'C:/Users/Administrator/mcnet'
SEAFILE_WORK_TREE = os.path.join(os.path.dirname(CLIENT_DEFAULT_DIR), "seafile")

def get_fs_info(path):
    """Get free/used/total space info for a filesystem

    :param path: Any dirent on the filesystem
    :returns: A dict containing:

             :free: How much space is free (in bytes)
             :used: How much space is used (in bytes)
             :total: How big the filesystem is (in bytes)
    """
    hddinfo = os.statvfs(path)
    total = hddinfo.f_frsize * hddinfo.f_blocks
    free = hddinfo.f_frsize * hddinfo.f_bavail
    used = hddinfo.f_frsize * (hddinfo.f_blocks - hddinfo.f_bfree)
    return {'total': int(float(total)),
            'free': int(float(free)),
            'used': int(float(used))}

print '/usr/web' + str(get_fs_info('/usr/web'))
print '/home/morph' + str(get_fs_info('/home/morph'))
print '/home/morph/morphfile-data/storage' + str(get_fs_info('/home/morph/morphfile-data/storage'))