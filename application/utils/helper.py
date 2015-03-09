# coding: utf-8
from datetime import date, timedelta
from ..models import db, Piece


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
        'date': day,
        'date_string': date_string,
        'pieces': pieces,
        'hide_pieces': hide_pieces,
        'hide_pieces_count': hide_pieces_count
    }
