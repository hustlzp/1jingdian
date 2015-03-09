# coding: utf-8
from datetime import date, timedelta
from flask import render_template, Blueprint
from ..models import db, Piece

bp = Blueprint('site', __name__)


@bp.route('/')
def index():
    """Index page."""
    today = date.today()
    today_pieces = get_pieces_data_by_day(today)
    yesterday = today - timedelta(days=1)
    yesterday_pieces = get_pieces_data_by_day(yesterday)
    the_day_before_yesterday = today - timedelta(days=2)
    the_day_before_yesterday_pieces = get_pieces_data_by_day(the_day_before_yesterday)
    if today_pieces['pieces'].count():
        first_piece = today_pieces['pieces'].first()
    elif yesterday_pieces['pieces'].count():
        first_piece = yesterday_pieces['pieces'].first()
    elif the_day_before_yesterday_pieces['pieces'].count():
        first_piece = the_day_before_yesterday_pieces['pieces'].first()
    else:
        first_piece = None
    return render_template('site/index.html', today_pieces=today_pieces,
                           yesterday_pieces=yesterday_pieces,
                           the_day_before_yesterday_pieces=the_day_before_yesterday_pieces,
                           first_piece=first_piece)


def get_pieces_data_by_day(day):
    """获取某天的pieces"""
    SHOW_PIECES_COUNT = 2
    pieces_count = Piece.query.filter(db.func.date(Piece.created_at) == day).count()
    hide_pieces_count = pieces_count - SHOW_PIECES_COUNT if pieces_count > SHOW_PIECES_COUNT else 0
    if hide_pieces_count:
        hide_pieces = pieces = Piece.query.filter(db.func.date(Piece.created_at) == day).order_by(
            Piece.votes_count.desc()).offset(SHOW_PIECES_COUNT)
    else:
        hide_pieces = None
    pieces = Piece.query.filter(db.func.date(Piece.created_at) == day).order_by(
        Piece.votes_count.desc()).limit(SHOW_PIECES_COUNT)
    if day == date.today():
        date_string = '今天'
    elif day == date.today() - timedelta(days=1):
        date_string = '昨天'
    else:
        date_string = "%s年%s月%s日" % (day.year, day.month, day.day)
    return {
        'date': date_string,
        'pieces': pieces,
        'hide_pieces': hide_pieces,
        'hide_pieces_count': hide_pieces_count
    }


@bp.route('/about')
def about():
    """About page."""
    return render_template('site/about.html')
