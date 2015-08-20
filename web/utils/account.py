# -*- coding: UTF-8 -*-
from flask import session, request, redirect, current_app
from ..models import User


def signin_user(user, permanent):
    print permanent
    session.permanent = permanent
    session['role'] = user.role
    session['user_id'] = user.id


def signout_user():
    if 'user_id' in session:
        session.pop('user_id', None)
    if 'role' in session:
        session.pop('role', None)


def get_current_user():
    if not 'user_id' in session:
        return None
    user = User.query.filter_by(id=session['user_id']).first()
    if not user:
        signout_user()
        return None
    return user


def redirect_to_ssl():
    """Redirect incoming requests to HTTPS."""
    if request.url.startswith('http://'):
        url = request.url.replace('http://', 'https://', 1)
        code = 302
        r = redirect(url, code=code)
        return r