# coding: utf-8
from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import Optional, URL


class SettingsForm(Form):
    motto = StringField('座右铭')
    blog = StringField('博客', validators=[Optional(), URL(message='链接格式不正确')])
    weibo = StringField('微博', validators=[Optional(), URL(message='链接格式不正确')])
    douban = StringField('豆瓣', validators=[Optional(), URL(message='链接格式不正确')])
    zhihu = StringField('知乎', validators=[Optional(), URL(message='链接格式不正确')])
