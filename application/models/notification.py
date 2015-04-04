# coding: utf-8
from datetime import datetime
from ._base import db


class NOTIFICATION_KIND(object):
    COMMENT_PIECE = 1
    COMMENT_PIECE_COMMENT = 2
    COMMENT_FEEDBACK = 3
    NEW_BLOG = 4


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kind = db.Column(db.Integer, nullable=False)
    target = db.Column(db.String(100))
    content = db.Column(db.Text, default="")
    link = db.Column(db.String(200))
    checked = db.Column(db.Boolean, nullable=False, default=False)
    checked_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.now)

    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    sender = db.relationship('User',
                             backref=db.backref('sender_notifications', lazy='dynamic',
                                                order_by="desc(Notification.created_at)",
                                                cascade="all, delete, delete-orphan"),
                             foreign_keys=[sender_id])

    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    receiver = db.relationship('User', backref=db.backref('notifications', lazy='dynamic',
                                                          order_by="desc(Notification.created_at)",
                                                          cascade="all, delete, delete-orphan"),
                               foreign_keys=[receiver_id])
