# coding: utf-8
from datetime import date
from flask import session, abort, redirect, url_for, g
from permission import Rule
from ..models import db, User, Piece


class VisitorRule(Rule):
    def check(self):
        return 'user_id' not in session

    def deny(self):
        return redirect(url_for('site.index'))


class UserRule(Rule):
    def check(self):
        return 'user_id' in session

    def deny(self):
        return redirect(url_for('account.signin'))


class AdminRule(Rule):
    def base(self):
        return UserRule()

    def check(self):
        user_id = int(session['user_id'])
        user = User.query.filter(User.id == user_id).first()
        return user and user.is_admin

    def deny(self):
        abort(403)


class PieceOwnerRule(Rule):
    def __init__(self, piece):
        self.piece = piece
        super(PieceOwnerRule, self).__init__()

    def base(self):
        return UserRule()

    def check(self):
        return self.piece and self.piece.user_id == g.user.id

    def deny(self):
        abort(403)


class PieceAddRule(Rule):
    def base(self):
        return UserRule()

    def check(self):
        today_pieces_count = g.user.pieces.filter(
            db.func.date(Piece.created_at) == date.today()).count()
        return today_pieces_count < 2

    def deny(self):
        abort(403)


class TrustedUserRule(Rule):
    """受信赖句子：发表过 5 个以上获得 5 次顶的句子的用户。"""

    def base(self):
        return UserRule()

    def check(self):
        return g.user.pieces.filter(Piece.votes_count >= 5).count() >= 5

    def deny(self):
        abort(403)


class CollectionEditableRule(Rule):
    def __init__(self, collection):
        self.collection = collection
        super(CollectionEditableRule, self).__init__()

    def check(self):
        return self.collection and self.collection.locked

    def deny(self):
        abort(403)


class CollectionCreatorRule(Rule):
    def __init__(self, collection):
        self.collection = collection
        super(CollectionCreatorRule, self).__init__()

    def base(self):
        return UserRule()

    def check(self):
        return self.collection.user_id == g.user.id

    def deny(self):
        abort(403)
