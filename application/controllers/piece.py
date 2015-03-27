# coding: utf-8
from datetime import datetime, date, timedelta
from flask import render_template, Blueprint, redirect, request, url_for, g, \
    get_template_attribute, json, abort
from ..utils.permissions import UserPermission, PieceAddPermission
from ..models import db, User, Piece, PieceVote, PieceComment, CollectionPiece, Collection, \
    PieceSource, PieceAuthor
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
    piece.clicks_count += 1
    db.session.add(piece)
    db.session.commit()
    return render_template("piece/view.html", piece=piece)


@bp.route('/piece/<int:uid>/add_clicks_count', methods=['POST'])
def add_clicks_count(uid):
    piece = Piece.query.get_or_404(uid)
    piece.clicks_count += 1
    db.session.add(piece)
    db.session.commit()
    return json.dumps({'result': True})


@bp.route('/piece/<int:uid>/modal')
def modal(uid):
    piece = Piece.query.get_or_404(uid)
    piece.clicks_count += 1
    db.session.add(piece)
    db.session.commit()
    modal = get_template_attribute('macro/ui.html', 'render_piece_details_wap')
    return modal(piece)


@bp.route('/piece/add', methods=['GET', 'POST'])
@UserPermission()
def add():
    permission = PieceAddPermission()
    if not permission.check():
        return permission.deny()

    form = PieceForm()
    if form.validate_on_submit():
        piece = Piece(**form.data)
        piece.user_id = g.user.id
        db.session.add(piece)

        if piece.source:
            _save_piece_source(piece.source)
        if piece.author:
            _save_piece_author(piece.author)
        g.user.pieces_count += 1

        db.session.add(g.user)
        db.session.commit()
        return redirect(url_for('.view', uid=piece.id))
    return render_template('piece/add.html', form=form)


@bp.route('/piece/<int:uid>/edit', methods=['GET', 'POST'])
@UserPermission()
def edit(uid):
    piece = Piece.query.get_or_404(uid)
    form = PieceForm(obj=piece)
    if form.validate_on_submit():
        source = form.source.data
        author = form.author.data
        if source and source != piece.source:
            _save_piece_source(source)
        if author and author != piece.author:
            _save_piece_author(author)

        form.populate_obj(piece)
        if piece.original:
            piece.author = ""
            piece.source = ""
            piece.source_link = ""
        db.session.add(piece)
        db.session.commit()
        return redirect(url_for('.view', uid=piece.id))
    return render_template('piece/edit.html', piece=piece, form=form)


@bp.route('/piece/<int:uid>/vote', methods=['POST'])
@UserPermission()
def vote(uid):
    piece = Piece.query.get_or_404(uid)
    vote = g.user.voted_pieces.filter(PieceVote.piece_id == uid).first()
    if not vote:
        vote = PieceVote(piece_id=uid)
        g.user.voted_pieces.append(vote)
        g.user.votes_count += 1
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
            if g.user.votes_count > 0:
                g.user.votes_count -= 1
            if piece.votes_count > 0:
                piece.votes_count -= 1
        db.session.add(g.user)
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


@bp.route('/piece/<int:uid>/add_to_collection_by_title', methods=['POST'])
@UserPermission()
def add_to_collection_by_title(uid):
    piece = Piece.query.get_or_404(uid)
    title = request.form.get('title')

    if title:
        title = title.strip().replace(" ", "")
    if title:
        # 若不存在该title的句集，则创建
        collection = Collection.query.filter(Collection.title == title).first()
        if not collection:
            collection = Collection(title=title)
            db.session.add(collection)
            db.session.commit()

        # 若该句集尚未收录此句子，则收录
        collection_piece = CollectionPiece.query.filter(
            CollectionPiece.collection_id == collection.id,
            CollectionPiece.piece_id == uid).first()
        if not collection_piece:
            collection_piece = CollectionPiece(user_id=g.user.id, collection_id=collection.id,
                                               piece_id=uid)
            db.session.add(collection_piece)
            db.session.commit()
        macro = get_template_attribute('macro/ui.html', 'render_collection_tag_wap')
        return json.dumps({'result': True,
                           'id': collection.id,
                           'html': macro(collection)})
    else:
        return json.dumps({'result': False})


@bp.route('/piece/<int:uid>/add_to_collection_by_id', methods=['POST'])
@UserPermission()
def add_to_collection_by_id(uid):
    piece = Piece.query.get_or_404(uid)
    collection_id = request.form.get('collection_id', type=int)

    if not collection_id:
        abort(400)
    collection = Collection.query.get_or_404(collection_id)

    # 若该句集尚未收录此句子，则收录
    collection_piece = CollectionPiece.query.filter(
        CollectionPiece.collection_id == collection.id,
        CollectionPiece.piece_id == uid).first()
    if not collection_piece:
        collection_piece = CollectionPiece(user_id=g.user.id, collection_id=collection.id,
                                           piece_id=uid)
        db.session.add(collection_piece)
        db.session.commit()
    macro = get_template_attribute('macro/ui.html', 'render_collection_tag_wap')
    return json.dumps({'result': True,
                       'id': collection.id,
                       'html': macro(collection)})


@bp.route('/piece/<int:uid>/remove_from_collection/<int:collection_id>', methods=['POST'])
@UserPermission()
def remove_from_collection(uid, collection_id):
    """将某句子从某句集中移除"""
    piece = Piece.query.get_or_404(uid)
    collection = Collection.query.get_or_404(collection_id)
    collection_piece = CollectionPiece.query.filter(
        CollectionPiece.collection_id == collection_id,
        CollectionPiece.piece_id == uid)
    map(db.session.delete, collection_piece)
    db.session.commit()
    return json.dumps({'result': True})


def _save_piece_source(source):
    """存储Piece来源，若存在，则count加1"""
    piece_source = PieceSource.query.filter(PieceSource.name == source).first()
    if piece_source:
        piece_source.count += 1
    else:
        piece_source = PieceSource(name=source)
        db.session.add(piece_source)
        db.session.commit()
    return piece_source.id


def _save_piece_author(author):
    """存储Piece原作者，若存在，则count加1"""
    piece_author = PieceAuthor.query.filter(PieceSource.name == author).first()
    if piece_author:
        piece_author.count += 1
    else:
        piece_author = PieceSource(name=author)
        db.session.add(piece_author)
        db.session.commit()
    return piece_author.id