# -*- coding: UTF-8 -*-
import os

class Config(object):

    DEBUG = True
    SECRET_KEY = "lab"
    PERMANENT_SESSION_LIFETIME = 3600 * 24 * 7
    USING_SSL = False

    PROJECT_PATH = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + '\\').replace('\\', '/')

    SITE_DOMAIN = "http://localhost:7000"

    SQLALCHEMY_DATABASE_URI = "sqlite:///%s/db/lab.db" % PROJECT_PATH

    HOST_STRING = "root@182.92.160.85"

    UPLOADS_DEFAULT_DEST = PROJECT_PATH + 'uploads'
    UPLOADS_DEFAULT_URL = 'http://localhost'
    UPLOADS_DEST = PROJECT_PATH + 'uploads/logs/'

    # db
    MCNET_DB = 'sqlite:///%s/db/mcnet.db' % PROJECT_PATH
    MFILE_DB = 'sqlite:///%s/db/morphfile.db' % PROJECT_PATH

    # other config
    DEFAULT_CCNET_CONF_DIR = '/usr/haiwen/ccnet'
    SEAFILE_CONF_DIR = '/usr/haiwen/seafile-data'
    DEFAULT_DIR = '/usr/haiwen/seafile-data'
    SEASERVER_PY_PACKAGE = '/usr/haiwen/seafile-server-3.1.7/seafile/lib64/python2.6/site-packages'

    SEAHUB_DB = '/usr/haiwen/seahub.db'
    SEAFILE_DB = '/usr/haiwen/seafile-data/seafile.db' #可以不配置

    SEAFILE_API_URL = 'http://www.surica.cn/repo/history/'
