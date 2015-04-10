# coding: utf-8
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from ._base import db
from ..utils.uploadsets import avatars


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50), unique=True)
    avatar = db.Column(db.String(200), default='default.png')
    motto = db.Column(db.String(100))
    password = db.Column(db.String(200))
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    votes_count = db.Column(db.Integer, default=0)
    pieces_count = db.Column(db.Integer, default=0)
    liked_collections_count = db.Column(db.Integer, default=0)

    # 社交媒体
    weibo = db.Column(db.String(100))
    zhihu = db.Column(db.String(100))
    douban = db.Column(db.String(100))
    blog = db.Column(db.String(100))

    def __setattr__(self, name, value):
        # Hash password when set it.
        if name == 'password':
            value = generate_password_hash(value)
        super(User, self).__setattr__(name, value)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def avatar_url(self):
        return avatars.url(self.avatar)

    def __repr__(self):
        return '<User %s>' % self.name


class InvitationCode(db.Model):
    """"""
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(200))
    email = db.Column(db.String(100))
    used = db.Column(db.Boolean, default=False)
    sended_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.now)

    # 当用户使用此邀请码注册后，填充user_id字段
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), default=None)
    user = db.relationship('User', backref=db.backref('invitation_code',
                                                      cascade="all, delete, delete-orphan",
                                                      uselist=False))
