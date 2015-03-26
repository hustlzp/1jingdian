# coding: utf-8
from datetime import datetime, date, timedelta
from flask import render_template, Blueprint, redirect, request, url_for, g, \
    get_template_attribute, json, abort
from ..utils.permissions import VisitorPermission, UserPermission, CollectionEditPermission
from ..models import db, User, Piece, PieceVote, PieceComment, Collection, CollectionPiece
from ..forms import CollectionForm
from ..utils.uploadsets import collection_covers, process_avatar

bp = Blueprint('collection', __name__)


@bp.route('/collection/<int:uid>', defaults={'page': 1})
@bp.route('/collection/<int:uid>/page/<int:page>')
def view(uid, page):
    collection = Collection.query.get_or_404(uid)
    pieces = collection.pieces.paginate(page, 20)
    return render_template('collection/view.html', collection=collection, pieces=pieces)


@bp.route('/collection/<int:uid>/hot', defaults={'page': 1})
@bp.route('/collection/<int:uid>/hot/page/<int:page>')
def hot_view(uid, page):
    collection = Collection.query.get_or_404(uid)
    pieces = Piece.query.filter(Piece.collections.any(CollectionPiece.collection_id == uid)) \
        .order_by(Piece.votes_count.desc()).paginate(page, 20)
    return render_template('collection/hot_view.html', collection=collection, pieces=pieces)


@bp.route('/collection/<int:uid>/voted', defaults={'page': 1})
@bp.route('/collection/<int:uid>/voted/page/<int:page>')
@UserPermission()
def voted_view(uid, page):
    collection = Collection.query.get_or_404(uid)
    pieces = collection.voted_pieces_by_user.paginate(page, 20)
    return render_template('collection/voted_view.html', collection=collection, pieces=pieces)


@bp.route('/collection_bars/<int:piece_id>', methods=['POST'])
@UserPermission()
def collection_bars(piece_id):
    """Ajax: 返回collection_bars的HTML"""
    collection_bars_macro = get_template_attribute('macro/ui.html', 'render_collection_bars')
    return collection_bars_macro(g.user.collections, piece_id)


@bp.route('/collection/<int:uid>/edit', methods=['GET', 'POST'])
def edit(uid):
    collection = Collection.query.get_or_404(uid)
    permission = CollectionEditPermission(collection)
    if not permission.check():
        return permission.deny()

    form = CollectionForm(obj=collection)
    if form.validate_on_submit():
        form.populate_obj(collection)
        db.session.add(collection)
        db.session.commit()
        return redirect(url_for('collection.view', uid=uid))
    return render_template('collection/edit.html', form=form, collection=collection)


@bp.route('/collection/add_and_collect/<int:piece_id>', methods=['POST'])
@UserPermission()
def add_and_collect(piece_id):
    piece = Piece.query.get_or_404(piece_id)
    title = request.form.get('title')
    desc = request.form.get('desc')

    if not title:
        return json.dumps({'result': False})
    collection = g.user.collections.filter(Collection.title == title).first()
    if collection:
        return json.dumps({'result': False, 'error': 'repeat'})

    collection = Collection(title=title, desc=desc, user_id=g.user.id)
    collect = CollectionPiece(collection_owner_id=g.user.id, piece_id=piece_id)
    collection.pieces.append(collect)
    db.session.add(collection)

    g.user.collections_count += 1
    db.session.add(g.user)
    db.session.commit()

    collection_bars_macro = get_template_attribute('macro/ui.html', 'render_collection_bars')
    collection_bars_html = collection_bars_macro(g.user.collections, piece_id)
    return json.dumps({'result': True, 'collection_bars_html': collection_bars_html})


@bp.route('/collection/<int:uid>/upload_cover', methods=['POST'])
@UserPermission()
def upload_cover(uid):
    collection = Collection.query.get_or_404(uid)
    try:
        filename = process_avatar(request.files['file'], collection_covers, 160)
    except Exception, e:
        return json.dumps({'result': False, 'error': e.__repr__()})
    else:
        collection.cover = filename
        db.session.add(collection)
        db.session.commit()
        return json.dumps({'result': True, 'avatar_url': collection_covers.url(filename)})

