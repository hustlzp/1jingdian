# coding: utf-8
from datetime import datetime
from ._base import db


class ClickLog(db.Model):
    """点击日志"""
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('click_logs',
                                                      lazy='dynamic',
                                                      order_by='desc(ClickLog.created_at)',
                                                      cascade="all, delete, delete-orphan"))


class SearchLog(db.Model):
    """搜索日志"""
    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('search_logs',
                                                      lazy='dynamic',
                                                      order_by='desc(SearchLog.created_at)',
                                                      cascade="all, delete, delete-orphan"))


class MailLog(db.Model):
    """邮件发送日志"""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200))
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)
