# coding: utf-8
from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired, Email


class SendInvitationCodeForm(Form):
    email = StringField('邮箱',
                        validators=[
                            DataRequired('邮箱不能为空'),
                            Email('邮箱格式不正确')
                        ],
                        description='Email')
