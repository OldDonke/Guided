# encoding:utf-8

from flask import Flask, render_template, request, redirect, url_for, session, g
from exts import db
from model import User, Community, Comment
import config
from decorator import login_necessary
import flask_whooshalchemyplus

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
flask_whooshalchemyplus.init_app(app)
with app.app_context():
    db.create_all()


@app.route('/')
def index():
    """主页：显示所有帖子"""
    context = {
        'community_context': Community.query.order_by('-create_time').all()
    }
    flask_whooshalchemyplus.index_one_model(Community)
    return render_template('index.html', **context)


@app.route('/search/', methods=['POST'])
def search():
    """
    搜索功能，只搜帖子的title
    :return: 包含所有result的内容
    """
    if not request.form.get('search'):
        return redirect(url_for('index'))
    query = request.form.get('search')
    results = Community.query.whoosh_search(query).all()
    return render_template('searchResult.html', results=results)


"""
@app.route('/s/<query>')
def search_result(query):
    results = Community.query.whoosh_search(query).all()
    return render_template('searchResult.html', results=results)
"""


@app.route('/question/', methods=['GET', 'POST'])
@login_necessary
def question():
    """发帖页面：说出你的想法"""
    if request.method == 'GET':
        return render_template('question.html')
    else:
        title = request.form.get('title')
        context = request.form.get('context')
        community = Community(title=title, context=context)
        user_name = session.get('user_name')
        user = User.query.filter(User.username == user_name).first()
        community.author = user
        db.session.add(community)
        db.session.commit()
        return redirect(url_for('index'))


@app.route('/d/<community_id>')
def question_detail(community_id):
    """帖子详情页面：显示具体内容，同时可以进行评论"""
    content = {
        'community': Community.query.filter(Community.id == community_id).first()
    }
    return render_template('detail.html', **content)


@app.route('/add_comment/', methods=['POST'])
@login_necessary
def add_comment():
    """添加评论操作"""
    context = request.form.get('comment')
    comment = Comment(context=context)
    community_id = request.form.get('community_id')
    community = Community.query.filter(Community.id == community_id).first()
    comment.community = community
    username = session.get('user_name')
    author = User.query.filter(User.username == username).first()
    comment.author = author
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('question_detail', community_id=community_id))


@app.route('/login/', methods=['GET', 'POST'])
def login():
    """登陆页面：进行简单的登陆操作"""
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter(User.username == username).first()
        if user:
            if user.password == password:
                session['user_name'] = username
                # cookie保存功能,31天免登陆
                # session.permanent = True
                return redirect(url_for('index'))
            else:
                return u'密码输入有误'
        else:
            return u'用户不存在，请去注册'


@app.route('/regist/', methods=['GET', 'POST'])
def regist():
    """注册页面：进行简单的注册操作"""
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        # 检测用户名是否被注册
        username_test = User.query.filter(User.username == username).first()
        if username_test:
            return u'用户名已被注册，try again'
        else:
            if password != password2:
                return u'两次密码输入不一致，try again'
            elif password == '':
                return u'密码不能为空'
            else:
                user_new = User(username=username, password=password)
                db.session.add(user_new)
                db.session.commit()
                return redirect(url_for('login'))


@app.route('/signout/')
def signout():
    """登出操作"""
    # 清除cookie
    session.clear()
    return redirect(url_for('login'))


@app.context_processor
def user_context_processor():
    """
    钩子函数
    在每一次模版渲染之前查找session中是否存在用户名。
    :return: 用户实例的字典或空字典
    """
    username = session.get('user_name')
    if username:
        user = User.query.filter(User.username == username).first()
        if user:
            return {'user': user}
    return {}


if __name__ == '__main__':
    app.run()
