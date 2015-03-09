# coding: utf-8
from flask_wtf import Form
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, URL, Optional
from ..models import User


class PieceForm(Form):
    content = TextAreaField('文字', validators=[DataRequired('内容不能为空')])
    source = StringField('出处', validators=[DataRequired('出处不能为空')])
    source_url = StringField('链接', validators=[Optional(), URL(message='链接格式不正确')])


class PieceCommentForm(Form):
    content = TextAreaField('评论',
                            validators=[DataRequired('评论内容不能为空')],
                            description='评论内容')
