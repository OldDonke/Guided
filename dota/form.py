# encoding:utf-8

from flask_wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired


class LoginForm(Form):
    """
    登陆表单，用于认证用户
    openid：由OpenID提供者完成的登陆验证
    remember_me：让用户选择是否能在他们的网页浏览器中种植cookie
    """
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class SearchForm(Form):
    """
    搜索表单，用于搜索相关帖子
    search:查找的内容
    """
    search = StringField('search', validators=[DataRequired()])
