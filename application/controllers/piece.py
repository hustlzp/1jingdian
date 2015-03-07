# coding: utf-8
from flask import render_template, Blueprint, redirect, request, url_for, g
from ..forms import SigninForm, SignupForm
from ..utils.account import signin_user, signout_user
from ..utils.permissions import VisitorPermission, UserPermission
from ..models import db, User, Book, Piece
from ..forms import PieceForm

bp = Blueprint('piece', __name__)


@bp.route('/<int:uid>')
def view(uid):
    """Single piece page"""
    piece = Piece.query.get_or_404(uid)
    return render_template("piece/piece.html", piece=piece)


@bp.route('/add', methods=['GET', 'POST'])
@UserPermission()
def add():
    form = PieceForm()
    if form.validate_on_submit():
        piece = Piece(**form.data)
        piece.user_id = g.user.id
        db.session.add(piece)
        db.session.commit()
        return redirect(url_for('site.index'))
    return render_template('piece/add.html', form=form)