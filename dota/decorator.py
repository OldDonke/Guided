# encoding:utf-8
from flask import session, redirect,url_for
from functools import wraps


def login_necessary(func):
    '''
    需要登陆后才可以操作的模块装饰器，若没有登陆，跳转至登陆界面
    :param func: 传入的需要登陆的模块
    :return: 跳转至登陆界面
    '''
    @wraps(func)
    def wrappers(*args, **kwargs):
        if session.get('user_name'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrappers
