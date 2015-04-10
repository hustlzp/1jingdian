# coding: utf-8
from datetime import datetime
from ._base import db


class FEEDBACK_KIND(object):
    pass


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, default="")
    created_at = db.Column(db.DateTime, default=datetime.now)
    processed = db.Column(db.Boolean, default=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User',
                           backref=db.backref('feedbacks', lazy='dynamic',
                                              order_by="desc(Feedback.created_at)",
                                              cascade="all, delete, delete-orphan"))
