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

    # today = date.today()
    # today_pieces = get_pieces_data_by_day(today)
    # yesterday = today - timedelta(days=1)
    # yesterday_pieces = get_pieces_data_by_day(yesterday)
    # the_day_before_yesterday = today - timedelta(days=2)
    # the_day_before_yesterday_pieces = get_pieces_data_by_day(the_day_before_yesterday)
    # if today_pieces['pieces'].count():
    # first_piece = today_pieces['pieces'].first()
    # elif yesterday_pieces['pieces'].count():
    # first_piece = yesterday_pieces['pieces'].first()
    # elif the_day_before_yesterday_pieces['pieces'].count():
    # first_piece = the_day_before_yesterday_pieces['pieces'].first()
    # else:
    # first_piece = None
    # start_date = (the_day_before_yesterday - timedelta(days=1)).strftime("%Y-%m-%d")
    # return render_template('site/index.html', today_pieces=today_pieces,
    # yesterday_pieces=yesterday_pieces,
    # the_day_before_yesterday_pieces=the_day_before_yesterday_pieces,
    #                        first_piece=first_piece, start_date=start_date)


@bp.route('/about')
def about():
    """About page."""
    return render_template('site/about.html')
