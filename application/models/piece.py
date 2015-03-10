# coding: utf-8
from flask import g
from urlparse import urlparse
from datetime import datetime, date
from ._base import db


class Piece(db.Model):
    """Model for text piece"""
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    source = db.Column(db.String(100))
    source_url = db.Column(db.String(200))
    clicks_count = db.Column(db.Integer, default=0)
    votes_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('created_pieces',
                                                      lazy='dynamic',
                                                      order_by='desc(Piece.created_at)'))

    def voted_by_user(self):
        if not g.user:
            return False
        return g.user.vote_pieces.filter(PieceVote.piece_id == self.id).count() > 0

    @property
    def source_favicon(self):
        result = urlparse(self.source_url)
        host = "%s://%s" % (result.scheme or "http", result.netloc)
        return "http://g.soz.im/%s" % host

    def __repr__(self):
        return '<Piece %s>' % self.id


class PieceVote(db.Model):
    """每日文字的投票（顶）"""
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('vote_pieces',
                                                      lazy='dynamic',
                                                      order_by='desc(PieceVote.created_at)'))

    piece_id = db.Column(db.Integer, db.ForeignKey('piece.id'))
    piece = db.relationship('Piece', backref=db.backref('voters',
                                                        lazy='dynamic',
                                                        order_by='asc(PieceVote.created_at)'))


class PieceComment(db.Model):
    """文字评论"""
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)
    likes_count = db.Column(db.Integer, default=0)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('piece_comments',
                                                      lazy='dynamic',
                                                      order_by='desc(PieceComment.created_at)'))

    piece_id = db.Column(db.Integer, db.ForeignKey('piece.id'))
    piece = db.relationship('Piece', backref=db.backref('comments',
                                                        lazy='dynamic',
                                                        order_by='asc(PieceComment.created_at)'))


class PieceCommentLike(db.Model):
    """针对文字评论的赞"""
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('piece_comment_likes',
                                                      lazy='dynamic',
                                                      order_by='desc(PieceCommentLike.created_at)'))

    piece_comment_id = db.Column(db.Integer, db.ForeignKey('piece_comment.id'))
    piece_comment = db.relationship('PieceComment',
                                    backref=db.backref('likes',
                                                       lazy='dynamic',
                                                       order_by='asc(PieceCommentLike.created_at)'))
