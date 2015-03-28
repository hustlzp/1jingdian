# coding: utf-8
from flask import g
from urlparse import urlparse
from datetime import datetime, date
from ._base import db
from .collection import CollectionPiece


class Piece(db.Model):
    """Model for text piece"""
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    original = db.Column(db.Boolean, default=False)
    author = db.Column(db.String(100))
    source = db.Column(db.String(100))
    source_link = db.Column(db.String(200))
    source_link_title = db.Column(db.String(200))
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
        return g.user.voted_pieces.filter(PieceVote.piece_id == self.id).count() > 0

    def collected_by_user(self):
        if not g.user:
            return False
        return g.user.colleced_pieces.filter(CollectionPiece.piece_id == self.id).count() > 0

    @property
    def source_link_favicon(self):
        result = urlparse(self.source_link)
        host = "%s://%s" % (result.scheme or "http", result.netloc)
        return "http://g.soz.im/%s" % host

    def __repr__(self):
        return '<Piece %s>' % self.id


class PieceVote(db.Model):
    """每日文字的投票（顶）"""
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('voted_pieces',
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


class PieceSource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    count = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.now)


class PieceAuthor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    count = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.now)


class PIECE_EDIT_KIND(object):
    # collection
    ADD_TO_COLLECTION = 1
    REMOVE_FROM_COLLECTION = 2

    # content
    UPDATE_CONTENT = 3

    # authro
    ADD_AUTHOR = 4
    UPDATE_AUTHOR = 5
    DELETE_AUTHOR = 6

    # source
    ADD_SOURCE = 7
    UPDATE_SOURCE = 8
    DELETE_SOURCE = 9

    # source link
    ADD_SOURCE_LINK = 10
    UPDATE_SOURCE_LINK = 11
    DELETE_SOURCE_LINK = 12


class PieceEditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    kind = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User',
                           backref=db.backref('edited_pieces',
                                              lazy='dynamic',
                                              order_by='desc(CollectionPiece.created_at)'))

    piece_id = db.Column(db.Integer, db.ForeignKey('piece.id'))
    piece = db.relationship('Piece',
                            backref=db.backref('logs',
                                               lazy='dynamic',
                                               order_by='asc(CollectionPiece.created_at)'))

    collection_id = db.Column(db.Integer, db.ForeignKey('collection.id'))
    collection = db.relationship('Collection')
