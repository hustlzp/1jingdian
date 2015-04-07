# coding: utf-8
import re
import math
from flask_wtf import Form
from wtforms import StringField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, URL, Optional


class PieceForm(Form):
    content = TextAreaField('句子', validators=[DataRequired('句子不能为空')])
    original = BooleanField('原创', default=False)
    author = StringField('原作者', validators=[Optional()], description='选填')
    source = StringField('出处', validators=[Optional()])
    source_link = StringField('链接', validators=[Optional(), URL(message='链接格式不正确')],
                              description='选填')

    def validate_content(self, field):
        content = self.content.data
        content = content.strip()  # 去除首尾的空格
        content = re.sub('\r\n', '', content)  # 去掉换行符
        content = re.sub('\s+', ' ', content)  # 将多个空格替换为单个空格
        self.content.data = content

        cn_length = (len(bytes(content)) - len(content)) / 2
        en_length = len(content) - cn_length
        content_length = cn_length + int(math.ceil(en_length / 2.0))

        if content_length > 160:
            raise ValueError('不超过160字')


class PieceCommentForm(Form):
    content = TextAreaField('评论',
                            validators=[DataRequired('评论内容不能为空')],
                            description='评论内容')
