# coding: utf-8
from datetime import datetime, date, timedelta
from flask import render_template, Blueprint, redirect, request, url_for, g, \
    get_template_attribute, json, abort
from ..utils.permissions import VisitorPermission, UserPermission
from ..models import db, User, Piece, PieceVote, PieceComment, CollectionPiece, Collection
from ..utils.helper import get_pieces_data_by_day
from ..forms import PieceForm

bp = Blueprint('piece', __name__)


@bp.route('/pieces_by_date', methods=['POST'])
def pieces_by_date():
    """获取从指定date开始的指定天数的pieces"""
    start = request.form.get('start')
    if start:
        start_date = datetime.strptime(start, '%Y-%m-%d').date()
    else:
        start_date = date.today() - timedelta(days=3)
    days = request.form.get('days', 2, type=int)
    html = ""
    for i in xrange(days):
        target_day = start_date - timedelta(days=i)
        pieces_data = get_pieces_data_by_day(target_day)
        pieces_macro = get_template_attribute('macro/ui.html', 'render_pieces_by_date')
        html += pieces_macro(pieces_data)
    return html


@bp.route('/piece/<int:uid>')
def view(uid):
    """Single piece page"""
    piece = Piece.query.get_or_404(uid)
    return render_template("piece/view.html", piece=piece)


@bp.route('/piece/<int:uid>/modal')
def modal(uid):
    piece = Piece.query.get_or_404(uid)
    piece.clicks_count += 1
    db.session.add(piece)
    db.session.commit()
    modal = get_template_attribute('macro/ui.html', 'render_piece_modal')
    return modal(piece)


@bp.route('/piece/add', methods=['GET', 'POST'])
@UserPermission()
def add():
    form = PieceForm()
    if form.validate_on_submit():
        piece = Piece(**form.data)
        piece.user_id = g.user.id
        db.session.add(piece)
        db.session.commit()
        return redirect(url_for('.view', uid=piece.id))
    return render_template('piece/add.html', form=form)


@bp.route('/piece/<int:uid>/vote', methods=['POST'])
@UserPermission()
def vote(uid):
    piece = Piece.query.get_or_404(uid)
    vote = g.user.voted_pieces.filter(PieceVote.piece_id == uid).first()
    if not vote:
        vote = PieceVote(piece_id=uid)
        g.user.voted_pieces.append(vote)
        piece.votes_count += 1
        db.session.add(g.user)
        db.session.add(piece)
        db.session.commit()
        return json.dumps({'result': True})
    else:
        return json.dumps({'result': False})


@bp.route('/piece/<int:uid>/unvote', methods=['POST'])
@UserPermission()
def unvote(uid):
    piece = Piece.query.get_or_404(uid)
    votes = g.user.voted_pieces.filter(PieceVote.piece_id == uid)
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


@bp.route('/piece/<int:uid>/comment', methods=['POST'])
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


@bp.route('/piece/<int:uid>/collect_to/<int:collection_id>', methods=['POST'])
@UserPermission()
def collect(uid, collection_id):
    piece = Piece.query.get_or_404(uid)
    collection = Collection.query.get_or_404(collection_id)
    collect = g.user.colleced_pieces.filter(CollectionPiece.collection_id == collection_id,
                                            CollectionPiece.piece_id == uid).first()
    if not collect:
        collect = CollectionPiece(collection_id=collection_id, piece_id=uid)
        g.user.colleced_pieces.append(collect)
        db.session.add(g.user)
        db.session.commit()
        return json.dumps({'result': True})
    else:
        return json.dumps({'result': False})


@bp.route('/piece/<int:uid>/uncollect_from/<int:collection_id>', methods=['POST'])
@UserPermission()
def uncollect(uid, collection_id):
    piece = Piece.query.get_or_404(uid)
    collects = g.user.colleced_pieces.filter(CollectionPiece.collection_id == collection_id,
                                             CollectionPiece.piece_id == uid)
    if not collects.count():
        return json.dumps({'result': False})
    else:
        for collect in collects:
            db.session.delete(collect)
        db.session.commit()
        return json.dumps({'result': True})
