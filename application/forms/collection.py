# coding: utf-8
from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired


class CollectionForm(Form):
    title = StringField('名称', validators=[DataRequired('句集名称不能为空')])
    desc = StringField('描述')
