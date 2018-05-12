# encoding:utf-8

from exts import db
from datetime import datetime
from jieba.analyse.analyzer import ChineseAnalyzer
import flask_whooshalchemyplus


class User(db.Model):
    """
    用户模型：
    username：用户名
    password：用户密码
    """
    __tablename__ = 'user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)


class Community(db.Model):
    """
    社区帖子模型：
    title：帖子的标题
    context：帖子的内容
    create_time：帖子创建时间(datetime.now:每一次创建模型都会记录时间，datetime.now():第一次创建模型时记录时间)
    author_id:作者id，与User表的id相关联
    """
    __tablename__ = 'community'
    __searchable__ = ['title']
    __analyzer__ = ChineseAnalyzer()
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    context = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    author = db.relationship('User', backref=db.backref('community'))


class Comment(db.Model):
    """
    评论模型：
    context：评论的内容
    create_time:评论创建时间
    community_id：帖子id，和Community的id相关联
    author_id：作者id，和User的id相关联
    """
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    context = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    community_id = db.Column(db.Integer, db.ForeignKey('community.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    community = db.relationship('Community', backref=db.backref('comments'))
    author = db.relationship('User', backref=db.backref('comments'))
