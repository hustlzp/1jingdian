# coding: utf-8
from datetime import datetime, date
from ._base import db


class Piece(db.Model):
    """Model for text piece"""
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    review = db.Column(db.Text)
    page_start = db.Column(db.Integer)
    page_end = db.Column(db.Integer)
    create_at = db.Column(db.DateTime, default=datetime.now)

    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    book = db.relationship('Book', backref=db.backref('pieces', lazy='dynamic',
                                                      order_by='asc(Piece.page_start)'))

    @property
    def start_percentage(self):
        """起始页百分比"""
        return self.page_start * 100 / self.book.pages_num

    @property
    def width_percentage(self):
        """页面范围百分比"""
        return (self.page_end - self.page_start + 1) * 100 / self.book.pages_num

    def __repr__(self):
        return '<Piece %s>' % self.id