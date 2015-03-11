# coding: utf-8
from flask_wtf import Form
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, URL, Optional
from ..models import User


class PieceForm(Form):
    content = TextAreaField('文字', validators=[DataRequired('文字不能为空')])
    book = StringField('书籍', validators=[DataRequired('书籍不能为空')])
