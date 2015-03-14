# coding: utf-8
from flask_wtf import Form
from wtforms import StringField, PasswordField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email, URL, Optional
from ..models import User


class CollectionForm(Form):
    title = StringField('标题', validators=[DataRequired('标题不能为空')])
    desc = StringField('简介')
