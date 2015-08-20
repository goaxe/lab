# -*- coding: UTF-8 -*-

from flask import Blueprint, current_app, render_template, redirect, url_for, g, flash, \
    request, make_response, Response
from ..models import db, User, Department
from ..forms.account import LoginForm, ModifyPsw
from ..utils.account import signin_user, signout_user
from ..utils.permissions import require_user
from ..utils.get_server_info import set_user_repo_and_ip
from werkzeug import security
from datetime import datetime
import os

bp = Blueprint('site', __name__)

@bp.route('/', methods=['GET'],  defaults={'page': 1})
@bp.route('/<int:page>')
@require_user
def index(page):
    uid = request.args.get('uid')
    if not uid or g.user.role != 'admin': # 非管理员用户只能看到自己的
        uid = g.user.id
    departs = Department.query
    per = 10
    pages = User.query.filter(User.role == 'client').paginate(page, per, False)
    return render_template('site/index.html', departs=departs, pages=pages, cur=uid), 200

@bp.route('/tt')
def tt():
    c = request.cookies.get('tt')
    print c
    r = Response()
    r.set_cookie('tt', '123')
    return r

@bp.route('/view_log')
def view_log():
    uid = request.args.get('uid')
    if not uid or g.user.role != 'admin': # 非管理员用户只能看到自己的
        uid = g.user.id
    file_name = request.args.get('file_name')
    config = current_app.config
    root = config.get('UPLOADS_DEST') + str(uid) + '/'
    pt = root + file_name
    if not os.path.exists(pt):
        return "文件不存在"
    with open(pt, 'r') as f:
        content = f.read()
    response = make_response(content)
    response.headers['Content-Type'] = 'text/plain; charset=utf-8'
    return response

@bp.route('/download_log')
def download_log():
    uid = request.args.get('uid')
    if not uid or g.user.role != 'admin': # 非管理员用户只能看到自己的
        uid = g.user.id
    file_name = request.args.get('file_name')
    config = current_app.config
    root = config.get('UPLOADS_DEST') + str(uid) + '/'
    pt = root + file_name
    if not os.path.exists(pt):
        return "文件不存在"
    with open(pt, 'r') as f:
        content = f.read()
    response = make_response(content)
    response.headers['Content-Type'] = 'application/octet-stream'
    response.headers['Content-Disposition'] = 'attachment; filename=' + file_name
    return response

@bp.route('/db')
def db_test():
    user = User(name=u'管理员', email='admin@qq.com', password='123456', role='admin')
    user.hash_psw()
    db.session.add(user)
    db.session.commit()
    return '用户人数:%d' % User.query.count()

@bp.route('/test')
def test():
    hsh = security.generate_password_hash('hash1')
    print str(security.check_password_hash(hsh, 'hash1'))
    return render_template('css_test.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        signin_user(form.user, form.permanent.data)
        days = form.user.get_expire_day()
        set_user_repo_and_ip(form.email.data)
        # print days
        if 0 < days < 10:
            flash('你的账号还有%d天就过期，请尽快修改密码' % days)
        else:
            flash('登陆成功')
        return redirect(url_for('site.index'))
    return render_template('site/login.html', form=form, hide_nav=True)

@bp.route('/logout')
def logout():
    if g.user:
        flash('退出')
        signout_user()
    return redirect(url_for('site.index'))

@bp.route('/modify_psw', methods=['GET', 'POST'])
@require_user
def modify_psw():
    uid = request.args.get('uid')
    modify_form = ModifyPsw()
    if modify_form.validate_on_submit():
        user = User.query.get_or_404(uid)
        user.password = modify_form.password.data
        user.hash_psw()
        user.renew_at = datetime.now()
        db.session.commit()
        flash('修改成功，新密码有效期是30天！')
        return redirect(url_for('site.index'))
    return render_template('site/modify_psw.html', modify_form=modify_form, cur=uid)