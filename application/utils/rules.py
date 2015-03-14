# coding: utf-8
from flask import session, abort, flash, redirect, url_for, g
from permission import Rule
from ..models import User


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


class CollectionOwnerRule(Rule):
    def __init__(self, collection):
        self.collection = collection
        super(CollectionOwnerRule, self).__init__()

    def base(self):
        return UserRule()

    def check(self):
        return self.collection and self.collection.user_id == g.user.id

    def deny(self):
        abort(403)
