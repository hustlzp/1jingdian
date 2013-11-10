#-*- coding: UTF-8 -*-
import datetime
from jd import db


class Book(db.Model):
    """Model for book"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True)
    author = db.Column(db.String(50))
    intro = db.Column(db.Text)
    cover_image = db.Column(db.String(200))
    amazon_url = db.Column(db.String(200))
    douban_url = db.Column(db.String(200))
    pub_date = db.Column(db.DateTime)
    press = db.Column(db.String(100))
    pages_num = db.Column(db.Integer)
    price = db.Column(db.String(50))

    def __repr__(self):
        return '<Book %s>' % self.title


class Excerpt(db.Model):
    """Model for excerpt"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    review = db.Column(db.Text)
    page_start = db.Column(db.Integer)
    page_end = db.Column(db.Integer)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now())

    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    book = db.relationship('Book', backref=db.backref('excerpts'))

    def __repr__(self):
        return '<Excerpt %s>' % self.title