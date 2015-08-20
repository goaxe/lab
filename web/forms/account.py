# -*- coding: UTF-8 -*-
from flask_wtf import Form
from wtforms import TextField, RadioField, SelectField, PasswordField, BooleanField, HiddenField
from wtforms.validators import DataRequired, InputRequired, Email
from ..models import Department, User


class DepartmentForm(Form):
    name = TextField('部门名', validators=[DataRequired('部门名称不能为空')], description='部门')

    def validate_name(self, filed):
        dp = Department.query.filter_by(name=filed.data).first()
        if dp:
            raise ValueError('部门名称不能重复')


class LoginForm(Form):
    """
    label validators descriptions
    """
    email = TextField('', validators=[Email('无效的邮箱')], description='邮箱')
    password = PasswordField('', validators=[DataRequired('密码不能为空')], description='密码')
    permanent = BooleanField('一周内自动登录')

    def validate_password(self, field):
        email = self.email.data.replace(' ', '')
        user = User.query.filter_by(email=email).first()
        if not user:
            raise ValueError('账户或密码错误')
        if user.check_psw(field.data):
            if not user.check_renew() and user.role != 'admin':
                # 管理员账号不会过期
                raise ValueError('你的账号已经超过30天没修改密码，请联系管理员修改密码')
            self.user = user
        else:
            raise ValueError('账户或密码错误')


class UserForm(Form):
    name = TextField('用户名', validators=[DataRequired('用户名不能为空')])
    email = TextField('邮箱', validators=[Email('无效的邮箱')])
    password = PasswordField('密码', validators=[DataRequired('密码不能为空')])
    confirm_psw = PasswordField('确认密码', validators=[DataRequired('请确认密码')])
    contact = TextField('联系方式')
    ip = TextField('ip地址')
    role = RadioField('身份', choices=[('admin', '管理员'), ('client', '普通用户')],
                      validators=[InputRequired('请选择身份')], default='client')
    depart_id = SelectField('选择部门', coerce=int, validators=[DataRequired('请选择部门')])

    def validate_email(self, field):
        user = User.query.filter(User.email == field.data).first()
        if user:
            raise ValueError('该邮箱已经被使用')

    def validate_password(self, field):
        if field.data != self.confirm_psw.data:
            raise ValueError('两次输入的密码不一致')
        if len(field.data) < 5:
            raise ValueError('密码长度不能少于5位')


class ModifyUserForm(UserForm):
    password = PasswordField('密码', )
    confirm_psw = PasswordField('确认密码', )

    def __init__(self):
        super(UserForm, self).__init__()

    def validate_email(self, field):
        pass

    def validate_password(self, field):
        if field.data:
            super(ModifyUserForm, self).validate_password(field)


class ModifyPsw(Form):
    password = PasswordField('密码', validators=[DataRequired('密码不能为空')])
    confirm_psw = PasswordField('确认密码', validators=[DataRequired('请确认密码')])

    def validate_password(self, field):
        if field.data != self.confirm_psw.data:
            raise ValueError('两次输入的密码不一致')
        if len(field.data) < 6:
            raise ValueError('密码长度不能少于6位')