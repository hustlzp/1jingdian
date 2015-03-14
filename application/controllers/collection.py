# coding: utf-8
from datetime import datetime, date, timedelta
from flask import render_template, Blueprint, redirect, request, url_for, g, \
    get_template_attribute, json, abort
from ..utils.permissions import VisitorPermission, UserPermission, CollectionOwnerPermission
from ..models import db, User, Piece, PieceVote, PieceComment, Collection, CollectionPiece
from ..forms import CollectionForm

bp = Blueprint('collection', __name__)


@bp.route('/collection/<int:uid>')
def view(uid):
    collection = Collection.query.get_or_404(uid)
    return render_template('collection/view.html', collection=collection)


@bp.route('/collection_bars/<int:piece_id>', methods=['POST'])
@UserPermission()
def collection_bars(piece_id):
    """Ajax: 返回collection_bars的HTML"""
    collection_bars_macro = get_template_attribute('macro/ui.html', 'render_collection_bars')
    return collection_bars_macro(g.user.collections, piece_id)


@bp.route('/collection/<int:uid>/edit', methods=['GET', 'POST'])
def edit(uid):
    collection = Collection.query.get_or_404(uid)
    permission = CollectionOwnerPermission(collection)
    if not permission.check():
        return permission.deny()

    form = CollectionForm(obj=collection)
    if form.validate_on_submit():
        form.populate_obj(collection)
        db.session.add(collection)
        db.session.commit()
        return redirect(url_for('collection.view', uid=uid))
    return render_template('collection/edit.html', form=form)
