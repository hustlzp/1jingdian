# coding: utf-8
from flask_wtf import Form
from wtforms import TextAreaField
from wtforms.validators import DataRequired


class FeedbackForm(Form):
    content = TextAreaField('反馈内容',
                            validators=[DataRequired('反馈内容不能为空')],
                            description="我是壹经典的开发者 hustlzp，把你遇到的问题，或是想要的功能告诉我吧")
