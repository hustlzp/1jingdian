# coding: utf-8
from flask import g
from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import Optional, URL, DataRequired, EqualTo


class SettingsForm(Form):
    motto = StringField('座右铭')
    blog = StringField('博客', validators=[Optional(), URL(message='链接格式不正确')])
    weibo = StringField('微博', validators=[Optional(), URL(message='链接格式不正确')])
    douban = StringField('豆瓣', validators=[Optional(), URL(message='链接格式不正确')])
    zhihu = StringField('知乎', validators=[Optional(), URL(message='链接格式不正确')])


class ChangePasswordForm(Form):
    password = PasswordField('当前密码',
                             validators=[DataRequired('当前密码不能为空')])

    new_password = PasswordField('新密码',
                                 validators=[DataRequired('新密码不能为空')])

    re_new_password = PasswordField('确认密码',
                                    validators=[
                                        DataRequired('请再输入一次新密码'),
                                        EqualTo('new_password', message='两次输入密码不一致')])

    def validate_password(self, field):
        if not g.user or not g.user.check_password(self.password.data):
            raise ValueError('密码错误')
