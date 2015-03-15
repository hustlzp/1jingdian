# coding: utf-8
from datetime import date, timedelta
from flask import render_template, Blueprint
from ..models import db, Piece
from ..utils.helper import get_pieces_data_by_day

bp = Blueprint('site', __name__)


@bp.route('/page/<int:page>')
@bp.route('/', defaults={'page': 1})
def index(page):
    """Index page."""
    target_day = date.today() - timedelta(days=page - 1)
    pieces = get_pieces_data_by_day(target_day)
    first_piece = pieces['pieces'].first()
    if page == 1:
        pre_page = None
    else:
        pre_page = page - 1
    next_page = page + 1
    return render_template('site/index.html', pieces=pieces, page=page, pre_page=pre_page,
                           next_page=next_page, first_piece=first_piece)


@bp.route('/about')
def about():
    """About page."""
    return render_template('site/about.html')
