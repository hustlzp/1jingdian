#-*- coding: UTF-8 -*-
from __future__ import division
import datetime
import markdown2
from jd import db


class Book(db.Model):
    """Model for book"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True)
    author = db.Column(db.String(50))
    intro = db.Column(db.Text)
    cover_image = db.Column(db.String(200))
    amazon_url = db.Column(db.String(300))
    douban_url = db.Column(db.String(200))
    pub_date = db.Column(db.Date)
    press = db.Column(db.String(100))
    pages_num = db.Column(db.Integer)
    price = db.Column(db.String(50))
    isbn = db.Column(db.String(50))

    @property
    def friendly_intro(self):
        return markdown2.markdown(self.intro)

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
    create_time = db.Column(db.Date, default=datetime.date.today())

    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    book = db.relationship('Book', backref=db.backref('excerpts', lazy='dynamic'))

    @property
    def friendly_content(self):
        return markdown2.markdown(self.content)

    @property
    def friendly_review(self):
        return markdown2.markdown(self.review)

    @property
    def start_percentage(self):
        return self.page_start * 100 / self.book.pages_num

    @property
    def width_percentage(self):
        return (self.page_end - self.page_start + 1) * 100 / self.book.pages_num

    def __repr__(self):
        return '<Excerpt %s>' % self.title