# coding: utf-8
from datetime import datetime
from flask import g
from ._base import db
from ..utils.uploadsets import collection_covers


class Collection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    locked = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    cover = db.Column(db.String(200), default="default.png")
    desc = db.Column(db.Text)

    kind_id = db.Column(db.Integer, db.ForeignKey('collection_kind.id'), default=1)
    kind = db.relationship('CollectionKind',
                           backref=db.backref('collections',
                                              lazy='dynamic',
                                              order_by='desc(Collection.created_at)'))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User',
                           backref=db.backref('created_collections',
                                              lazy='dynamic',
                                              order_by='desc(Collection.created_at)'))

    @property
    def cover_url(self):
        return collection_covers.url(self.cover) if self.cover else ""

    @property
    def voted_pieces_by_user(self):
        from . import PieceVote, Piece

        if not g.user:
            return None
        return Piece.query \
            .filter(Piece.collections.any(CollectionPiece.collection_id == self.id)) \
            .filter(Piece.voters.any(PieceVote.user_id == g.user.id))

    def liked_by_user(self):
        return g.user and self.likers.filter(CollectionLike.user_id == g.user.id).count() > 0

    def has_piece(self, piece_id):
        return self.pieces.filter(CollectionPiece.piece_id == piece_id).count() > 0

    @staticmethod
    def get_by_title(title, create_if_not_exist=False):
        """通过title获取句集，若不存在则创建"""
        title = title or ""
        title = title.strip().replace(" ", "")
        if title:
            # 若不存在该title的句集，则创建
            collection = Collection.query.filter(Collection.title == title).first()
            if not collection and create_if_not_exist:
                collection = Collection(title=title, user_id=g.user.id)
                log = CollectionEditLog(user_id=g.user.id, kind=COLLECTION_EDIT_KIND.CREATE)
                collection.logs.append(log)
                db.session.add(collection)
                db.session.commit()
            return collection
        else:
            return None

    def __repr__(self):
        return '<Collection %s>' % self.id


class CollectionKind(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    show_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now())


class CollectionPiece(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now())

    collection_id = db.Column(db.Integer, db.ForeignKey('collection.id'))
    collection = db.relationship('Collection',
                                 backref=db.backref('pieces',
                                                    lazy='dynamic',
                                                    order_by='desc(CollectionPiece.created_at)'))

    piece_id = db.Column(db.Integer, db.ForeignKey('piece.id'))
    piece = db.relationship('Piece',
                            backref=db.backref('collections',
                                               lazy='dynamic',
                                               order_by='asc(CollectionPiece.created_at)'))


class CollectionLike(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now())

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User',
                           backref=db.backref('liked_collections',
                                              lazy='dynamic',
                                              order_by='desc(CollectionLike.created_at)'))

    collection_id = db.Column(db.Integer, db.ForeignKey('collection.id'))
    collection = db.relationship('Collection',
                                 backref=db.backref('likers',
                                                    lazy='dynamic',
                                                    order_by='desc(CollectionLike.created_at)'))


class COLLECTION_EDIT_KIND(object):
    # create
    CREATE = 1

    # title
    UPDATE_TITLE = 7

    # desc
    ADD_DESC = 2
    UPDATE_DESC = 3
    REMOVE_DESC = 4

    # cover
    ADD_COVER = 5
    UPDATE_COVER = 6


class CollectionEditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    kind = db.Column(db.Integer, nullable=False)
    before = db.Column(db.String(200))
    before_id = db.Column(db.Integer)
    after = db.Column(db.String(200))
    after_id = db.Column(db.Integer)
    compare = db.Column(db.String(500))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User',
                           backref=db.backref('edited_collections',
                                              lazy='dynamic',
                                              order_by='desc(CollectionEditLog.created_at)'))

    collection_id = db.Column(db.Integer, db.ForeignKey('collection.id'))
    collection = db.relationship('Collection',
                                 backref=db.backref('logs',
                                                    lazy='dynamic',
                                                    order_by='desc(CollectionEditLog.created_at)'))

    def reported_by_user(self):
        return g.user and g.user.reported_collection_edit_logs.filter(
            CollectionEditLogReport.log_id == self.id).count() > 0


class CollectionEditLogReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    processed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User',
                           backref=db.backref('reported_collection_edit_logs',
                                              lazy='dynamic',
                                              order_by='desc(CollectionEditLogReport.created_at)'))

    log_id = db.Column(db.Integer, db.ForeignKey('collection_edit_log.id'))
    log = db.relationship('CollectionEditLog',
                          backref=db.backref(
                              'reports',
                              lazy='dynamic',
                              order_by='desc(CollectionEditLogReport.created_at)'
                          ))
