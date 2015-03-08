# coding: utf-8
from flask import render_template, Blueprint, redirect, request, url_for, g, \
    get_template_attribute, json, abort
from ..forms import SigninForm, SignupForm
from ..utils.account import signin_user, signout_user
from ..utils.permissions import VisitorPermission, UserPermission
from ..models import db, User, Book, Piece, PieceVote, PieceComment
from ..forms import PieceForm

bp = Blueprint('piece', __name__)


@bp.route('/<int:uid>')
def view(uid):
    """Single piece page"""
    piece = Piece.query.get_or_404(uid)
    return render_template("piece/piece.html", piece=piece)


@bp.route('/<int:uid>/modal')
def modal(uid):
    piece = Piece.query.get_or_404(uid)
    piece.clicks_count += 1
    db.session.add(piece)
    db.session.commit()
    modal = get_template_attribute('macro/ui.html', 'modal')
    return modal(piece)


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


@bp.route('/<int:uid>/vote', methods=['POST'])
@UserPermission()
def vote(uid):
    piece = Piece.query.get_or_404(uid)
    vote = g.user.vote_pieces.filter(PieceVote.piece_id == uid).first()
    if not vote:
        vote = PieceVote(piece_id=uid)
        g.user.vote_pieces.append(vote)
        piece.votes_count += 1
        db.session.add(g.user)
        db.session.add(piece)
        db.session.commit()
        return json.dumps({'result': True})
    else:
        return json.dumps({'result': False})


@bp.route('/<int:uid>/unvote', methods=['POST'])
@UserPermission()
def unvote(uid):
    piece = Piece.query.get_or_404(uid)
    votes = g.user.vote_pieces.filter(PieceVote.piece_id == uid)
    if not votes.count():
        return json.dumps({'result': False})
    else:
        for vote in votes:
            db.session.delete(vote)
            if piece.votes_count > 0:
                piece.votes_count -= 1
        db.session.add(piece)
        db.session.commit()
        return json.dumps({'result': True})


@bp.route('/<int:uid>/comment', methods=['POST'])
@UserPermission()
def comment(uid):
    """评论"""
    piece = Piece.query.get_or_404(uid)
    content = request.form.get('comment')
    if content:
        comment = PieceComment(content=content, piece_id=uid, user_id=g.user.id)
        db.session.add(comment)
        db.session.commit()
        comment_macro = get_template_attribute('macro/ui.html', 'render_comment')
        return comment_macro(comment)
    else:
        abort(500)
