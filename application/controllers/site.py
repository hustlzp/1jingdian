# coding: utf-8
from datetime import date, timedelta
from flask import render_template, Blueprint
from ..models import db, Piece, Collection

bp = Blueprint('site', __name__)


@bp.route('/page/<int:page>')
@bp.route('/', defaults={'page': 1})
def index(page):
    """Index page."""
    target_day = date.today() - timedelta(days=page - 1)
    pieces = Piece.get_pieces_data_by_day(target_day)
    if page == 1:
        pre_page = None
    else:
        pre_page = page - 1
    next_page = page + 1
    return render_template('site/index.html', pieces=pieces, page=page, pre_page=pre_page,
                           next_page=next_page)


@bp.route('/about')
def about():
    """About page."""
    return render_template('site/about.html')


@bp.route('/search')
def search():
    return render_template('site/search.html')


@bp.route('/collections', defaults={'page': 1})
@bp.route('/collections/page/<int:page>')
def collections(page):
    collections = Collection.query.paginate(page, 20)
    return render_template('site/collections.html', collections=collections)


@bp.route('/test')
def test():
    pass
