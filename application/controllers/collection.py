# coding: utf-8
from datetime import datetime, date, timedelta
from flask import render_template, Blueprint, redirect, request, url_for, g, \
    get_template_attribute, json, abort
from ..utils.permissions import VisitorPermission, UserPermission
from ..models import db, User, Piece, PieceVote, PieceComment, Collection, CollectionPiece
from ..utils.helper import get_pieces_data_by_day
from ..forms import PieceForm

bp = Blueprint('collection', __name__)


@bp.route('/collection/<int:uid>')
def view(uid):
    collection = Collection.query.get_or_404(uid)
    return render_template('collection/view.html', collection=collection)


@bp.route('/collection_bars/<int:piece_id>', methods=['POST'])
@UserPermission()
def collection_bars(piece_id):
    collection_bars_macro = get_template_attribute('macro/ui.html', 'render_collection_bars')
    return collection_bars_macro(g.user.collections, piece_id)
