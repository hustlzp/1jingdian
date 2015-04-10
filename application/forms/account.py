# coding: utf-8
from flask import g
from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo
from ..models import User, InvitationCode


class SigninForm(Form):
    """Form for signin"""
    email = StringField('邮箱',
                        validators=[
                            DataRequired('邮箱不能为空'),
                            Email('邮箱格式错误')
                        ])

    password = PasswordField('密码',
                             validators=[DataRequired('密码不能为空')])

    def validate_email(self, field):
        user = User.query.filter(User.email == self.email.data).first()
        if not user:
            raise ValueError("账户不存在")

    def validate_password(self, field):
        if self.email.data:
            user = User.query.filter(User.email == self.email.data).first()
            if not user or not user.check_password(self.password.data):
                raise ValueError('密码错误')
            else:
                self.user = user


class SignupForm(Form):
    """Form for signin"""
    code = StringField('邀请码',
                       validators=[DataRequired('邀请码不能为空')])

    name = StringField('用户名',
                       validators=[DataRequired('用户名不能为空')])

    email = StringField('邮箱',
                        validators=[
                            DataRequired(message="邮箱不能为空"),
                            Email(message="无效的邮箱")
                        ])

    password = PasswordField('密码',
                             validators=[DataRequired('密码不能为空')])

    repassword = PasswordField('再次确认',
                               validators=[
                                   DataRequired('再次确认你的密码'),
                                   EqualTo('password', message='两次输入密码不一致')
                               ])

    def validate_name(self, field):
        user = User.query.filter(User.name == self.name.data).first()
        if user:
            raise ValueError('用户名已存在')

    def validate_email(self, field):
        user = User.query.filter(User.email == self.email.data).first()
        if user:
            raise ValueError('邮箱已被注册')

    def validate_code(self, field):
        code = InvitationCode.query.filter(InvitationCode.code == self.code.data).first()
        if not code or code.used:
            raise ValueError('无效的邀请码')


class ChangePasswordForm(Form):
    password = PasswordField('当前密码',
                             validators=[DataRequired('当前密码不能为空')])

    new_password = PasswordField('新的密码',
                                 validators=[DataRequired('新密码不能为空')])

    re_new_password = PasswordField('确认密码',
                                    validators=[
                                        DataRequired('请再输入一次新密码'),
                                        EqualTo('new_password', message='两次输入密码不一致')])

    def validate_password(self, field):
        if not g.user or not g.user.check_password(self.password.data):
            raise ValueError('密码错误')


class ForgotPasswordForm(Form):
    email = StringField('注册邮箱',
                        validators=[
                            DataRequired(message="邮箱不能为空"),
                            Email(message="无效的邮箱")
                        ])

    def validate_email(self, field):
        user = User.query.filter(User.email == self.email.data).first()
        if not user:
            raise ValueError('账号不存在')


class ResetPasswordForm(Form):
    new_password = PasswordField('新的密码',
                                 validators=[DataRequired('新密码不能为空')])

    re_new_password = PasswordField('确认密码',
                                    validators=[
                                        DataRequired('请再输入一次新密码'),
                                        EqualTo('new_password', message='两次输入密码不一致')])
