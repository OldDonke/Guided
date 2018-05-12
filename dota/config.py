# encoding:utf-8

import os
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

SECRET_KEY = os.urandom(24)

# 激活跨站点请求伪造保护
CSRF_ENABLED = True

# 返回的最大搜索结果数量
MAX_SEARCH_RESULTS = 50

WHOOSH_BASE = os.path.join(basedir, 'dota.db')

DIALECT = 'mysql'
DRIVER = 'mysqldb'
USERNAME = 'root'
PASSWORD = 'root'
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'dota'
DB_URI = '{}+{}://{}:{}@{}:{}/{}'.format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
