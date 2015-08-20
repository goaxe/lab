# -*- coding: UTF-8 -*-
from .default import Config

class ProductionConfig(Config):
     DEBUG = True

     SQLALCHEMY_DATABASE_URI = "mysql://root:root@localhost/lab"

     # other config
     DEFAULT_CCNET_CONF_DIR = '/home/madsys/morph_deploy/morph/mcnet'
     SEAFILE_CONF_DIR = '/home/madsys/morph_deploy/morph/morphfile-data'
     DEFAULT_DIR = '/home/madsys/morph_deploy/morph/morphfile-data'
     SEASERVER_PY_PACKAGE = '/usr/local/lib/python2.7/site-packages'

     SEAHUB_DB = 'mysql://root:root@localhost/morphweb-db'
     SEAFILE_DB = 'mysql://root:root@localhost/morphfile-db' #可以不配置

     SEAFILE_API_URL = 'https://192.168.1.203/repo/history/'
     HOST_URI = '192.168.1.201'
     SITE_DOMAIN = "http://192.168.0.201:7000/"


